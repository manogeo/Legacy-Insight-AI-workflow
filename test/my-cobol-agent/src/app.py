import streamlit as st
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate
import os

st.set_page_config(page_title="COBOL Analyzer", layout="wide")

st.title("👨‍💻 Legacy COBOL Code Analyzer")

# User Input
st.subheader("Paste your COBOL code below:")
cobol_code = st.text_area("COBOL Code", height=300)

# Define LangChain components
llm = OpenAI(temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Prompt for generating business requirements
business_requirements_prompt = PromptTemplate(
    input_variables=["cobol_code"],
    template="""
    You are an experienced legacy system analyst. Analyze the following COBOL program and extract the core business functionality. Return the result as:

    1. Business Objectives
    2. Input Fields (name, type, validations)
    3. Output Fields
    4. Business Rules (step-by-step logic)
    5. Assumptions or Constraints

    COBOL Code:
    {cobol_code}

    Return as bullet points.
    """
)

business_requirements_chain = LLMChain(llm=llm, prompt=business_requirements_prompt)

# Prompt for formatting requirements
format_requirements_prompt = PromptTemplate(
    input_variables=["bullet_points"],
    template="""
    You are a technical writer AI. Rephrase the following bullet-point business requirements into a well-written plain English document.

    Bullet Points:
    {bullet_points}
    """
)

format_requirements_chain = LLMChain(llm=llm, prompt=format_requirements_prompt)

# Prompt for generating test cases
test_cases_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a QA engineer experienced in writing test cases. Create 3 detailed test scenarios based on the following business requirements:

    {requirements}

    For each test case, include:
    1. Test Case Description
    2. Input Values
    3. Expected Output
    4. Reasoning
    """
)

test_cases_chain = LLMChain(llm=llm, prompt=test_cases_prompt)

if st.button("Analyze"):
    if not cobol_code.strip():
        st.warning("Please paste some COBOL code to analyze.")
    else:
        with st.spinner("Extracting business logic..."):
            # Generate business requirements
            bullet_points = business_requirements_chain.run(cobol_code=cobol_code)
            paragraph_doc = format_requirements_chain.run(bullet_points=bullet_points)
            test_cases = test_cases_chain.run(requirements=paragraph_doc)

        # Display Outputs
        st.success("✅ Analysis complete!")

        st.subheader("📘 Business Requirements")
        st.write(paragraph_doc)

        st.subheader("🧪 Generated Test Cases")
        st.code(test_cases)
