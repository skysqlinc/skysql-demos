from setuptools import setup, find_packages

setup(
    name="chat-with-db-agents",
    version="0.1.0",
    description="A conversational agent for querying database agents via CLI or Streamlit UI.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "llama-index-core",
        "llama-index-llms-openai",
        "openai",
        "requests",
        "python-dotenv",
        "streamlit",
        "streamlit_chat"
    ],
    entry_points={
        "console_scripts": [
            "chat-db-cli=student_advisor_agent:main",
            "chat-db-ui=student_advisor_streamlit_app:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.8",
) 