from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_file_type():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "test.txt",
                b"This is not a valid geospatial file",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only .kml and .zip files are allowed"


def test_file_not_found():
    response = client.get("/api/files/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"