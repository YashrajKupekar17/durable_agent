import copy
import json
from typing import Optional

from models.core import AgentGoal
from models.requests import ConversationHistory, ToolData
from prompts.prompts import (
    GENAI_PROMPT,
    MISSING_ARGS_PROMPT,
    TOOL_COMPLETION_PROMPT,
    TOOLCHAIN_COMPLETE_GUIDANCE_PROMPT,
)

# Keys whose values are large code blobs the LLM planner doesn't need in full
_LARGE_KEYS = {"html", "css", "js", "html_content", "htmlContent", "currentHtml",
               "fixedHtml", "fixedCss", "fixedJs"}
_TRUNCATE_LIMIT = 200  # chars to keep as preview


def _truncate_large_values(obj, depth=0):
    """Recursively truncate large code values so the LLM prompt stays within TPM limits."""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if k in _LARGE_KEYS and isinstance(v, str) and len(v) > _TRUNCATE_LIMIT:
                result[k] = v[:_TRUNCATE_LIMIT] + f"... [truncated, {len(v)} chars total]"
            else:
                result[k] = _truncate_large_values(v, depth + 1)
        return result
    elif isinstance(obj, list):
        return [_truncate_large_values(item, depth + 1) for item in obj]
    return obj


def generate_genai_prompt(
    agent_goal: AgentGoal,
    conversation_history: ConversationHistory,
    raw_json: Optional[ToolData] = None,
) -> str:
    """
    Generates a concise prompt for producing or validating JSON instructions
    with the provided tools and conversation history.
    """

    # Truncate large code blobs so the prompt fits within TPM limits
    trimmed_history = _truncate_large_values(copy.deepcopy(conversation_history))

    # Prepare template variables
    template_vars = {
        "agent_goal": agent_goal,
        "conversation_history_json": json.dumps(trimmed_history, indent=2),
        "toolchain_complete_guidance": TOOLCHAIN_COMPLETE_GUIDANCE_PROMPT,
        "raw_json": raw_json,
        "raw_json_str": (
            json.dumps(raw_json, indent=2) if raw_json is not None else None
        ),
    }

    return GENAI_PROMPT.render(**template_vars)


def generate_tool_completion_prompt(current_tool: str, dynamic_result: dict) -> str:
    """
    Generates a prompt for handling tool completion and determining next steps.

    Args:
        current_tool: The name of the tool that just completed
        dynamic_result: The result data from the tool execution

    Returns:
        str: A formatted prompt string for the agent to process the tool completion
    """
    trimmed_result = _truncate_large_values(dynamic_result)
    return TOOL_COMPLETION_PROMPT.format(
        current_tool=current_tool, dynamic_result=trimmed_result
    )


def generate_missing_args_prompt(
    current_tool: str, tool_data: dict, missing_args: list[str]
) -> str:
    """
    Generates a prompt for handling missing arguments for a tool.

    Args:
        current_tool: The name of the tool that needs arguments
        tool_data: The current tool data containing the response
        missing_args: List of argument names that are missing

    Returns:
        str: A formatted prompt string for requesting missing arguments
    """
    return MISSING_ARGS_PROMPT.format(
        response=tool_data.get("response"),
        current_tool=current_tool,
        missing_args=missing_args,
    )