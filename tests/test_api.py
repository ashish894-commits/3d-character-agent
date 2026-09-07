"""API integration tests"""

import pytest
from fastapi.testclient import TestClient

from src.api.server import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_character(client):
    """Test character creation endpoint"""
    response = client.post(
        "/api/character/create",
        json={
            "name": "test_hero",
            "gender": "male",
            "age": 30,
            "style": "realistic",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_hero"
    assert "id" in data


def test_list_characters(client):
    """Test list characters endpoint"""
    response = client.get("/api/characters")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_generate_animation(client):
    """Test animation generation endpoint"""
    # First create a character
    char_response = client.post(
        "/api/character/create",
        json={"name": "anim_test"}
    )
    char_id = char_response.json()["id"]
    
    # Generate animation
    response = client.post(
        "/api/animation/generate",
        json={
            "character_id": char_id,
            "animation_type": "walk",
            "duration": 5.0,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "walk"
    assert data["duration"] == 5.0


def test_render_video(client):
    """Test video render endpoint"""
    # Create character first
    char_response = client.post(
        "/api/character/create",
        json={"name": "render_test"}
    )
    char_id = char_response.json()["id"]
    
    # Request render
    response = client.post(
        "/api/render/video",
        json={
            "character_id": char_id,
            "animation_type": "walk",
            "quality": "high",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rendering"


def test_delete_character(client):
    """Test character deletion endpoint"""
    # Create character
    char_response = client.post(
        "/api/character/create",
        json={"name": "to_delete"}
    )
    char_id = char_response.json()["id"]
    
    # Delete character
    response = client.delete(f"/api/character/{char_id}")
    assert response.status_code == 200
