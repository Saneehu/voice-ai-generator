from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

print("=" * 50)
print("🤖 AI Tutor Started")
print("Type 'exit' to quit")
print("=" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("\nGoodbye!")
        break

    try:

        response = llm.invoke(question)

        print("\nAI:\n")
        print(response.content)

    except Exception as e:

        print("\nError:")
        print(e)