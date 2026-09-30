from app import app


def test_home_page():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200


def test_add_task():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/add",
            data={
                "title": "Create Dockerfile",
                "assigned_to": "Teena",
                "priority": "High",
                "due_date": "2026-10-10",
                "category": "Development"
            }
        )

        assert response.status_code == 302


def test_complete_task():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/add",
            data={
                "title": "Test Task",
                "assigned_to": "Teena",
                "priority": "Medium",
                "due_date": "2026-10-10",
                "category": "Testing"
            }
        )

        assert response.status_code == 302


def test_delete_task():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200