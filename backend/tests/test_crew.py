def test_list_crew_empty(client):
    resp = client.get("/api/crew")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_crew_member(client):
    resp = client.post("/api/crew", json={"name": "Mike Chen", "phone": "555-1234"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Mike Chen"
    assert data["phone"] == "555-1234"
    assert "id" in data


def test_update_crew_member(client):
    member = client.post("/api/crew", json={"name": "Tom R"}).json()
    resp = client.put(f"/api/crew/{member['id']}", json={"phone": "555-9999"})
    assert resp.status_code == 200
    assert resp.json()["phone"] == "555-9999"


def test_delete_crew_member(client):
    member = client.post("/api/crew", json={"name": "Dave K"}).json()
    resp = client.delete(f"/api/crew/{member['id']}")
    assert resp.status_code == 204
    assert client.get("/api/crew").json() == []


def test_crew_member_not_found(client):
    resp = client.put("/api/crew/999", json={"name": "Ghost"})
    assert resp.status_code == 404


def test_job_crew_assignment(client):
    member = client.post("/api/crew", json={"name": "Alice"}).json()
    job = client.post("/api/jobs", json={"name": "Roof Job", "crew_member_id": member["id"]}).json()
    assert job["crew_member_id"] == member["id"]
