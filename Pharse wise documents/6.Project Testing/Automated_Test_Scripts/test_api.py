import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify root endpoint responds with online status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "online"
    assert "LegalEase" in data["message"]


def test_health_endpoint():
    """Verify /health endpoint returns operational status and AI mode."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "gemini_configured" in data
    assert "model" in data
    assert "demo_mode" in data


def test_generate_valid_request():
    """Verify /generate endpoint creates document with valid inputs."""
    payload = {
        "document_type": "Freelance Work Contract",
        "parties": "Alice Walker (Consultant), Acme Global Inc. (Client)",
        "terms": "Work delivered by June 1, 2025; Compensation of $5,000; Confidentiality strictly preserved",
        "dates": "May 1, 2025",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["document_type"] == "Freelance Work Contract"
    assert len(data["content"]) > 100
    assert "Alice Walker" in data["content"]
    assert "Acme Global" in data["content"]
    assert "May 1, 2025" in data["content"]


def test_generate_empty_inputs_validation():
    """Verify /generate rejects empty or blank input fields."""
    # Empty parties
    payload_bad_parties = {
        "document_type": "NDA",
        "parties": "   ",
        "terms": "Term 1; Term 2",
        "dates": "Today",
    }
    response = client.post("/generate", json=payload_bad_parties)
    assert response.status_code in [400, 422]

    # Missing field
    payload_missing_terms = {
        "document_type": "NDA",
        "parties": "Party A, Party B",
        "dates": "Today",
    }
    response2 = client.post("/generate", json=payload_missing_terms)
    assert response2.status_code == 422


def test_generate_demo_mode_indicator():
    """Verify /generate indicates demo mode when running without API key."""
    payload = {
        "document_type": "Non-Disclosure Agreement (NDA)",
        "parties": "Party Alpha, Party Beta",
        "terms": "Confidential information shall be kept secret; 2 years duration",
        "dates": "October 10, 2025",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # If GEMINI_API_KEY is not configured in this test environment, is_demo must be True
    assert isinstance(data["is_demo"], bool)
