def test_full_flow(client):

    r = client.post("/auth/register", json={
        "email": "flow@test.com",
        "password": "testpass123"
    })
    assert r.status_code == 200
    

    r = client.post("/auth/login", data={
        "username": "flow@test.com",
        "password": "testpass123"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    r = client.post("/tasks/", json={
        "title": "Integration Test",
        "priority": "high"
    }, headers=headers)
    assert r.status_code == 200
    task_id = r.json()["id"]
    

    r = client.get("/tasks/", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
    

    r = client.patch(f"/tasks/{task_id}", json={
        "is_complete": True
    }, headers=headers)
    assert r.status_code == 200
    assert r.json()["is_complete"] == True
    

    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 200
    

    r = client.get("/tasks/", headers=headers)
    assert len(r.json()) == 0