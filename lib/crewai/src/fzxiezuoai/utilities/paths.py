"""Deprecated: use ``fzxiezuoai_core.paths`` instead."""

from __future__ import annotations

import warnings

from fzxiezuoai_core.paths import (
    db_storage_path as db_storage_path,
    get_project_directory_name as get_project_directory_name,
)


__all__ = ["db_storage_path", "get_project_directory_name"]


warnings.warn(
    "fzxiezuoai.utilities.paths is deprecated; import from fzxiezuoai_core.paths.",
    DeprecationWarning,
    stacklevel=2,
)
