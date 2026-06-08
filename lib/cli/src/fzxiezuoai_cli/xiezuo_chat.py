"""Wrapper for the xiezuo chat command.

Delegates to ``fzxiezuoai.utilities.xiezuo_chat.run_chat`` when the full fzxiezuoai
package is installed, otherwise prints a helpful error message.
"""

from __future__ import annotations

import click


def run_chat() -> None:
    try:
        from fzxiezuoai.utilities.xiezuo_chat import run_chat as _run_chat
    except ImportError:
        click.secho(
            "The 'chat' command requires the full fzxiezuoai package.\n"
            "Install it with: pip install fzxiezuoai",
            fg="red",
        )
        raise SystemExit(1) from None

    _run_chat()
