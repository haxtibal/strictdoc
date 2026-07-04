from typing import Optional, Protocol, Type

from strictdoc.backend.markdown.reader import SDMarkdownReader
from strictdoc.backend.sdoc.models.document import SDocDocument
from strictdoc.backend.sdoc.reader import SDReader


class DocumentReaderProtocol(Protocol):
    @staticmethod
    def post_grammar_hook(document: SDocDocument) -> None:
        """Readers implement grammar dependent parsing fixups here. Called by framework after grammar is available."""
        ...


class DocumentReaderRegistry:
    @staticmethod
    def get_reader_class(
        path_to_file: str,
    ) -> Optional[Type[DocumentReaderProtocol]]:
        if path_to_file.endswith(".sdoc"):
            return SDReader
        if path_to_file.endswith((".md", ".markdown")):
            return SDMarkdownReader
        return None
