# mypy: disable-error-code="no-untyped-def,type-arg"
from enum import Enum
from typing import List, Optional

from strictdoc.backend.sdoc_source_code.models.requirement_marker import Req
from strictdoc.helpers.auto_described import auto_described


class RangeMarkerType(Enum):
    FUNCTION = "function"
    CLASS = "class"
    FILE = "file"


@auto_described
class FunctionRangeMarker:
    def __init__(self, parent, reqs_objs: List[Req], scope: str):
        assert isinstance(reqs_objs, list)
        assert isinstance(scope, str), scope
        self.parent = parent
        self.reqs_objs: List[Req] = reqs_objs
        self.reqs: List[str] = list(map(lambda req: req.uid, reqs_objs))

        self.scope: RangeMarkerType = RangeMarkerType(scope)

        # Line number of the marker in the source code.
        self.ng_source_line_begin: Optional[int] = None
        self.ng_source_column_begin: Optional[int] = None

        # Line number of the marker range in the source code:
        # TODO: Improve description.
        # For Begin ranges:
        #   ng_range_line_begin == ng_source_line_begin  # noqa: ERA001
        #   ng_range_line_end == ng_source_line_begin of the End marker  # noqa: ERA001, E501
        # For End ranges:
        #   ng_range_line_begin == ng_range_line_begin of the Begin marker  # noqa: ERA001, E501
        #   ng_range_line_end == ng_source_line_begin  # noqa: ERA001
        self.ng_range_line_begin: Optional[int] = None
        self.ng_range_line_end: Optional[int] = None

        self.ng_marker_line: Optional[int] = None
        self.ng_marker_column: Optional[int] = None

        self.ng_is_nodoc = "nosdoc" in self.reqs

        self._description: Optional[str] = None

    def is_range_marker(self) -> bool:
        return True

    def is_line_marker(self) -> bool:
        return False

    def is_begin(self) -> bool:
        return True

    def is_end(self) -> bool:
        return False

    def get_description(self) -> Optional[str]:
        return self._description

    def set_description(self, description: str) -> None:
        assert isinstance(description, str)
        self._description = description


@auto_described
class ForwardFunctionRangeMarker(FunctionRangeMarker):
    def __init__(self, parent, reqs_objs: List[Req], scope: str):
        super().__init__(parent, reqs_objs, scope)
