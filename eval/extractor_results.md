# RAG Evaluation Results

## Eval Set: 15 questions

## Before Fix (Broken)
- chunk_size: 3000 (too large)
- overlap: 0 (no context)
- threshold: 0.7

Pass rate: 8/15 = 53%

## Bugs Introduced
1. chunk_size too large -&gt; loses focus
2. overlap=0 -&gt; cuts context between sections

## After Fix
- chunk_size: 600
- overlap: 100
- threshold: 0.85

Pass rate: 12/15 = 80%

## Fixes Applied
1. Reduced chunk_size to 600 for better focus
2. Added overlap=100 to preserve context
3. Raised threshold to 0.85 for stricter relevance

## Conclusion
Pass rate improved from 53% to 80% (+27%)