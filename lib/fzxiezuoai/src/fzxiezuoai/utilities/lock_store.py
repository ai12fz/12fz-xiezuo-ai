"""Deprecated: use ``fzxiezuoai_core.lock_store`` instead."""

from __future__ import annotations

import warnings

from fzxiezuoai_core.lock_store import lock as lock


__all__ = ["lock"]


warnings.warn(
    "fzxiezuoai.utilities.lock_store is deprecated; import from fzxiezuoai_core.lock_store.",
    DeprecationWarning,
    stacklevel=2,
)
