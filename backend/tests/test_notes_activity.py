def test_create_general_note(client):
    resp = client.post("/api/notes", json={"body": "Called supplier about materials"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["body"] == "Called supplier about materials"
    assert data["job_id"] is None


def test_create_note_for_job(client):
    job = client.post("/api/jobs", json={"name": "Test Job"}).json()
    resp = client.post("/api/notes", json={"body": "Permit approved", "job_id": job["id"]})
    assert resp.status_code == 201
    assert resp.json()["job_id"] == job["id"]


def test_list_notes(client):
    client.post("/api/notes", json={"body": "Note 1"})
    client.post("/api/notes", json={"body": "Note 2"})
    resp = client.get("/api/notes")
    assert len(resp.json()) == 2


def test_add_activity_to_job(client):
    job = client.post("/api/jobs", json={"name": "Active Job"}).json()
    resp = client.post(
        f"/api/jobs/{job['id']}/activity",
        json={"source_name": "Mike", "channel": "manual", "raw_message": "Job started", "parsed_action": "Job marked active"},
    )
    assert resp.status_code == 201
    assert resp.json()["job_id"] == job["id"]
    assert resp.json()["source_name"] == "Mike"


def test_list_activity_for_job(client):
    job = client.post("/api/jobs", json={"name": "Job"}).json()
    client.post(f"/api/jobs/{job['id']}/activity", json={"raw_message": "Update 1"})
    client.post(f"/api/jobs/{job['id']}/activity", json={"raw_message": "Update 2"})
    resp = client.get(f"/api/jobs/{job['id']}/activity")
    assert len(resp.json()) == 2


def test_activity_job_not_found(client):
    resp = client.get("/api/jobs/999/activity")
    assert resp.status_code == 404
