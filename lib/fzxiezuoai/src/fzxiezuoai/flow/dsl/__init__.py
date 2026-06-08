"""Flow DSL: the Python authoring layer for Flows.

Provides the ``@start`` / ``@listen`` / ``@router`` decorators and the
``or_`` / ``and_`` condition combinators used to write Flow classes in
Python. The DSL is one way to produce a Flow Structure: this package
extracts a :class:`~fzxiezuoai.flow.flow_definition.FlowDefinition` from a
Python Flow class. Execution is handled by ``runtime``.
"""

from fzxiezuoai.flow.dsl._conditions import and_, or_
from fzxiezuoai.flow.dsl._human_feedback import (
    HumanFeedbackResult,
    human_feedback,
)
from fzxiezuoai.flow.dsl._listen import listen
from fzxiezuoai.flow.dsl._router import router
from fzxiezuoai.flow.dsl._start import start
from fzxiezuoai.flow.dsl._utils import (
    build_flow_definition as build_flow_definition,
    extract_flow_definition as extract_flow_definition,
)


__all__ = [
    "HumanFeedbackResult",
    "and_",
    "human_feedback",
    "listen",
    "or_",
    "router",
    "start",
]
