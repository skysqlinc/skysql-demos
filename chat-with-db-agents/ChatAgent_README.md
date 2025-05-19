# Chat with SkySQL Semantic DB Agents

The examples here demonstrate how one can use SkySQL DB agents as tools within popular GenAI Frameworks  - LangChain, LlamaIndex and CrewAI. 

### Why use SkySQL DB Agents ? 
While it is possible to generate SQL given some schema description to a LLM or use APIs in frameworks, it is rather challenging to generate accurate SQL for real world DBs with high complexity. You need the correct context, allow humans to add missing semantic information, store some relevant context in Vector stores and more. 
SkySQL DB Agents provides a No-Code UI to autonomously learn the DB context. It is also secure and reliable. 

### Why integrate with AI frameworks
SkySQL provides "DB level" Agents. Your application may still need to work with disparate other sources, have its own orchestration across multiple agents and so on. 
Moreover, a high level agent often improves the quality of the responses. It will rewrite the user question to be more appropriate and synthesize good results. 

## Examples here
The Simple examples here provide a conversational agent that can interact with backend database agents to answer your queries, show SQL, and suggest next steps. You can use it as a web app (Streamlit) or from the command line.

---

## Setup Instructions

### 1. Clone the Repository
Clone or download this(?) repository to your local machine.

### 2. Install Python (if needed)
Ensure you have Python 3.8 or newer installed. You can check with:
```sh
python --version
```

### 3. Create a Virtual Environment (Recommended)
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Requirements
Install all dependencies:
```sh
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
- You need both the [SkySQL API Key](https://app.skysql.com/user-profile/api-keys) and the [OpenAI API key](https://platform.openai.com/api-keys)

Add these to a .env file or set it. 

```sh
export OPENAI_API_KEY = "sk-Upwxj2mlvm......"
export SKYSQL_API_KEY = "skysql.1zzz......"
```

---

## Running the App

### Option 1: Run the Streamlit Web App
From the `chat-with-db-agents` directory, run:
```sh
streamlit run db_chat_streamlit_app.py
```
- Open the provided local URL in your browser.
- Chat with the agent in the web UI.

### Option 2: Run the CLI Version

You can try the CLI agent using any of the following frameworks:

**LlamaIndex:**
```sh
python db_chat_agent.py
```

**LangGraph:**
```sh
python db_chat_agent_langgraph.py
```

**CrewAI:**
```sh
python db_chat_agent_crewai.py
```

- Interact with the agent in your terminal.
- All versions support listing available DB agents, chatting with them, and showing SQL for transparency.

---

## Features
- Uses OpenAI LLM and backend DB agents.
- Lists available DB agents and chats with them.
- Synthesizes responses, includes SQL, and suggests follow-up questions.
- Works as both a web app and CLI.

---

## Troubleshooting
- Ensure your API keys are correct and active.
- If you see missing package errors, re-run `pip install -r requirements.txt`.
- For Streamlit issues, try upgrading: `pip install --upgrade streamlit`.

---

## Credits
- Built with [SkySQL](https://skysql.com), [Streamlit](https://streamlit.io/), [LangGraph](https://github.com/langchain-ai/langgraph), and [LangChain](https://github.com/langchain-ai/langchain). 
