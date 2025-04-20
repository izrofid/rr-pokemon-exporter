from constants import (
    SAVE_SECTION_SIZE,
    SECTION_DATA_SIZE,
    CHECKSUM_OFFSET,
    SAVE_INDEX_OFFSET,
    SECTION_ID_OFFSET,
)

from utils import get_slice, int_from_slice


class SaveSection:
    def __init__(self, index: int, raw_bytes: bytes):
        if len(raw_bytes) != SAVE_SECTION_SIZE:
            raise ValueError(
                f"Section must be {SAVE_SECTION_SIZE} bytes, got {len(raw_bytes)}"
            )

        self.index = index
        self.raw_bytes = raw_bytes
        self.data = raw_bytes[:SECTION_DATA_SIZE]

        self.checksum = int.from_bytes(get_slice(raw_bytes, CHECKSUM_OFFSET), "little")

        self.save_index = int.from_bytes(
            get_slice(raw_bytes, SAVE_INDEX_OFFSET), "little"
        )

        self.section_id = int_from_slice(raw_bytes, SECTION_ID_OFFSET)
