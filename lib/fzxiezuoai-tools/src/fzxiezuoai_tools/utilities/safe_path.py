"""Backward-compatible re-export from fzxiezuoai_tools.security.safe_path."""

from fzxiezuoai_tools.security.safe_path import (
    validate_directory_path,
    validate_file_path,
    validate_url,
)


__all__ = ["validate_directory_path", "validate_file_path", "validate_url"]
