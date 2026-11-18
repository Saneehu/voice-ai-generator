from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

template = """
You are an experienced {role}.

Answer the following question.

Question:
{question}

Difficulty Level:
{level}

Instructions:
- Keep the explanation suitable for the selected level.
- Give real-world examples whenever possible.
- If applicable, provide interview tips.
- If coding is required, provide code examples.
"""

prompt = PromptTemplate(
    input_variables=["role", "question", "level"],
    template=template
)

print("=" * 60)
print("🤖 Universal AI Assistant")
print("=" * 60)

while True:

    role = input("\nEnter Role (Example: Data Engineer, HR, Python Mentor): ")

    if role.lower() == "exit":
        break

    level = input("Enter Level (Beginner / Intermediate / Advanced): ")

    question = input("Ask your question: ")

    final_prompt = prompt.format(
        role=role,
        level=level,
        question=question
    )

    response = llm.invoke(final_prompt)

    print("\nAI Answer:\n")
    print(response.content)