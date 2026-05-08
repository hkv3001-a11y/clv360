from unittest.mock import patch, AsyncMock


def test_inbound_test_updates_job(client):
    job = client.post("/api/jobs", json={"name": "Garcia Drywall"}).json()

    parsed = {
        "job_id": job["id"],
        "status": "completed",
        "percent_complete": 100,
        "parsed_action": "Job marked complete by Tom",
        "unrecognized": False,
    }
    with patch("routers.inbound.parse_inbound_message", new_callable=AsyncMock) as mock_parse:
        mock_parse.return_value = parsed
        resp = client.post(
            "/api/inbound/test",
            json={"channel": "sms", "sender_name": "Tom R", "message": "Garcia done"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_updated"] is True
    assert data["parsed_action"] == "Job marked complete by Tom"

    updated_job = client.get("/api/jobs").json()[0]
    assert updated_job["status"] == "completed"
    assert updated_job["percent_complete"] == 100


def test_inbound_unrecognized_message(client):
    parsed = {"job_id": None, "unrecognized": True, "parsed_action": "Could not parse"}
    with patch("routers.inbound.parse_inbound_message", new_callable=AsyncMock) as mock_parse:
        mock_parse.return_value = parsed
        resp = client.post(
            "/api/inbound/test",
            json={"channel": "sms", "sender_name": "Unknown", "message": "random text"},
        )
    assert resp.status_code == 200
    assert resp.json()["job_updated"] is False


def test_inbound_sms_stub_returns_501(client):
    resp = client.post("/api/inbound/sms", json={})
    assert resp.status_code == 501


def test_inbound_whatsapp_stub_returns_501(client):
    resp = client.post("/api/inbound/whatsapp", json={})
    assert resp.status_code == 501
