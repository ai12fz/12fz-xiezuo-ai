"""Deprecated: use ``fzxiezuoai_core.token_manager`` instead."""

from __future__ import annotations

import warnings

from fzxiezuoai_core.token_manager import TokenManager as TokenManager


__all__ = ["TokenManager"]


warnings.warn(
    "fzxiezuoai.auth.token_manager is deprecated; import from fzxiezuoai_core.token_manager.",
    DeprecationWarning,
    stacklevel=2,
)
