def test_list_jobs_empty(client):
    resp = client.get("/api/jobs")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_job(client):
    resp = client.post("/api/jobs", json={"name": "Johnson Roofing", "address": "123 Main St"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Johnson Roofing"
    assert data["status"] == "active"
    assert data["percent_complete"] == 0
    assert "id" in data


def test_get_jobs_after_create(client):
    client.post("/api/jobs", json={"name": "Job A"})
    client.post("/api/jobs", json={"name": "Job B"})
    resp = client.get("/api/jobs")
    assert len(resp.json()) == 2


def test_update_job(client):
    job = client.post("/api/jobs", json={"name": "Garcia Drywall"}).json()
    resp = client.put(f"/api/jobs/{job['id']}", json={"percent_complete": 50, "status": "on_hold"})
    assert resp.status_code == 200
    assert resp.json()["percent_complete"] == 50
    assert resp.json()["status"] == "on_hold"


def test_update_job_not_found(client):
    resp = client.put("/api/jobs/999", json={"name": "Ghost"})
    assert resp.status_code == 404


def test_delete_job(client):
    job = client.post("/api/jobs", json={"name": "To Delete"}).json()
    resp = client.delete(f"/api/jobs/{job['id']}")
    assert resp.status_code == 204
    assert client.get("/api/jobs").json() == []


def test_delete_job_not_found(client):
    resp = client.delete("/api/jobs/999")
    assert resp.status_code == 404
