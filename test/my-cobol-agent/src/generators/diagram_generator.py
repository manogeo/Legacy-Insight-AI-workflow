# generators/diagram_generator.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_logic_diagram(business_logic_text: str) -> str:
    """
    Generate a Mermaid diagram that visualizes the logical flow
    of the provided business logic using OpenAI's LLM API.

    Args:
        business_logic_text (str): Textual description of business logic.

    Returns:
        str: Mermaid diagram code (graph TD ...).
    """
    diagram_prompt = f"""
    You are an expert software analyst.
    Based on the following COBOL business logic, create a Mermaid flowchart that represents
    the logical flow of operations, key decisions, and process branches.

    Business Logic:
    {business_logic_text}

    Output only valid Mermaid syntax starting with ```mermaid and ending with ```.
    Use a top-down (graph TD) layout.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a software visualization assistant."},
            {"role": "user", "content": diagram_prompt}
        ],
        temperature=0.3,
    )

    raw_output = response.choices[0].message.content.strip()

    # Extract Mermaid code if wrapped in backticks
    if "```mermaid" in raw_output:
        diagram_code = raw_output.split("```mermaid")[1].split("```")[0].strip()
    else:
        diagram_code = raw_output

    return diagram_code
