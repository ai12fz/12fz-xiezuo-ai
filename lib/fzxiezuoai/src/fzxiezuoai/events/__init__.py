"""12FZ协作AI events system for monitoring and extending agent behavior.

This module provides the event infrastructure that allows users to:
- Monitor agent, task, and crew execution
- Track memory operations and performance
- Build custom logging and analytics
- Extend 12FZ协作AI with custom event handlers
- Declare handler dependencies for ordered execution

Event type classes are lazy-loaded on first access to avoid importing
~12 Pydantic model modules (and their transitive deps) at package init time.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from fzxiezuoai.events.base_event_listener import BaseEventListener
from fzxiezuoai.events.depends import Depends
from fzxiezuoai.events.event_bus import crewai_event_bus
from fzxiezuoai.events.handler_graph import CircularDependencyError


if TYPE_CHECKING:
    from fzxiezuoai.events.types.agent_events import (
        AgentEvaluationCompletedEvent,
        AgentEvaluationFailedEvent,
        AgentEvaluationStartedEvent,
        AgentExecutionCompletedEvent,
        AgentExecutionErrorEvent,
        AgentExecutionStartedEvent,
        LiteAgentExecutionCompletedEvent,
        LiteAgentExecutionErrorEvent,
        LiteAgentExecutionStartedEvent,
    )
    from fzxiezuoai.events.types.checkpoint_events import (
        CheckpointBaseEvent,
        CheckpointCompletedEvent,
        CheckpointFailedEvent,
        CheckpointForkBaseEvent,
        CheckpointForkCompletedEvent,
        CheckpointForkStartedEvent,
        CheckpointPrunedEvent,
        CheckpointRestoreBaseEvent,
        CheckpointRestoreCompletedEvent,
        CheckpointRestoreFailedEvent,
        CheckpointRestoreStartedEvent,
        CheckpointStartedEvent,
    )
    from fzxiezuoai.events.types.crew_events import (
        CrewKickoffCompletedEvent,
        CrewKickoffFailedEvent,
        CrewKickoffStartedEvent,
        CrewTestCompletedEvent,
        CrewTestFailedEvent,
        CrewTestResultEvent,
        CrewTestStartedEvent,
        CrewTrainCompletedEvent,
        CrewTrainFailedEvent,
        CrewTrainStartedEvent,
    )
    from fzxiezuoai.events.types.flow_events import (
        ConversationMessageAddedEvent,
        ConversationRouteSelectedEvent,
        FlowCreatedEvent,
        FlowEvent,
        FlowFinishedEvent,
        FlowPlotEvent,
        FlowStartedEvent,
        HumanFeedbackReceivedEvent,
        HumanFeedbackRequestedEvent,
        MethodExecutionFailedEvent,
        MethodExecutionFinishedEvent,
        MethodExecutionStartedEvent,
    )
    from fzxiezuoai.events.types.knowledge_events import (
        KnowledgeQueryCompletedEvent,
        KnowledgeQueryFailedEvent,
        KnowledgeQueryStartedEvent,
        KnowledgeRetrievalCompletedEvent,
        KnowledgeRetrievalStartedEvent,
        KnowledgeSearchQueryFailedEvent,
    )
    from fzxiezuoai.events.types.llm_events import (
        LLMCallCompletedEvent,
        LLMCallFailedEvent,
        LLMCallStartedEvent,
        LLMStreamChunkEvent,
    )
    from fzxiezuoai.events.types.llm_guardrail_events import (
        LLMGuardrailCompletedEvent,
        LLMGuardrailStartedEvent,
    )
    from fzxiezuoai.events.types.logging_events import (
        AgentLogsExecutionEvent,
        AgentLogsStartedEvent,
    )
    from fzxiezuoai.events.types.mcp_events import (
        MCPConfigFetchFailedEvent,
        MCPConnectionCompletedEvent,
        MCPConnectionFailedEvent,
        MCPConnectionStartedEvent,
        MCPToolExecutionCompletedEvent,
        MCPToolExecutionFailedEvent,
        MCPToolExecutionStartedEvent,
    )
    from fzxiezuoai.events.types.memory_events import (
        MemoryQueryCompletedEvent,
        MemoryQueryFailedEvent,
        MemoryQueryStartedEvent,
        MemoryRetrievalCompletedEvent,
        MemoryRetrievalFailedEvent,
        MemoryRetrievalStartedEvent,
        MemorySaveCompletedEvent,
        MemorySaveFailedEvent,
        MemorySaveStartedEvent,
    )
    from fzxiezuoai.events.types.reasoning_events import (
        AgentReasoningCompletedEvent,
        AgentReasoningFailedEvent,
        AgentReasoningStartedEvent,
        ReasoningEvent,
    )
    from fzxiezuoai.events.types.skill_events import (
        SkillActivatedEvent,
        SkillDiscoveryCompletedEvent,
        SkillDiscoveryStartedEvent,
        SkillEvent,
        SkillLoadFailedEvent,
        SkillLoadedEvent,
    )
    from fzxiezuoai.events.types.task_events import (
        TaskCompletedEvent,
        TaskEvaluationEvent,
        TaskFailedEvent,
        TaskStartedEvent,
    )
    from fzxiezuoai.events.types.tool_usage_events import (
        ToolExecutionErrorEvent,
        ToolSelectionErrorEvent,
        ToolUsageErrorEvent,
        ToolUsageEvent,
        ToolUsageFinishedEvent,
        ToolUsageStartedEvent,
        ToolValidateInputErrorEvent,
    )

_LAZY_EVENT_MAPPING: dict[str, str] = {
    "AgentEvaluationCompletedEvent": "fzxiezuoai.events.types.agent_events",
    "AgentEvaluationFailedEvent": "fzxiezuoai.events.types.agent_events",
    "AgentEvaluationStartedEvent": "fzxiezuoai.events.types.agent_events",
    "AgentExecutionCompletedEvent": "fzxiezuoai.events.types.agent_events",
    "AgentExecutionErrorEvent": "fzxiezuoai.events.types.agent_events",
    "AgentExecutionStartedEvent": "fzxiezuoai.events.types.agent_events",
    "LiteAgentExecutionCompletedEvent": "fzxiezuoai.events.types.agent_events",
    "LiteAgentExecutionErrorEvent": "fzxiezuoai.events.types.agent_events",
    "LiteAgentExecutionStartedEvent": "fzxiezuoai.events.types.agent_events",
    "CheckpointBaseEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointCompletedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointFailedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointForkBaseEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointForkCompletedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointForkStartedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointPrunedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointRestoreBaseEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointRestoreCompletedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointRestoreFailedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointRestoreStartedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CheckpointStartedEvent": "fzxiezuoai.events.types.checkpoint_events",
    "CrewKickoffCompletedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewKickoffFailedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewKickoffStartedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTestCompletedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTestFailedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTestResultEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTestStartedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTrainCompletedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTrainFailedEvent": "fzxiezuoai.events.types.crew_events",
    "CrewTrainStartedEvent": "fzxiezuoai.events.types.crew_events",
    "ConversationMessageAddedEvent": "fzxiezuoai.events.types.flow_events",
    "ConversationRouteSelectedEvent": "fzxiezuoai.events.types.flow_events",
    "FlowCreatedEvent": "fzxiezuoai.events.types.flow_events",
    "FlowEvent": "fzxiezuoai.events.types.flow_events",
    "FlowFinishedEvent": "fzxiezuoai.events.types.flow_events",
    "FlowPlotEvent": "fzxiezuoai.events.types.flow_events",
    "FlowStartedEvent": "fzxiezuoai.events.types.flow_events",
    "HumanFeedbackReceivedEvent": "fzxiezuoai.events.types.flow_events",
    "HumanFeedbackRequestedEvent": "fzxiezuoai.events.types.flow_events",
    "MethodExecutionFailedEvent": "fzxiezuoai.events.types.flow_events",
    "MethodExecutionFinishedEvent": "fzxiezuoai.events.types.flow_events",
    "MethodExecutionStartedEvent": "fzxiezuoai.events.types.flow_events",
    "KnowledgeQueryCompletedEvent": "fzxiezuoai.events.types.knowledge_events",
    "KnowledgeQueryFailedEvent": "fzxiezuoai.events.types.knowledge_events",
    "KnowledgeQueryStartedEvent": "fzxiezuoai.events.types.knowledge_events",
    "KnowledgeRetrievalCompletedEvent": "fzxiezuoai.events.types.knowledge_events",
    "KnowledgeRetrievalStartedEvent": "fzxiezuoai.events.types.knowledge_events",
    "KnowledgeSearchQueryFailedEvent": "fzxiezuoai.events.types.knowledge_events",
    "LLMCallCompletedEvent": "fzxiezuoai.events.types.llm_events",
    "LLMCallFailedEvent": "fzxiezuoai.events.types.llm_events",
    "LLMCallStartedEvent": "fzxiezuoai.events.types.llm_events",
    "LLMStreamChunkEvent": "fzxiezuoai.events.types.llm_events",
    "LLMGuardrailCompletedEvent": "fzxiezuoai.events.types.llm_guardrail_events",
    "LLMGuardrailStartedEvent": "fzxiezuoai.events.types.llm_guardrail_events",
    "AgentLogsExecutionEvent": "fzxiezuoai.events.types.logging_events",
    "AgentLogsStartedEvent": "fzxiezuoai.events.types.logging_events",
    "MCPConfigFetchFailedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPConnectionCompletedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPConnectionFailedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPConnectionStartedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPToolExecutionCompletedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPToolExecutionFailedEvent": "fzxiezuoai.events.types.mcp_events",
    "MCPToolExecutionStartedEvent": "fzxiezuoai.events.types.mcp_events",
    "MemoryQueryCompletedEvent": "fzxiezuoai.events.types.memory_events",
    "MemoryQueryFailedEvent": "fzxiezuoai.events.types.memory_events",
    "MemoryQueryStartedEvent": "fzxiezuoai.events.types.memory_events",
    "MemoryRetrievalCompletedEvent": "fzxiezuoai.events.types.memory_events",
    "MemoryRetrievalFailedEvent": "fzxiezuoai.events.types.memory_events",
    "MemoryRetrievalStartedEvent": "fzxiezuoai.events.types.memory_events",
    "MemorySaveCompletedEvent": "fzxiezuoai.events.types.memory_events",
    "MemorySaveFailedEvent": "fzxiezuoai.events.types.memory_events",
    "MemorySaveStartedEvent": "fzxiezuoai.events.types.memory_events",
    "AgentReasoningCompletedEvent": "fzxiezuoai.events.types.reasoning_events",
    "AgentReasoningFailedEvent": "fzxiezuoai.events.types.reasoning_events",
    "AgentReasoningStartedEvent": "fzxiezuoai.events.types.reasoning_events",
    "ReasoningEvent": "fzxiezuoai.events.types.reasoning_events",
    "SkillActivatedEvent": "fzxiezuoai.events.types.skill_events",
    "SkillDiscoveryCompletedEvent": "fzxiezuoai.events.types.skill_events",
    "SkillDiscoveryStartedEvent": "fzxiezuoai.events.types.skill_events",
    "SkillEvent": "fzxiezuoai.events.types.skill_events",
    "SkillLoadFailedEvent": "fzxiezuoai.events.types.skill_events",
    "SkillLoadedEvent": "fzxiezuoai.events.types.skill_events",
    "TaskCompletedEvent": "fzxiezuoai.events.types.task_events",
    "TaskEvaluationEvent": "fzxiezuoai.events.types.task_events",
    "TaskFailedEvent": "fzxiezuoai.events.types.task_events",
    "TaskStartedEvent": "fzxiezuoai.events.types.task_events",
    "ToolExecutionErrorEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolSelectionErrorEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolUsageErrorEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolUsageEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolUsageFinishedEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolUsageStartedEvent": "fzxiezuoai.events.types.tool_usage_events",
    "ToolValidateInputErrorEvent": "fzxiezuoai.events.types.tool_usage_events",
}

_extension_exports: dict[str, Any] = {}


def __getattr__(name: str) -> Any:
    """Lazy import for event types and registered extensions."""
    if name in _LAZY_EVENT_MAPPING:
        module_path = _LAZY_EVENT_MAPPING[name]
        module = importlib.import_module(module_path)
        val = getattr(module, name)
        globals()[name] = val  # cache for subsequent access
        return val

    if name in _extension_exports:
        value = _extension_exports[name]
        if isinstance(value, str):
            module_path, _, attr_name = value.rpartition(".")
            if module_path:
                module = importlib.import_module(module_path)
                return getattr(module, attr_name)
            return importlib.import_module(value)
        return value

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__ = [
    "AgentEvaluationCompletedEvent",
    "AgentEvaluationFailedEvent",
    "AgentEvaluationStartedEvent",
    "AgentExecutionCompletedEvent",
    "AgentExecutionErrorEvent",
    "AgentExecutionStartedEvent",
    "AgentLogsExecutionEvent",
    "AgentLogsStartedEvent",
    "AgentReasoningCompletedEvent",
    "AgentReasoningFailedEvent",
    "AgentReasoningStartedEvent",
    "BaseEventListener",
    "CheckpointBaseEvent",
    "CheckpointCompletedEvent",
    "CheckpointFailedEvent",
    "CheckpointForkBaseEvent",
    "CheckpointForkCompletedEvent",
    "CheckpointForkStartedEvent",
    "CheckpointPrunedEvent",
    "CheckpointRestoreBaseEvent",
    "CheckpointRestoreCompletedEvent",
    "CheckpointRestoreFailedEvent",
    "CheckpointRestoreStartedEvent",
    "CheckpointStartedEvent",
    "CircularDependencyError",
    "ConversationMessageAddedEvent",
    "ConversationRouteSelectedEvent",
    "CrewKickoffCompletedEvent",
    "CrewKickoffFailedEvent",
    "CrewKickoffStartedEvent",
    "CrewTestCompletedEvent",
    "CrewTestFailedEvent",
    "CrewTestResultEvent",
    "CrewTestStartedEvent",
    "CrewTrainCompletedEvent",
    "CrewTrainFailedEvent",
    "CrewTrainStartedEvent",
    "Depends",
    "FlowCreatedEvent",
    "FlowEvent",
    "FlowFinishedEvent",
    "FlowPlotEvent",
    "FlowStartedEvent",
    "HumanFeedbackReceivedEvent",
    "HumanFeedbackRequestedEvent",
    "KnowledgeQueryCompletedEvent",
    "KnowledgeQueryFailedEvent",
    "KnowledgeQueryStartedEvent",
    "KnowledgeRetrievalCompletedEvent",
    "KnowledgeRetrievalStartedEvent",
    "KnowledgeSearchQueryFailedEvent",
    "LLMCallCompletedEvent",
    "LLMCallFailedEvent",
    "LLMCallStartedEvent",
    "LLMGuardrailCompletedEvent",
    "LLMGuardrailStartedEvent",
    "LLMStreamChunkEvent",
    "LiteAgentExecutionCompletedEvent",
    "LiteAgentExecutionErrorEvent",
    "LiteAgentExecutionStartedEvent",
    "MCPConfigFetchFailedEvent",
    "MCPConnectionCompletedEvent",
    "MCPConnectionFailedEvent",
    "MCPConnectionStartedEvent",
    "MCPToolExecutionCompletedEvent",
    "MCPToolExecutionFailedEvent",
    "MCPToolExecutionStartedEvent",
    "MemoryQueryCompletedEvent",
    "MemoryQueryFailedEvent",
    "MemoryQueryStartedEvent",
    "MemoryRetrievalCompletedEvent",
    "MemoryRetrievalFailedEvent",
    "MemoryRetrievalStartedEvent",
    "MemorySaveCompletedEvent",
    "MemorySaveFailedEvent",
    "MemorySaveStartedEvent",
    "MethodExecutionFailedEvent",
    "MethodExecutionFinishedEvent",
    "MethodExecutionStartedEvent",
    "ReasoningEvent",
    "SkillActivatedEvent",
    "SkillDiscoveryCompletedEvent",
    "SkillDiscoveryStartedEvent",
    "SkillEvent",
    "SkillLoadFailedEvent",
    "SkillLoadedEvent",
    "TaskCompletedEvent",
    "TaskEvaluationEvent",
    "TaskFailedEvent",
    "TaskStartedEvent",
    "ToolExecutionErrorEvent",
    "ToolSelectionErrorEvent",
    "ToolUsageErrorEvent",
    "ToolUsageEvent",
    "ToolUsageFinishedEvent",
    "ToolUsageStartedEvent",
    "ToolValidateInputErrorEvent",
    "_extension_exports",
    "crewai_event_bus",
]
