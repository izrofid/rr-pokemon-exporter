import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import pytest
from read_sav import get_block, get_section, get_latest_block

# Mock constants
BLOCK_SIZE = 57344
SECTION_SIZE = 4096
NUM_SECTIONS = 14

# Mock data
mock_sav_data = b"\x00" * (128 * 1024)  # Mock save file with two empty blocks
mock_block = b"\x00" * BLOCK_SIZE  # Mock block with empty data
mock_section = b"\x00" * SECTION_SIZE  # Mock section with empty data


def test_get_block():
    # Test extracting the first block
    block = get_block(mock_sav_data, 0)
    assert block == mock_block

    # Test extracting the second block
    block = get_block(mock_sav_data, 1)
    assert block == mock_block


def test_get_section():
    # Test extracting the first section
    section = get_section(mock_block, 0)
    assert section == mock_section

    # Test extracting the last section
    section = get_section(mock_block, NUM_SECTIONS - 1)
    assert section == mock_section


def test_get_latest_block():
    # Mock extract_field to return different save indexes
    def mock_extract_field(section, field_name):
        if field_name == "save_index":
            return 5 if section is mock_section else 10
        return 0

    # Patch extract_field in the get_latest_block function
    from read_sav import extract_section_field

    extract_field_backup = extract_section_field
    try:
        from read_sav import extract_section_field

        extract_section_field = mock_extract_field

        # Test get_latest_block
        latest_block = get_latest_block(mock_sav_data)
        assert latest_block == mock_block
    finally:
        # Restore the original extract_field
        extract_section_field = extract_field_backup
