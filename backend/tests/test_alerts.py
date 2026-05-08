from datetime import datetime, timedelta


def _insert_old_job(conn, name, days_ago):
    dt = (datetime.utcnow() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO jobs (name, status, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (name, "active", dt, dt),
    )
    conn.commit()


def test_no_alerts_for_fresh_jobs(client):
    client.post("/api/jobs", json={"name": "New Job"})
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    assert resp.json()["alerts"] == []


def test_stale_job_triggers_alert(client):
    import database as db
    conn = db.get_connection()
    _insert_old_job(conn, "Old Job", 10)
    conn.close()

    resp = client.get("/api/alerts")
    alerts = resp.json()["alerts"]
    assert len(alerts) == 1
    assert alerts[0]["type"] == "stale_job"
    assert "Old Job" in alerts[0]["message"]
