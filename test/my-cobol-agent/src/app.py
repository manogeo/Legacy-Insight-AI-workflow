import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import langchain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

st.set_page_config(page_title="COBOL Analyzer", layout="wide")

st.title("👨‍💻 Legacy COBOL Code Analyzer")

# Email Configuration
st.sidebar.header("Email Configuration")
sender_email = st.sidebar.text_input("Sender Email (Gmail)", "")
sender_password = st.sidebar.text_input("Sender Password (App Password)", "", type="password")
recipient_email = st.sidebar.text_input("Recipient Email", "")

# User Input
st.subheader("Paste your COBOL code below:")
cobol_code = st.text_area("COBOL Code", height=300)

# Define LangChain components
llm = ChatOpenAI(temperature=0.7)

# Prompt for generating business requirements
business_requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced legacy system analyst."),
    ("human", """
    You are an experienced legacy system analyst. Analyze the following COBOL program and extract the core business functionality. Return the result as:

    1. Business Objectives
    2. Input Fields (name, type, validations)
    3. Output Fields
    4. Business Rules (step-by-step logic)
    5. Assumptions or Constraints

    COBOL Code:
    {cobol_code}

    Return as bullet points.
    """)
])

business_requirements_chain = business_requirements_prompt | llm

# Prompt for formatting requirements
format_requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical writer AI."),
    ("human", """   
    You are a technical writer AI. Rephrase the following bullet-point business requirements into a well-written plain English document.

    Bullet Points:
    {bullet_points}
    """)
])

format_requirements_chain = format_requirements_prompt | llm

# Prompt for generating test cases
test_cases_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a QA engineer experienced in writing test cases."),
    ("human", """
    You are a QA engineer experienced in writing test cases. Create 3 detailed test scenarios based on the following business requirements:

    {requirements}

    For each test case, include:
    1. Test Case Description
    2. Input Values
    3. Expected Output
    4. Reasoning
    """)
])

test_cases_chain = test_cases_prompt | llm

def send_email_with_pdf(sender, password, recipient, pdf_path):
    """Send PDF via email"""
    try:
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "COBOL Analysis - Business Requirements PDF"
        
        body = "Please find attached the business requirements PDF from the COBOL code analysis."
        message.attach(MIMEText(body, "plain"))
        
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {pdf_path}")
        message.attach(part)
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

if st.button("Analyze"):
    if not cobol_code.strip():
        st.warning("Please paste some COBOL code to analyze.")
    else:
        with st.spinner("Extracting business logic..."):
          # Generate business requirements
            bullet_points = business_requirements_chain.invoke({"cobol_code": cobol_code}).content
            paragraph_doc = format_requirements_chain.invoke({"bullet_points": bullet_points}).content
            test_cases = test_cases_chain.invoke({"requirements": paragraph_doc}).content

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, paragraph_doc)
        pdf_output_path = "business_requirements.pdf"
        pdf.output(pdf_output_path)

        # Display Outputs
        st.success("✅ Analysis complete! PDF generated.")

        st.subheader("📘 Business Requirements")
        st.write(paragraph_doc)

        st.subheader("🧪 Generated Test Cases")
        st.code(test_cases)

        st.download_button(
            label="Download Business Requirements PDF",
            data=open(pdf_output_path, "rb").read(),
            file_name="business_requirements.pdf",
            mime="application/pdf"
        )

        # Send Email
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Send PDF via Email"):
                if not sender_email or not sender_password or not recipient_email:
                    st.error("Please fill in all email configuration fields in the sidebar.")
                else:
                    with st.spinner("Sending email..."):
                        if send_email_with_pdf(sender_email, sender_password, recipient_email, pdf_output_path):
                            st.success("✅ Email sent successfully!")
                        else:
                            st.error("Failed to send email.")

