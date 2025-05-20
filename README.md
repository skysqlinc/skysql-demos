# skysql-demos

This repository contains demo applications showcasing SkySQL technologies and integrations with modern GenAI frameworks.

## Contents

### 1. Chat with SkySQL Database Agents

A collection of examples demonstrating how to use SkySQL DB agents as tools within popular GenAI frameworks such as LangChain, LlamaIndex, and CrewAI.

## Features
- Interact with SkySQL-powered database agents via web or CLI
- Generate and view SQL queries for your questions
- Integrate with OpenAI LLMs for natural language understanding
- List available DB agents and chat with them
- Works with multiple GenAI frameworks

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/skysqlinc/skysql-demos
   cd skysql-demos/chat-with-db-agents
   ```
2. (Recommended) Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set Up Environment Variables
- You need both the [SkySQL API Key](https://app.skysql.com/user-profile/api-keys) and the [OpenAI API key](https://platform.openai.com/api-keys)

Add these to a `.env` file or set it. 

```sh
export OPENAI_API_KEY = "sk-Upwxj2mlvm......"
export SKYSQL_API_KEY = "skysql.1zzz......"
```

Follow detailed instructions, troubleshooting, and feature descriptions, see [`chat-with-db-agents/README.md`](chat-with-db-agents/README.md).
