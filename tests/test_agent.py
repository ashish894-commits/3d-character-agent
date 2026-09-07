"""Unit tests for character generator"""

import pytest
import tempfile
from pathlib import Path

from src.agent import CharacterGenerator


@pytest.fixture
def char_gen():
    """Create character generator with temp directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield CharacterGenerator(output_dir=tmpdir)


def test_character_creation(char_gen):
    """Test basic character creation"""
    character = char_gen.create(
        name="test_char",
        gender="male",
        age=30,
    )
    
    assert character["name"] == "test_char"
    assert character["params"]["gender"] == "male"
    assert character["params"]["age"] == 30
    assert character["status"] == "ready"
    assert "id" in character


def test_character_load(char_gen):
    """Test loading character"""
    # Create character
    created = char_gen.create(name="test_char")
    
    # Load character
    loaded = char_gen.load(created["id"])
    
    assert loaded["id"] == created["id"]
    assert loaded["name"] == created["name"]


def test_character_list(char_gen):
    """Test listing characters"""
    # Create multiple characters
    for i in range(3):
        char_gen.create(name=f"char_{i}")
    
    # List characters
    characters = char_gen.list_characters()
    
    assert len(characters) == 3


def test_character_delete(char_gen):
    """Test character deletion"""
    # Create character
    character = char_gen.create(name="to_delete")
    char_id = character["id"]
    
    # Delete character
    success = char_gen.delete(char_id)
    assert success
    
    # Verify deletion
    with pytest.raises(FileNotFoundError):
        char_gen.load(char_id)


def test_invalid_character_load(char_gen):
    """Test loading non-existent character"""
    with pytest.raises(FileNotFoundError):
        char_gen.load("nonexistent_id")
