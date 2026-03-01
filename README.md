# Temporal AI Agent — Durable Webpage Builder

A learning project exploring how to build **durable AI agents** using [Temporal](https://temporal.io/). The agent builds webpages through a structured conversation — asking questions, planning, generating HTML/CSS/JS through specialized tools, and refining based on feedback. All orchestrated as a Temporal workflow, so it survives crashes, retries failures, and maintains state automatically.

> **Note:** This is a learning/experimental project. It works end-to-end but has rough edges — the goal was to understand Temporal's workflow orchestration, not to ship a production app.

## What I Learned

- **Temporal Workflows** — long-running, stateful orchestration with signals and queries
- **Activities** — wrapping LLM calls and tool executions as retryable units of work
- **Dynamic Activities** — routing tool execution by name at runtime
- **Signals & Queries** — real-time communication between the API/frontend and the workflow
- **Durability** — the workflow picks up exactly where it left off after a crash

## How It Works

```
Frontend (React) <-> FastAPI <-> Temporal Workflow
                                      |
                                 LLM Planner (picks next tool)
                                      |
                     +----------------+----------------+
                     |        |       |       |        |
               GatherReqs  Plan  BuildHTML BuildCSS  BuildJS
                     |        |       |       |        |
                     +--------+-------+-------+--------+
                                      |
                                 QualityCheck -> Assemble -> Save -> Preview
                                      |
                                 Refine Loop (user feedback)
```

1. User describes what they want
2. Agent asks discovery questions (audience, vibe, sections, interactivity, colors, content)
3. Tools run in sequence: requirements -> plan -> HTML -> CSS -> JS -> QA -> assemble -> save
4. User previews in an inline iframe and requests changes
5. Refine loop until satisfied

## Tech Stack

- **Temporal** — workflow orchestration and durability
- **FastAPI** — API layer with signals/queries to Temporal
- **LiteLLM** — LLM abstraction (works with OpenAI, Gemini, Anthropic, etc.)
- **React + Vite** — frontend with polling-based chat UI
- **Jinja2** — prompt templating

## Project Structure

```
temporal-ai-agent/
  activities/       # LLM calls and tool execution (Temporal activities)
  api/              # FastAPI server
  frontend/         # React chat UI
  models/           # Data models (ToolDefinition, AgentGoal, etc.)
  prompts/          # Jinja2 prompt templates
  tools/            # Tool implementations (each is a specialist)
  workflows/        # Temporal workflow definition
  worker/           # Temporal worker process
  generated_pages/  # Output HTML files
```

## Running It

**Prerequisites:** Python 3.9+, Node.js, Temporal server running locally.

```bash
# 1. Start Temporal (if not running)
temporal server start-dev

# 2. Set up environment
cp .env.example .env  # add your LLM_KEY and LLM_MODEL

# 3. Start the worker
python -m worker.worker

# 4. Start the API
uvicorn api.main:app --reload

# 5. Start the frontend
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173` and start chatting.

## .env Config

```env
LLM_MODEL=openai/gpt-4o          # or gemini/gemini-2.0-flash, anthropic/claude-sonnet-4-20250514
LLM_KEY=your-api-key
SHOW_CONFIRM=True                  # require user confirmation before each tool runs
TEMPORAL_ADDRESS=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=agent-task-queue
```
