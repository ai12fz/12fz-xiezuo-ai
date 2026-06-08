"""Wrapper for the reset-memories command.

Delegates to ``fzxiezuoai.utilities.reset_memories`` when the full fzxiezuoai
package is installed, otherwise prints a helpful error message.
"""

from __future__ import annotations

import click


def reset_memories_command(
    memory: bool,
    knowledge: bool,
    agent_knowledge: bool,
    kickoff_outputs: bool,
    all: bool,
) -> None:
    try:
        from fzxiezuoai.utilities.reset_memories import (
            reset_memories_command as _reset,
        )
    except ImportError:
        click.secho(
            "The 'reset-memories' command requires the full fzxiezuoai package.\n"
            "Install it with: pip install fzxiezuoai",
            fg="red",
        )
        raise SystemExit(1) from None

    _reset(memory, knowledge, agent_knowledge, kickoff_outputs, all)
