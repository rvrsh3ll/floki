from floki.workflow.orchestrators.llm.state import PlanStep
from floki.types.message import BaseMessage
from floki.llm.utils import StructureHandler
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import json

class AgentTaskResponse(BaseMessage):
    """
    Represents a response message from an agent after completing a task.
    """

class TriggerAction(BaseModel):
    """
    Represents a message used to trigger an agent's activity within the workflow.
    """
    task: Optional[str] = Field(None, description="The specific task to execute. If not provided, the agent can act based on its memory or predefined behavior.")
    iteration: Optional[int] = Field(default=0, description="The current iteration of the workflow loop.")

class NextStep(BaseModel):
    """
    Represents the next step in a workflow, including the next agent to respond,
    an instruction message for that agent and the step id and substep id if applicable.
    """
    next_agent: str = Field(..., description="The name of the agent selected to respond next.")
    instruction: str = Field(..., description="A direct message instructing the agent on their next action.")
    step: int = Field(..., description="The step number the agent will be working on.")
    substep: Optional[float] = Field(None, description="The substep number (if applicable) the agent will be working on.")

class TaskPlan(BaseModel):
    """Encapsulates the structured execution plan."""
    plan: List[PlanStep] = Field(..., description="Structured execution plan.")

class PlanStatusUpdate(BaseModel):
    step: int = Field(..., description="Step identifier (integer).")
    substep: Optional[float] = Field(None, description="Substep identifier (float, e.g., 1.1, 2.3). Set to None if updating a step.")
    status: Literal["not_started", "in_progress", "blocked", "completed"] = Field(..., description="Updated status for the step or sub-step.")

class ProgressCheckOutput(BaseModel):
    verdict: Literal["continue", "completed", "failed"] = Field(..., description="Task status: 'continue' (in progress), 'completed' (done), or 'failed' (unresolved issue).")
    plan_needs_update: bool = Field(..., description="Indicates whether the plan requires updates (true/false).")
    plan_status_update: Optional[List[PlanStatusUpdate]] = Field(None, description="List of status updates for steps or sub-steps. Each entry must contain `step`, optional `substep`, and `status`.")
    plan_restructure: Optional[List[PlanStep]] = Field(None, description="A list of restructured steps. Only one step should be modified at a time.")

# Schemas used in Prompts
PLAN_SCHEMA = json.dumps(StructureHandler.enforce_strict_json_schema(TaskPlan.model_json_schema())["properties"]["plan"])
PROGRESS_CHECK_SCHEMA = json.dumps(StructureHandler.enforce_strict_json_schema(ProgressCheckOutput.model_json_schema()))
NEXT_STEP_SCHEMA = json.dumps(NextStep.model_json_schema())