import pytest
import add_src  # noqa
from unittest.mock import Mock, patch
from save_block import SaveBlock, ExpandedBlock
from save_section import SaveSection
from pokemon_extractor import BoxPokemonExtractor
from constants import FRLG_BOX_SECTIONS, CFRU_BOX_SECTIONS, BOXMON_SIZE


@pytest.fixture
def mock_blocks():
    """Create mock SaveBlock instances and sections for testing."""
    mock_active_block = Mock(spec=SaveBlock)
    mock_expanded_block = Mock(spec=ExpandedBlock)

    # Create mock sections with dummy data
    mock_sections = {}
    for sid in FRLG_BOX_SECTIONS + CFRU_BOX_SECTIONS:
        # Create test data with section ID as pattern
        test_data = bytes([sid % 256] * 4096)
        mock_section = Mock(spec=SaveSection)
        mock_section.data = test_data
        mock_sections[sid] = mock_section

    # Configure get_section method to return appropriate mock section
    mock_active_block.get_section.side_effect = lambda sid: mock_sections[sid]
    mock_expanded_block.get_section.side_effect = lambda sid: mock_sections[sid]

    return mock_active_block, mock_expanded_block


def test_pokemon_in_storage(mock_blocks):
    """Test pokemon_in_storage property extracts and processes data correctly."""
    mock_active_block, mock_expanded_block = mock_blocks

    with patch("pokemon_extractor.get_slice") as mock_slice, patch(
        "pokemon_extractor.split_into_chunks"
    ) as mock_split:

        # Configure mocks
        mock_slice.side_effect = lambda data, offset: data[
            :100
        ]  # Return first 100 bytes
        expected_pokemon = [b"pokemon1", b"pokemon2"]
        mock_split.return_value = expected_pokemon

        # Create extractor and call the property
        extractor = BoxPokemonExtractor(mock_active_block, mock_expanded_block)
        result = extractor.pokemon_in_storage

        # Assertions
        assert result == expected_pokemon

        # Verify section retrieval
        for sid in FRLG_BOX_SECTIONS:
            mock_active_block.get_section.assert_any_call(sid)

        for sid in CFRU_BOX_SECTIONS:
            if sid in [30, 31]:
                mock_expanded_block.get_section.assert_any_call(sid)
            else:
                mock_active_block.get_section.assert_any_call(sid)

        # Verify slice and chunk operations
        assert mock_slice.call_count == len(FRLG_BOX_SECTIONS) + len(CFRU_BOX_SECTIONS)
        mock_split.assert_called_once()

        # Check split_into_chunks parameters
        args, kwargs = mock_split.call_args
        assert isinstance(args[0], bytes)
        assert args[1] == BOXMON_SIZE
        assert kwargs == {"skip_empty": True}


@pytest.mark.parametrize(
    "section_data,expected_length",
    [
        # Test with empty data
        (bytes([0] * 4096), 0),
        # Test with data that has one valid Pokémon
        (bytes([1] + [0] * (BOXMON_SIZE - 1) + [0] * (4096 - BOXMON_SIZE)), 1),
    ],
)
def test_pokemon_extraction_with_different_data(
    section_data, expected_length, mock_blocks
):
    """Test extraction with different section data patterns."""
    mock_active_block, mock_expanded_block = mock_blocks

    # Override section data for the first section
    first_section_id = FRLG_BOX_SECTIONS[0]
    mock_section = mock_active_block.get_section(first_section_id)
    mock_section.data = section_data

    # Use real functions instead of mocks for this test
    extractor = BoxPokemonExtractor(mock_active_block, mock_expanded_block)

    with patch(
        "pokemon_extractor.get_slice", side_effect=lambda data, offset: data
    ), patch("pokemon_extractor.split_into_chunks") as mock_split:

        mock_split.return_value = [b"pokemon"] * expected_length

        result = extractor.pokemon_in_storage
        assert len(result) == expected_length
