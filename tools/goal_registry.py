# tools/goal_registry.py
import tools.tool_registry as tool_registry
from models.core import AgentGoal

goal_webpage_builder = AgentGoal(
    id="webpage_builder",
    category_tag="web",
    agent_friendly_description="Build high-quality webpages through structured discovery and specialized agents",
    agent_name="Webpage Builder",
    tools=[
        tool_registry.gather_requirements_tool,
        tool_registry.plan_webpage_tool,
        tool_registry.build_structure_tool,
        tool_registry.build_styles_tool,
        tool_registry.build_interactivity_tool,
        tool_registry.quality_check_tool,
        tool_registry.assemble_webpage_tool,
        tool_registry.save_webpage_tool,
        tool_registry.refine_webpage_tool,
        tool_registry.explain_webpage_tool,
    ],
    description=(
        "Build a high-quality webpage through a structured process: "
        "PHASE 1 — DISCOVERY: After the user says what they want, ask ALL of the following in a SINGLE message "
        "as a numbered list: "
        "(1) Who is the audience? "
        "(2) What's the vibe/feel? (minimal, bold, corporate, playful, dark, luxury, etc.) "
        "(3) What sections do you need? (hero, about, features, pricing, contact, gallery, etc.) "
        "(4) Any interactivity? (contact form, dark mode toggle, carousel, tabs, animations, or none) "
        "(5) Color/font preferences? (or 'you decide') "
        "(6) Any content ready? (business name, tagline, text — or 'use placeholders') "
        "Wait for ONE reply with all answers, then proceed to Phase 2. "
        "PHASE 2 — BUILDING: Run tools in this exact sequence: "
        "1. GatherRequirements: Structure the collected answers into a spec. "
        "2. PlanWebpage: Create a technical blueprint from the spec. "
        "3. BuildStructure: Write semantic HTML skeleton from the plan. "
        "4. BuildStyles: Write complete responsive CSS. "
        "5. BuildInteractivity: Write vanilla JS for interactive features (skip if none needed). "
        "6. QualityCheck: Review all pieces for issues and fix them. "
        "7. AssembleWebpage: Combine HTML + CSS + JS into one file. "
        "8. SaveWebpage: Save and show preview URL. "
        "PHASE 3 — REFINEMENT: After preview, ALWAYS ask what to change. "
        "For changes, use RefineWebpage on the assembled HTML, then SaveWebpage again. "
        "Never set next='done' unless user explicitly says they are satisfied."
    ),
    starter_prompt=(
        "Welcome me warmly. Tell me you can build beautiful, production-quality webpages "
        "through a structured process. Ask: What kind of webpage would you like to build? "
        "(portfolio, landing page, dashboard, blog, product page, or something else?)"
    ),
    example_conversation_history="\n".join([
        "agent: Welcome! I build production-quality webpages. What kind of page would you like?",
        "user: A landing page for my coffee shop",
        "agent: Great choice! To build this perfectly, I need a few details. Please answer all of these:\n"
        "1. Who is the audience? (local customers, tourists, general public, etc.)\n"
        "2. What's the vibe? (minimal, cozy, bold, modern, luxury, etc.)\n"
        "3. What sections do you need? (hero, about, menu, contact, gallery, etc.)\n"
        "4. Any interactivity? (contact form, image carousel, dark mode toggle, animations, or none)\n"
        "5. Color/font preferences? (or say 'you decide')\n"
        "6. Any content ready? (business name, tagline, menu items — or 'use placeholders')",
        "user: 1. Local customers 2. Warm and cozy 3. Hero, about us, menu highlights, contact 4. Contact form and smooth scroll 5. Warm browns and cream, you pick fonts 6. Name is 'Bean & Brew', tagline 'Your neighborhood coffee spot', placeholders for the rest",
        "agent: Perfect, let's lock in your requirements and start building!",
        "user_confirmed_tool_run: <confirm GatherRequirements>",
        "tool_result: { 'status': 'requirements_gathered', 'spec': {...} }",
        "user_confirmed_tool_run: <confirm PlanWebpage>",
        "tool_result: { 'status': 'planned', 'plan': {...} }",
        "user_confirmed_tool_run: <confirm BuildStructure>",
        "tool_result: { 'status': 'structure_built', 'html': '...' }",
        "user_confirmed_tool_run: <confirm BuildStyles>",
        "tool_result: { 'status': 'styles_built', 'css': '...' }",
        "user_confirmed_tool_run: <confirm BuildInteractivity>",
        "tool_result: { 'status': 'interactivity_built', 'js': '...' }",
        "user_confirmed_tool_run: <confirm QualityCheck>",
        "tool_result: { 'status': 'checked', 'passed': true }",
        "user_confirmed_tool_run: <confirm AssembleWebpage>",
        "tool_result: { 'status': 'assembled', 'html_content': '...' }",
        "user_confirmed_tool_run: <confirm SaveWebpage>",
        "tool_result: { 'previewUrl': 'http://localhost:8000/preview/bean-and-brew.html' }",
        "agent: Here's your preview! Would you like to change anything?",
        "user: Make the hero section taller and buttons rounder",
        "user_confirmed_tool_run: <confirm RefineWebpage>",
        "tool_result: { 'status': 'refined', 'html_content': '...' }",
        "user_confirmed_tool_run: <confirm SaveWebpage>",
        "tool_result: { 'previewUrl': 'http://localhost:8000/preview/bean-and-brew.html' }",
        "agent: Updated! Anything else to tweak?",
        "user: Looks perfect, I'm done",
    ]),
)
