from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # loads your .env file

client = OpenAI()  # auto-reads OPENAI_API_KEY from environment

def generate_business_requirements(cobol_code: str) -> str:
    prompt = f"""
You are an experienced legacy system analyst.

Your task is to analyze the following COBOL program and extract the core business functionality. Return the result as:

1. Business Objectives
2. Input Fields (name, type, validations)
3. Output Fields
4. Business Rules (step-by-step logic)
5. Assumptions or Constraints

Only return information directly implied by the code.


COBOL Code:
{cobol_code}

Return as bullet points.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a COBOL-to-business logic translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
# ✅ Agent 2: Converts bullet points into a paragraph-style plain English document
def format_requirements_to_document(bullet_points: str) -> str:
    prompt = f"""
You are a technical writer AI.

Rephrase the following bullet-point business requirements into a well-written plain English document.

Make it sound like formal documentation that explains the business functionality of a system to stakeholders.

Bullet Points:
{bullet_points}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a technical documentation writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content