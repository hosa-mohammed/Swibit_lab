from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.logging import logger
from app.api.deps import get_current_user
from app.models.user import User
from app.ai.rag.chunks import build_user_chunks
from app.ai.rag.embeddings import embed_chunks, embed_query
from app.ai.rag.vector_db import UserVectorDB
from app.ai.rag.llm import classify_message, extract_info, rag_answer, rag_answer_stream
from pydantic import BaseModel


router = APIRouter(prefix="/rag", tags=["rag"])

class RAGQuery(BaseModel):
    question: str
    k: int = 3 


class RAGResponse(BaseModel):
    answer: str
    sources: List[dict]
    classification: Optional[dict] = None
    extracted_info: Optional[dict] = None


class RebuildResponse(BaseModel):
    message: str
    chunks_count: int


@router.post("/ask", response_model=RAGResponse)
def ask_rag(
    query: RAGQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    logger.info("RAG query", extra={
        "user_id": current_user.id,
        "question": query.question
    })
    
    vdb = UserVectorDB(current_user.id)
    vdb._load()
    if not vdb.index:
        chunks = build_user_chunks(db, current_user.id)
        if not chunks:
            return RAGResponse(
                answer="لا توجد مهام مسجلة لديك حالياً.",
                sources=[],
                classification=classify_message(query.question),
                extracted_info=extract_info(query.question)
            )
        
        embeddings = embed_chunks(chunks)
        vdb.build(embeddings, chunks)
        logger.info(f"Built new index for user {current_user.id} with {len(chunks)} chunks")

    query_emb = embed_query(query.question)
    results = vdb.search(query_emb, k=query.k)
    
    if not results:
        return RAGResponse(
            answer="لم أجد مهاماً ذات صلة بسؤالك.",
            sources=[],
            classification=classify_message(query.question),
            extracted_info=extract_info(query.question)
        )
    

    answer = rag_answer(query.question, results)
    
    classification = classify_message(query.question)
    extracted = extract_info(query.question)
    
    logger.info("RAG answer generated", extra={
        "user_id": current_user.id,
        "sources_count": len(results)
    })
    
    return RAGResponse(
        answer=answer,
        sources=results,
        classification=classification,
        extracted_info=extracted
    )


@router.post("/rebuild", response_model=RebuildResponse)
def rebuild_index(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    logger.info("Rebuilding RAG index", extra={"user_id": current_user.id})
    
    chunks = build_user_chunks(db, current_user.id)
    
    if not chunks:
        vdb = UserVectorDB(current_user.id)
        vdb.delete()
        return RebuildResponse(
            message="تم حذف الـ index (لا توجد مهام)",
            chunks_count=0
        )
    
    embeddings = embed_chunks(chunks)

    vdb = UserVectorDB(current_user.id)
    vdb.build(embeddings, chunks)
    
    logger.info(f"Index rebuilt: {len(chunks)} chunks", extra={"user_id": current_user.id})
    
    return RebuildResponse(
        message=f"تم إعادة بناء الفهرس بنجاح",
        chunks_count=len(chunks)
    )

@router.get("/status")
def rag_status(current_user: User = Depends(get_current_user)):
    vdb = UserVectorDB(current_user.id)
    vdb._load()
    
    has_index = vdb.index is not None
    
    return {
        "user_id": current_user.id,
        "has_index": has_index,
        "chunks_count": len(vdb.chunks) if has_index else 0,
        "index_path": str(vdb.file_path) if has_index else None
    }