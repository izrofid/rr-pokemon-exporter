from constants import (
    SAVE_FILE_SIZE,
    RTC_SAVE_SIZE,
    SAVE_SECTION_SIZE,
    CFRU_SECTIONS,
    SAVE_BLOCK_SIZE,
)

from save_block import SaveBlock
from save_block import ExpandedBlock
from utils import get_slice


class SaveFile:
    def __init__(self, raw_bytes: bytes):
        self.raw = self._validate_and_trim(raw_bytes)

        self.block_a_raw, self.block_b_raw = [
            get_slice(raw_bytes, (i * SAVE_BLOCK_SIZE, (i + 1) * SAVE_BLOCK_SIZE))
            for i in range(2)
        ]

        self.cfru_raw = self.raw[
            CFRU_SECTIONS[0]
            * SAVE_SECTION_SIZE : (CFRU_SECTIONS[1] + 1)
            * SAVE_SECTION_SIZE
        ]

        self.block_a = SaveBlock(self.block_a_raw)
        self.block_b = SaveBlock(self.block_b_raw)
        self.expanded_block = ExpandedBlock(self.cfru_raw)

        # Choose active block based on save index
        self.active_block = (
            self.block_a
            if self.block_a.get_save_index() >= self.block_b.get_save_index()
            else self.block_b
        )

    def _validate_and_trim(self, raw: bytes) -> bytes:
        if len(raw) == SAVE_FILE_SIZE:
            return raw
        if len(raw) == RTC_SAVE_SIZE:
            return raw[:SAVE_FILE_SIZE]
        raise ValueError(f"Unexpected save file size: {len(raw)} bytes")
