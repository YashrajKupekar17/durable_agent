# tools/tool_registry.py
from typing import Any, Callable, Dict
from models.core import ToolArgument, ToolDefinition

# --- Imports ---
from tools.gather_requirements import gather_requirements
from tools.plan_webpage import plan_webpage
from tools.build_structure import build_structure
from tools.build_styles import build_styles
from tools.build_interactivity import build_interactivity
from tools.quality_check import quality_check
from tools.assemble_webpage import assemble_webpage
from tools.save_webpage import save_webpage
from tools.refine_webpage import refine_webpage
from tools.explain_webpage import explain_webpage

# --- Tool Definitions ---

gather_requirements_tool = ToolDefinition(
    name="GatherRequirements",
    description="Structures the user's answers about purpose, audience, vibe, sections, interactivity, colors, and content into a spec. Run this FIRST after asking all discovery questions.",
    arguments=[
        ToolArgument(name="purpose", type="string",
                     description="What the webpage is for (portfolio, landing page, dashboard, blog, etc.)"),
        ToolArgument(name="audience", type="string",
                     description="Who will visit this page (employers, customers, general public, etc.)"),
        ToolArgument(name="vibe", type="string",
                     description="The design feel (minimal, bold, corporate, playful, dark, luxury, etc.)"),
        ToolArgument(name="sections", type="string",
                     description="Comma-separated list of sections needed (hero, about, features, pricing, contact, gallery, etc.)"),
        ToolArgument(name="interactivity", type="string",
                     description="Interactive features needed (contact form, dark mode toggle, carousel, tabs, animations, or 'none')"),
        ToolArgument(name="colorPreferences", type="string",
                     description="Color or font preferences, or 'you decide' to let the agent choose"),
        ToolArgument(name="content", type="string",
                     description="Any real content the user has (text, company name, tagline) or 'use placeholders'"),
    ],
)

plan_webpage_tool = ToolDefinition(
    name="PlanWebpage",
    description="Creates a detailed technical blueprint from the gathered requirements: color palette, typography, layout approach, section breakdown, CSS strategy, animations, and JS features. Infer the 'spec' argument from the GatherRequirements tool result.",
    arguments=[
        ToolArgument(name="spec", type="object",
                     description="The spec object from GatherRequirements result. Infer from conversation history."),
    ],
)

build_structure_tool = ToolDefinition(
    name="BuildStructure",
    description="Writes semantic HTML skeleton from the plan. No styles, no JS — just clean structure with meaningful class names. Infer 'plan' and 'spec' from previous tool results.",
    arguments=[
        ToolArgument(name="plan", type="object",
                     description="The plan object from PlanWebpage result. Infer from conversation history."),
        ToolArgument(name="spec", type="object",
                     description="The spec object from GatherRequirements result. Infer from conversation history."),
    ],
)

build_styles_tool = ToolDefinition(
    name="BuildStyles",
    description="Writes complete responsive CSS from the plan and HTML structure. Infer 'html' and 'plan' from previous tool results.",
    arguments=[
        ToolArgument(name="html", type="string",
                     description="The HTML from BuildStructure result. Infer from conversation history."),
        ToolArgument(name="plan", type="object",
                     description="The plan from PlanWebpage result. Infer from conversation history."),
    ],
)

build_interactivity_tool = ToolDefinition(
    name="BuildInteractivity",
    description="Writes vanilla JS for interactive features specified in the plan. If no JS features needed, returns empty. Infer 'html' and 'plan' from previous tool results.",
    arguments=[
        ToolArgument(name="html", type="string",
                     description="The HTML from BuildStructure result. Infer from conversation history."),
        ToolArgument(name="plan", type="object",
                     description="The plan from PlanWebpage result. Infer from conversation history."),
    ],
)

quality_check_tool = ToolDefinition(
    name="QualityCheck",
    description="Reviews HTML + CSS + JS for issues (broken class refs, missing accessibility, mobile problems) and auto-fixes them. Infer all args from previous tool results.",
    arguments=[
        ToolArgument(name="html", type="string",
                     description="The HTML from BuildStructure. Infer from conversation history."),
        ToolArgument(name="css", type="string",
                     description="The CSS from BuildStyles. Infer from conversation history."),
        ToolArgument(name="js", type="string",
                     description="The JS from BuildInteractivity (or empty string if none). Infer from conversation history."),
    ],
)

assemble_webpage_tool = ToolDefinition(
    name="AssembleWebpage",
    description="Combines HTML + CSS + JS into a single .html file. Infer all args from QualityCheck result (it returns the final html, css, js).",
    arguments=[
        ToolArgument(name="html", type="string",
                     description="The final HTML from QualityCheck. Infer from conversation history."),
        ToolArgument(name="css", type="string",
                     description="The final CSS from QualityCheck. Infer from conversation history."),
        ToolArgument(name="js", type="string",
                     description="The final JS from QualityCheck (or empty string). Infer from conversation history."),
    ],
)

save_webpage_tool = ToolDefinition(
    name="SaveWebpage",
    description="Saves the assembled HTML webpage to a file and returns a preview URL.",
    arguments=[
        ToolArgument(name="htmlContent", type="string",
                     description="The full assembled HTML content from AssembleWebpage. Infer from conversation history."),
        ToolArgument(name="filename", type="string",
                     description="A short, descriptive filename (e.g. 'portfolio.html'). Ask the user for this."),
    ],
)

refine_webpage_tool = ToolDefinition(
    name="RefineWebpage",
    description="Applies targeted changes to an existing webpage. For refinements, identify which layer (structure/styles/interactivity) needs updating. Use after user previews and wants changes.",
    arguments=[
        ToolArgument(name="currentHtml", type="string",
                     description="The current full HTML content. Infer from the last AssembleWebpage or SaveWebpage result."),
        ToolArgument(name="refinement", type="string",
                     description="Description of the changes the user wants."),
    ],
)

explain_webpage_tool = ToolDefinition(
    name="ExplainWebpage",
    description="Explains how part of the webpage works in simple terms.",
    arguments=[
        ToolArgument(name="htmlContent", type="string",
                     description="The current HTML content. Infer from conversation history."),
        ToolArgument(name="question", type="string",
                     description="The user's specific question about the webpage."),
    ],
)

# --- Handler Registry ---
TOOL_HANDLERS: Dict[str, Callable[..., Any]] = {
    "GatherRequirements": gather_requirements,
    "PlanWebpage": plan_webpage,
    "BuildStructure": build_structure,
    "BuildStyles": build_styles,
    "BuildInteractivity": build_interactivity,
    "QualityCheck": quality_check,
    "AssembleWebpage": assemble_webpage,
    "SaveWebpage": save_webpage,
    "RefineWebpage": refine_webpage,
    "ExplainWebpage": explain_webpage,
}

def get_handler(tool_name: str) -> Callable[..., Any]:
    if tool_name not in TOOL_HANDLERS:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_HANDLERS[tool_name]
