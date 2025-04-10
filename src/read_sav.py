from constants import (
    SECTION_OFFSETS,
    BLOCK_SIZE,
    SECTION_SIZE,
    NUM_SECTIONS,
    CFRU_EXPANSION_OFFSET_30,
    CFRU_EXPANSION_OFFSET_31,
    SAVE_FILE_SIZE,
    MGBA_SAVE_FILE_SIZE,
)

"""
This module provides functionality to read and process save files (.sav) by extracting
blocks, sections, and specific fields from the data.
Functions:
    read_sav_file(sav_file_path):
        Reads the content of a .sav file.
    extract_field(section, field_name):
        Extracts a specific field from a section using predefined offsets.
    get_block(sav, index):
        Retrieves a block of data from the save file based on the block index.
    get_section(block, index):
        Retrieves a section of data from a block based on the section index.
    get_all_sections(block):
        Retrieves all sections from a block. Raises a ValueError if no valid sections are found.
    get_latest_block(sav):
        Determines the latest block from the save file by comparing the save indices
        of the last sections in the first two blocks.
Constants (imported from constants module):
    SECTION_OFFSETS:
        A dictionary mapping field names to their offsets and sizes within a section.
    BLOCK_SIZE:
        The size of a block in bytes.
    SECTION_SIZE:
        The size of a section in bytes.
    NUM_SECTIONS:
        The number of sections in a block.
"""


def read_sav_file(sav_file_path, trim=False):
    """
    Reads the content of a .sav file.
    Args:
        sav_file_path (io.IOBase): A file-like object representing the .sav file to be read.
    Returns:
        str: The content of the .sav file as a string.
    Raises:
        AttributeError: If the provided object does not have a 'read' method.
    """
    # If trim is True and sav file size is MGBA_SAVE_FILE_SIZE, trim it to SAVE_FILE_SIZE
    file_size = sav_file_path.seek(0, 2)  # Get the file size
    sav_file_path.seek(0)

    if trim and file_size == MGBA_SAVE_FILE_SIZE:
        return sav_file_path.read(SAVE_FILE_SIZE)

    elif file_size == SAVE_FILE_SIZE:
        return sav_file_path.read(SAVE_FILE_SIZE)

    else:
        raise ValueError(
            f"Invalid file size: {file_size}. Expected {SAVE_FILE_SIZE} bytes."
        )


def extract_section_field(section, field_name):
    """
    Extracts a specific field from a section using predefined offsets.
    Args:
        section (bytes): The section data from which the field is to be extracted.
        field_name (str): The name of the field to extract.
    Returns:
        int: The extracted field value as an integer.
    Raises:
        KeyError: If the field_name is not found in SECTION_OFFSETS.
    """
    if field_name not in SECTION_OFFSETS:
        raise KeyError(f"Field '{field_name}' not found in SECTION_OFFSETS")

    start, size = SECTION_OFFSETS[field_name]
    stop = start + size
    raw_bytes = section[start:stop]
    return int.from_bytes(raw_bytes, byteorder="little")


def get_block(sav, index):
    """
    Extracts a block of data from the given sequence based on the specified index.
    Args:
        sav (sequence): The input sequence (e.g., a list, string, or bytes) from which the block is extracted.
        index (int): The index of the block to extract. Each block is of size `BLOCK_SIZE`.
    Returns:
        sequence: A slice of the input sequence corresponding to the block at the specified index.
    """

    start = index * BLOCK_SIZE
    stop = start + BLOCK_SIZE
    return sav[start:stop]


def get_section(block, index):
    """
    Extracts a specific section from a given block of data.
    Args:
        block (bytes or str): The data block from which a section is to be extracted.
        index (int): The index of the section to extract.
    Returns:
        bytes or str: The extracted section of the block, determined by the index and SECTION_SIZE.
    """

    start = index * SECTION_SIZE
    stop = start + SECTION_SIZE
    return block[start:stop]


def get_frlg_sections(block):
    """
    Extracts all sections from the given block.
    This function iterates through a predefined number of sections (`NUM_SECTIONS`)
    and retrieves each section using the `get_section` function. If no valid sections
    are found, it raises a `ValueError`.
    Args:
        block: The data block from which sections are to be extracted.
    Returns:
        list: A list containing all the extracted sections.
    Raises:
        ValueError: If no valid sections are found.
    """

    frlg_sections = {}
    for i in range(NUM_SECTIONS):
        section = get_section(block, i)
        section_id = extract_section_field(section, "section_id")
        frlg_sections[section_id] = section[:-16]

    if not frlg_sections:
        raise ValueError("No valid sections found")

    return frlg_sections


def get_cfru_section(sav, index):
    """
    Extracts the expanded sections from the given save data.
    This function retrieves the sections from the two blocks of the save data,
    specifically focusing on the sections at offsets `CFRU_EXPANSION_OFFSET_30`
    and `CFRU_EXPANSION_OFFSET_31`.
    Args:
        sav: The save data object containing multiple blocks.
    Returns:
        list: A list containing the extracted sections from both blocks.
    """
    if index not in (0, 1):
        raise ValueError("Invalid index. Must be 0 or 1.")

    start = CFRU_EXPANSION_OFFSET_30 if index == 0 else CFRU_EXPANSION_OFFSET_31
    stop = start + SECTION_SIZE

    return sav[start:stop]


def get_all_sections(sav, block_id=2):
    """
    Retrieves all sections from the specified block of data.
    This function extracts sections from a given block of data based on the provided
    block ID.

    It extracts vanilla frlg section and appends cfru sections onto it.

    For block ID 2, the latest block is obtained using the `get_latest_block` function.

    Args:
        sav: The save data object from which blocks and sections are extracted.
        block_id (int, optional): The ID of the block to extract sections from.
            Must be 0, 1, or 2. Defaults to 2.
        ValueError: If an invalid block ID is provided.
    """

    if block_id in (0, 1):
        block = get_block(sav, block_id)
    if block_id == 2:
        block = get_latest_block(sav)
    else:
        raise ValueError("Invalid block ID. Must be 0, 1, or 2.")

    sections = get_frlg_sections(block)

    for i in range(2):
        sections[30 + i] = get_cfru_section(sav, i)

    return sections


def get_latest_block(sav):
    """
    Determines the latest block from the given save data by comparing the save indices
    of the last sections of two blocks.
    Args:
        sav: The save data object containing multiple blocks.
    Returns:
        The latest block (either block A or block B) based on the save index of the
        last section in each block.
    Notes:
        - This function assumes the existence of helper functions `get_block`,
          `get_section`, and `extract_field`.
        - The constant `NUM_SECTIONS` is used to determine the index of the last section.
        - The "save_index" field is extracted from the last section of each block to
          determine which block is the latest.
    """

    block_a = get_block(sav, 0)
    block_b = get_block(sav, 1)

    # Grab last section of each block
    section_a = get_section(block_a, NUM_SECTIONS - 1)
    section_b = get_section(block_b, NUM_SECTIONS - 1)

    # Check the section IDs of both blocks
    save_index_a = extract_section_field(section_a, "save_index")
    save_index_b = extract_section_field(section_b, "save_index")

    # Compare the section IDs to determine which block is the latest
    if save_index_a > save_index_b:
        return block_a
    else:
        return block_b
