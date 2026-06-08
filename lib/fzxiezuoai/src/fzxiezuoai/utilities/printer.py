"""Deprecated: use ``fzxiezuoai_core.printer`` instead."""

from __future__ import annotations

import warnings

from fzxiezuoai_core.printer import (
    PRINTER as PRINTER,
    ColoredText as ColoredText,
    Printer as Printer,
    PrinterColor as PrinterColor,
)


__all__ = ["PRINTER", "ColoredText", "Printer", "PrinterColor"]


warnings.warn(
    "fzxiezuoai.utilities.printer is deprecated; import from fzxiezuoai_core.printer.",
    DeprecationWarning,
    stacklevel=2,
)
