"""File resolution logic."""

from fzxiezuoai_files.resolution.resolver import FileResolver
from fzxiezuoai_files.resolution.utils import (
    is_file_source,
    normalize_input_files,
    wrap_file_source,
)


__all__ = [
    "FileResolver",
    "is_file_source",
    "normalize_input_files",
    "wrap_file_source",
]
