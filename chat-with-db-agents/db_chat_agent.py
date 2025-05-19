import os
import requests
from dotenv import load_dotenv
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI

# --- Load API keys from .env file ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SKYSQL_API_KEY = os.getenv("SKYSQL_API_KEY")

if not OPENAI_API_KEY or not SKYSQL_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY or SKYSQL_API_KEY in environment or .env file")

SKYSQL_API_URL = "https://api.skysql.com"

# --- Tool 1: List DB Agents ---
def list_db_agents() -> str:
    """Lists available DB agents."""
    response = requests.get(
        f"{SKYSQL_API_URL}/copilot/v1/agent/",
        headers={"X-API-Key": SKYSQL_API_KEY, "Content-Type": "application/json"}
    )
    response.raise_for_status()
    agents = response.json()
    return "\n".join([f"{a['id']}: {a['name']} - {a['description']}" for a in agents])

list_agents_tool = FunctionTool.from_defaults(
    fn=list_db_agents,
    name="list_db_agents",
    description="Lists available DB agents."
)

# --- Tool 2: Chat with a DB Agent ---
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
        return f"""{content}

**SQL:**
```
{sql}
```"""
    return content

chat_tool = FunctionTool.from_defaults(
    fn=chat_with_db_agent,
    name="chat_with_db_agent",
    description="Send a user prompt to a specific DB agent ID and return the response.",
)

# --- LLM + Agent Setup ---
llm = OpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)

db_chat_agent = FunctionCallingAgent.from_tools(
    tools=[list_agents_tool, chat_tool],
    llm=llm,
    verbose=False,
    system_prompt=(
        """You are an intelligent assistant designed to interact with backend database agents to answer user queries. Follow this structured approach:
        1. **Agent Discovery**: Begin by invoking `list_db_agents` to retrieve available database agents along with their IDs and descriptions. Cache the results for future use.
        2. **Query Execution**: Based on the user's question, select the most appropriate database agent(s) and use `chat_with_db_agent` to obtain responses.
        3. **Response Synthesis**: Analyze the information received and craft a clear, concise, and conversational answer for the user. Ensure that any SQL queries executed are included in your response for transparency.
        4. **Proactive Engagement**: Conclude your response by suggesting relevant follow-up questions or next steps the user might consider, such as:
        - 'Would you like to explore this data further?'
        - 'Do you want to perform another operation or query?'
        - 'Is there another dataset or parameter you're interested in?'
        Maintain a helpful and engaging tone throughout the interaction."""
    )
)

# --- CLI Loop ---
def main():
    print("\U0001F4AC DB Chat Agent (type 'exit' to quit)")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                break
            response = db_chat_agent.chat(user_input)
            print(f"Agent: {response}")
            print("-" * 60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
