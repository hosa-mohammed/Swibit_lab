def get_auth_token(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]


def test_create_task(client):
    token = get_auth_token(client)
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": "high"
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["owner_id"] == 1


def test_list_tasks(client):
    token = get_auth_token(client)
    

    client.post("/tasks/", json={"title": "Task 1"}, 
                headers={"Authorization": f"Bearer {token}"})
    

    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_task(client):
    token = get_auth_token(client)
    

    client.post("/tasks/", json={"title": "Original"}, 
                headers={"Authorization": f"Bearer {token}"})
    

    response = client.patch("/tasks/1", json={"title": "Updated"}, 
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_task(client):
    token = get_auth_token(client)
    

    client.post("/tasks/", json={"title": "To Delete"}, 
                headers={"Authorization": f"Bearer {token}"})
    

    response = client.delete("/tasks/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    

    list_response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert len(list_response.json()) == 0