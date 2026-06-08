from fzxiezuoai.events.types.a2a_events import (
    A2AAgentCardFetchedEvent,
    A2AArtifactReceivedEvent,
    A2AAuthenticationFailedEvent,
    A2AConnectionErrorEvent,
    A2AConversationCompletedEvent,
    A2AConversationStartedEvent,
    A2ADelegationCompletedEvent,
    A2ADelegationStartedEvent,
    A2AMessageSentEvent,
    A2AParallelDelegationCompletedEvent,
    A2AParallelDelegationStartedEvent,
    A2APollingStartedEvent,
    A2APollingStatusEvent,
    A2APushNotificationReceivedEvent,
    A2APushNotificationRegisteredEvent,
    A2APushNotificationSentEvent,
    A2APushNotificationTimeoutEvent,
    A2AResponseReceivedEvent,
    A2AServerTaskCanceledEvent,
    A2AServerTaskCompletedEvent,
    A2AServerTaskFailedEvent,
    A2AServerTaskStartedEvent,
    A2AStreamingChunkEvent,
    A2AStreamingStartedEvent,
)
from fzxiezuoai.events.types.agent_events import (
    AgentExecutionCompletedEvent,
    AgentExecutionErrorEvent,
    AgentExecutionStartedEvent,
    LiteAgentExecutionCompletedEvent,
)
from fzxiezuoai.events.types.checkpoint_events import (
    CheckpointCompletedEvent,
    CheckpointFailedEvent,
    CheckpointForkCompletedEvent,
    CheckpointForkStartedEvent,
    CheckpointPrunedEvent,
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
    CrewTestStartedEvent,
    CrewTrainCompletedEvent,
    CrewTrainFailedEvent,
    CrewTrainStartedEvent,
)
from fzxiezuoai.events.types.flow_events import (
    ConversationMessageAddedEvent,
    ConversationRouteSelectedEvent,
    FlowFinishedEvent,
    FlowStartedEvent,
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
)
from fzxiezuoai.events.types.task_events import (
    TaskCompletedEvent,
    TaskFailedEvent,
    TaskStartedEvent,
)
from fzxiezuoai.events.types.tool_usage_events import (
    ToolUsageErrorEvent,
    ToolUsageFinishedEvent,
    ToolUsageStartedEvent,
)


EventTypes = (
    A2AAgentCardFetchedEvent
    | A2AArtifactReceivedEvent
    | A2AAuthenticationFailedEvent
    | A2AConnectionErrorEvent
    | A2AConversationCompletedEvent
    | A2AConversationStartedEvent
    | A2ADelegationCompletedEvent
    | A2ADelegationStartedEvent
    | A2AMessageSentEvent
    | A2APollingStartedEvent
    | A2APollingStatusEvent
    | A2APushNotificationReceivedEvent
    | A2APushNotificationRegisteredEvent
    | A2APushNotificationSentEvent
    | A2APushNotificationTimeoutEvent
    | A2AResponseReceivedEvent
    | A2AServerTaskCanceledEvent
    | A2AServerTaskCompletedEvent
    | A2AServerTaskFailedEvent
    | A2AServerTaskStartedEvent
    | A2AStreamingChunkEvent
    | A2AStreamingStartedEvent
    | A2AParallelDelegationStartedEvent
    | A2AParallelDelegationCompletedEvent
    | CrewKickoffStartedEvent
    | CrewKickoffCompletedEvent
    | CrewKickoffFailedEvent
    | CrewTestStartedEvent
    | CrewTestCompletedEvent
    | CrewTestFailedEvent
    | CrewTrainStartedEvent
    | CrewTrainCompletedEvent
    | CrewTrainFailedEvent
    | AgentExecutionStartedEvent
    | AgentExecutionCompletedEvent
    | LiteAgentExecutionCompletedEvent
    | TaskStartedEvent
    | TaskCompletedEvent
    | TaskFailedEvent
    | ConversationMessageAddedEvent
    | ConversationRouteSelectedEvent
    | FlowStartedEvent
    | FlowFinishedEvent
    | MethodExecutionStartedEvent
    | MethodExecutionFinishedEvent
    | MethodExecutionFailedEvent
    | AgentExecutionErrorEvent
    | ToolUsageFinishedEvent
    | ToolUsageErrorEvent
    | ToolUsageStartedEvent
    | LLMCallStartedEvent
    | LLMCallCompletedEvent
    | LLMCallFailedEvent
    | LLMStreamChunkEvent
    | LLMGuardrailStartedEvent
    | LLMGuardrailCompletedEvent
    | AgentReasoningStartedEvent
    | AgentReasoningCompletedEvent
    | AgentReasoningFailedEvent
    | KnowledgeRetrievalStartedEvent
    | KnowledgeRetrievalCompletedEvent
    | KnowledgeQueryStartedEvent
    | KnowledgeQueryCompletedEvent
    | KnowledgeQueryFailedEvent
    | KnowledgeSearchQueryFailedEvent
    | MemorySaveStartedEvent
    | MemorySaveCompletedEvent
    | MemorySaveFailedEvent
    | MemoryQueryStartedEvent
    | MemoryQueryCompletedEvent
    | MemoryQueryFailedEvent
    | MemoryRetrievalStartedEvent
    | MemoryRetrievalCompletedEvent
    | MemoryRetrievalFailedEvent
    | MCPConnectionStartedEvent
    | MCPConnectionCompletedEvent
    | MCPConnectionFailedEvent
    | MCPToolExecutionStartedEvent
    | MCPToolExecutionCompletedEvent
    | MCPToolExecutionFailedEvent
    | MCPConfigFetchFailedEvent
    | CheckpointStartedEvent
    | CheckpointCompletedEvent
    | CheckpointFailedEvent
    | CheckpointForkStartedEvent
    | CheckpointForkCompletedEvent
    | CheckpointRestoreStartedEvent
    | CheckpointRestoreCompletedEvent
    | CheckpointRestoreFailedEvent
    | CheckpointPrunedEvent
)
