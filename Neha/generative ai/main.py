from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os


# Load environment variables

load_dotenv()



# Create Groq Model

llm = ChatGroq(

    model="openai/gpt-oss-20b",

    groq_api_key=os.getenv("GROQ_API_KEY"),

    temperature=0.7

)



# FastAPI App

app = FastAPI()



# Allow frontend connection

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_methods=["*"],

    allow_headers=["*"],

)



# User Input Format

class ChatRequest(BaseModel):

    question:str



# Prompt

template = """

You are an expert AI tutor.

Your job is to explain any topic in a very simple beginner-friendly way.

User Question:

{question}


Follow these rules:

1. First explain the concept in simple words.

2. Assume the user is a beginner.

3. Avoid unnecessary complex terminology.

4. Use real-world examples.

5. Explain step-by-step.

6. If the topic is technical:
   - explain what it is
   - why it is used
   - where it is used
   - how it works

7. If coding is required:
   provide clean code with explanation.

8. End with:
   "Interview Tip:"
   and provide important points.

"""



prompt = PromptTemplate(

    input_variables=["question"],

    template=template

)




@app.get("/")

def home():

    return {

        "message":"AI Assistant Running"

    }





@app.post("/chat")

def chat(request:ChatRequest):


    question=request.question



    final_prompt = prompt.format(

        question=question

    )


    response = llm.invoke(final_prompt)



    return {

        "answer":response.content

    }