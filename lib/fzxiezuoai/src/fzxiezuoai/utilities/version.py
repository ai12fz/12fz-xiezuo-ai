"""Deprecated: use ``fzxiezuoai_core.version`` instead."""

from __future__ import annotations

import warnings

from fzxiezuoai_core.version import get_fzxiezuoai_version as get_fzxiezuoai_version


__all__ = ["get_fzxiezuoai_version"]


warnings.warn(
    "fzxiezuoai.utilities.version is deprecated; import from fzxiezuoai_core.version.",
    DeprecationWarning,
    stacklevel=2,
)
