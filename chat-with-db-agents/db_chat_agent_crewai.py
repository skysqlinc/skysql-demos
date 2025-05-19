import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool

# --- Load API keys from .env file ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SKYSQL_API_KEY = os.getenv("SKYSQL_API_KEY")

if not OPENAI_API_KEY or not SKYSQL_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY or SKYSQL_API_KEY in environment or .env file")

SKYSQL_API_URL = "https://api.skysql.com"

# --- Tool 1: List DB Agents ---
@tool("list_db_agents")
def list_db_agents() -> str:
    """Lists available DB agents."""
    response = requests.get(
        f"{SKYSQL_API_URL}/copilot/v1/agent/",
        headers={"X-API-Key": SKYSQL_API_KEY, "Content-Type": "application/json"}
    )
    response.raise_for_status()
    agents = response.json()
    return "\n".join([f"{a['id']}: {a['name']} - {a['description']}" for a in agents])

# --- Tool 2: Chat with a DB Agent ---
@tool("chat_with_db_agent")
def chat_with_db_agent(agent_id: str, prompt: str) -> str:
    """Send a user prompt to a specific DB agent ID and return the response, including SQL if present."""
    response = requests.post(
        f"{SKYSQL_API_URL}/copilot/v1/chat/",
        headers={"X-API-Key": SKYSQL_API_KEY, "Content-Type": "application/json"},
        json={"prompt": prompt, "agent_id": agent_id}
    )
    response.raise_for_status()
    result = response.json()
    resp = result.get("response", {})
    content = resp.get("content") or resp.get("error_text", "No response")
    sql = resp.get("sql_text")
    if sql:
        return f"""{content}\n\n**SQL:**\n```
{sql}
```"""
    return content

# --- Agent Definition ---
db_chat_agent = Agent(
    role="Database Chat Agent",
    goal="Help users interact with backend database agents to answer queries, discover agents, and provide SQL transparency.",
    backstory=(
        "You are an intelligent assistant designed to interact with backend database agents. "
        "First, list available agents. Then, select the best agent for the user's query, send the prompt, and return the answer. "
        "Always include any SQL queries executed for transparency. Suggest follow-up questions or next steps."
    ),
    tools=[list_db_agents, chat_with_db_agent],
    llm="gpt-4.1-mini",
    verbose=False
)

# --- CLI Loop ---
def main():
    print("\U0001F4AC DB Chat Agent (CrewAI) (type 'exit' to quit)")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                break
            # Create a task for the agent
            task = Task(
                description=f"User query: {user_input}",
                agent=db_chat_agent,
                expected_output="A clear, concise answer to the user's database question, including any relevant SQL and suggested follow-up questions."
            )
            crew = Crew(
                agents=[db_chat_agent],
                tasks=[task],
                verbose=False
            )
            result = crew.kickoff()
            print(f"Agent: {result}")
            print("-" * 60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main() 