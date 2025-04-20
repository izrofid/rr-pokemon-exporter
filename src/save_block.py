from utils import get_slice
from constants import SAVE_SECTION_SIZE, FINAL_SECTION_ID
from save_section import SaveSection


class BaseBlock:
    def __init__(
        self, raw_bytes: bytes, section_count: int, assign_ids: None | tuple = None
    ):
        self.sections = []
        self.section_map = {}

        for i in range(section_count):
            offset = i * SAVE_SECTION_SIZE
            byte_range = (offset, offset + SAVE_SECTION_SIZE)
            section_data = get_slice(raw_bytes, byte_range)
            section = SaveSection(i, section_data)
            if assign_ids:
                section.section_id = assign_ids[i]
            self.sections.append(section)
            self.section_map[section.section_id] = section

    def get_section(self, section_id: int) -> SaveSection:
        return self.section_map[section_id]


class SaveBlock(BaseBlock):
    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes, 14)

    def get_save_index(self):
        return self.sections[FINAL_SECTION_ID].save_index


class ExpandedBlock(BaseBlock):
    def __init__(self, raw_bytes: bytes, assign_ids: None | tuple = (30, 31)):

        super().__init__(raw_bytes, 2, assign_ids=assign_ids)

    def get_section_by_index(self, index: int) -> SaveSection:
        return self.sections[index]
