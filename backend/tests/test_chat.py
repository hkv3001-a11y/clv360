from unittest.mock import patch, AsyncMock


def test_chat_returns_response(client):
    with patch("routers.chat.chat_completion", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "You have 0 active jobs right now."
        resp = client.post("/api/chat", json={"message": "What's on my plate?"})
        assert resp.status_code == 200
        assert "response" in resp.json()
        assert len(resp.json()["response"]) > 0


def test_chat_action_update_job(client):
    job = client.post("/api/jobs", json={"name": "Johnson Roofing"}).json()
    action_json = f'{{"type":"update_job","job_id":{job["id"]},"updates":{{"status":"completed","percent_complete":100}}}}'
    ai_response = f"[[ACTION:{action_json}]]\nJohnson Roofing has been marked complete."

    with patch("routers.chat.chat_completion", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = ai_response
        resp = client.post("/api/chat", json={"message": "Mark Johnson Roofing done"})
        assert resp.status_code == 200
        data = resp.json()
        assert "Johnson Roofing" in data["response"]
        assert data["action_taken"] is not None

    updated = client.get("/api/jobs").json()
    assert updated[0]["status"] == "completed"
    assert updated[0]["percent_complete"] == 100
