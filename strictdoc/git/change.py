from enum import Enum
from typing import Dict, List, Optional, Union

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.requirement import (
    Requirement,
    RequirementField,
)
from strictdoc.backend.sdoc.models.section import Section
from strictdoc.helpers.auto_described import auto_described


class ChangeType(str, Enum):
    DOCUMENT = "Document"
    DOCUMENT_MODIFIED = "Document modified"

    SECTION = "Section"
    SECTION_REMOVED = "Section removed"
    SECTION_MODIFIED = "Section modified"
    SECTION_ADDED = "Section added"

    REQUIREMENT = "Requirement"
    REQUIREMENT_REMOVED = "Requirement removed"
    REQUIREMENT_MODIFIED = "Requirement modified"
    REQUIREMENT_ADDED = "Requirement added"


@auto_described
class DocumentChange:
    def __init__(
        self,
        *,
        matched_uid: Optional[str],
        lhs_document: Optional[Document],
        rhs_document: Optional[Document],
        title_modified: bool,
        free_text_modified: bool,
        lhs_colored_free_text_diff: Optional[str],
        rhs_colored_free_text_diff: Optional[str],
    ):
        assert lhs_document is not None or rhs_document is not None
        if matched_uid is not None:
            assert len(matched_uid) > 0
        self.matched_uid: Optional[str] = matched_uid
        self.title_modified: bool = title_modified
        self.free_text_modified: bool = free_text_modified
        self.lhs_colored_free_text_diff: Optional[
            str
        ] = lhs_colored_free_text_diff
        self.rhs_colored_free_text_diff: Optional[
            str
        ] = rhs_colored_free_text_diff

        self.lhs_document: Optional[Document] = lhs_document
        self.rhs_document: Optional[Document] = rhs_document

        self.change_type: ChangeType = ChangeType.DOCUMENT_MODIFIED

    def get_colored_free_text_diff(self, side: str) -> Optional[str]:
        if not self.free_text_modified:
            return None
        if side == "left":
            return self.lhs_colored_free_text_diff
        if side == "right":
            return self.rhs_colored_free_text_diff
        raise AssertionError(f"Must not reach here: {side}")


@auto_described
class SectionChange:
    def __init__(
        self,
        *,
        matched_uid: Optional[str],
        lhs_section: Optional[Section],
        rhs_section: Optional[Section],
        free_text_modified: bool,
        lhs_colored_free_text_diff: Optional[str],
        rhs_colored_free_text_diff: Optional[str],
    ):
        assert lhs_section is not None or rhs_section is not None
        if matched_uid is not None:
            assert len(matched_uid) > 0
        self.matched_uid: Optional[str] = matched_uid
        self.free_text_modified: bool = free_text_modified
        self.lhs_colored_free_text_diff: Optional[
            str
        ] = lhs_colored_free_text_diff
        self.rhs_colored_free_text_diff: Optional[
            str
        ] = rhs_colored_free_text_diff

        self.lhs_section: Optional[Section] = lhs_section
        self.rhs_section: Optional[Section] = rhs_section

        if matched_uid is not None:
            change_type = ChangeType.SECTION_MODIFIED
        elif lhs_section is not None:
            change_type = ChangeType.SECTION_REMOVED
        elif rhs_section is not None:
            change_type = ChangeType.SECTION_ADDED
        else:
            raise AssertionError("Must not reach here.")
        self.change_type = change_type

    def get_colored_free_text_diff(self, side: str) -> Optional[str]:
        if side == "left":
            return self.lhs_colored_free_text_diff
        if side == "right":
            return self.rhs_colored_free_text_diff
        raise AssertionError(f"Must not reach here: {side}")


@auto_described
class RequirementFieldChange:
    def __init__(
        self,
        *,
        field_name: str,
        lhs_field: Optional[RequirementField],
        rhs_field: Optional[RequirementField],
        left_diff: Optional[str],
        right_diff: Optional[str],
    ):
        assert isinstance(field_name, str) and len(field_name) > 0
        assert lhs_field is not None or rhs_field is not None
        assert (left_diff is None and right_diff is None) or (
            left_diff is not None and right_diff is not None
        )

        self.field_name: str = field_name
        self.lhs_field: Optional[RequirementField] = lhs_field
        self.rhs_field: Optional[RequirementField] = rhs_field
        self.left_diff: Optional[str] = left_diff
        self.right_diff: Optional[str] = right_diff


@auto_described
class RequirementChange:
    def __init__(
        self,
        *,
        requirement_token: Optional[str],
        lhs_requirement: Optional[Requirement],
        rhs_requirement: Optional[Requirement],
        field_changes: List[RequirementFieldChange],
    ):
        assert requirement_token is None or len(requirement_token) > 0
        assert lhs_requirement is not None or rhs_requirement is not None

        self.requirement_token: Optional[str] = requirement_token
        self.lhs_requirement: Optional[Requirement] = lhs_requirement
        self.rhs_requirement: Optional[Requirement] = rhs_requirement

        self.field_changes: List[RequirementFieldChange] = field_changes

        map_fields_to_changes: Dict[
            RequirementField, RequirementFieldChange
        ] = {}
        for field_change_ in field_changes:
            if field_change_.lhs_field is not None:
                map_fields_to_changes[field_change_.lhs_field] = field_change_
            if field_change_.rhs_field is not None:
                map_fields_to_changes[field_change_.rhs_field] = field_change_
        self.map_fields_to_changes: Dict[
            RequirementField, RequirementFieldChange
        ] = map_fields_to_changes

        if requirement_token is not None:
            change_type = ChangeType.REQUIREMENT_MODIFIED
        elif lhs_requirement is not None:
            change_type = ChangeType.REQUIREMENT_REMOVED
        elif rhs_requirement is not None:
            change_type = ChangeType.REQUIREMENT_ADDED
        else:
            raise AssertionError("Must not reach here.")
        self.change_type = change_type

    def get_field_change(
        self, requirement_field: RequirementField
    ) -> Optional[RequirementFieldChange]:
        assert isinstance(requirement_field, RequirementField)
        return self.map_fields_to_changes.get(requirement_field)


ChangeUnionType = Union[DocumentChange, SectionChange, RequirementChange]
