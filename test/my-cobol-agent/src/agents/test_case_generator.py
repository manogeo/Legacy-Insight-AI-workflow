from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI()

def generate_test_cases(requirements: dict, num_cases: int = 3) -> str:
    prompt = f"""
You are a QA engineer experience in writing test cases.

Your job is to create {num_cases} detailed test scenarios based on the following business requirements:

{requirements}

For each test case, include:
1. **Test Case Description**
2. **Input Values**
3. **Expected Output**
4. **Reasoning**

Format clearly for human review.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a QA engineer creating test cases from business rules."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
