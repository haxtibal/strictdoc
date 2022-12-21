from strictdoc.backend.sdoc.models.type_system import (
    ReferenceType,
    FileEntry,
)


class Reference:
    def __init__(self, ref_type, parent):
        self.parent = parent
        self.ref_type = ref_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"Reference("
            f"parent = {self.parent.field_name},"
            f" ref_type = {self.ref_type})"
        )


class FileReference(Reference):
    def __init__(self, parent, file_entry: FileEntry):
        super().__init__(ReferenceType.FILE, parent)
        self.file_entry = file_entry

    def __str__(self):
        return (
            f"FileReference("
            f"parent = {self.parent.field_name},"
            f" file_entry = {self.file_entry})"
        )


class ParentReqReference(Reference):
    def __init__(self, parent, ref_uid):
        super().__init__(ReferenceType.PARENT, parent)
        self.ref_uid = ref_uid

    def __str__(self):
        return (
            f"ParentReqReference("
            f"parent = {self.parent.field_name},"
            f" ref_uid = {self.ref_uid})"
        )
