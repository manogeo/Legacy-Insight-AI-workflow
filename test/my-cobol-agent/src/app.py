import streamlit as st
from generators.business_rules_generator import generate_business_requirements, format_requirements_to_document
from agents.test_case_generator import generate_test_cases
from generators.report_generator import generate_pdf_report
from generators.diagram_generator import generate_logic_diagram 
import os

st.set_page_config(page_title="COBOL Analyzer", layout="wide")

st.title("👨‍💻 Legacy COBOL Code Analyzer")

# User Input
st.subheader("Paste your COBOL code below:")
cobol_code = st.text_area("COBOL Code", height=300)

if st.button("Analyze"):
    if not cobol_code.strip():
        st.warning("Please paste some COBOL code to analyze.")
    else:
        with st.spinner("Extracting business logic..."):
            structured = generate_business_requirements(cobol_code)
            paragraph_doc = format_requirements_to_document(structured)
            test_cases = generate_test_cases(structured)

        # Display Outputs
        st.success("✅ Analysis complete!")

        st.subheader("📘 Business Requirements")
        st.write(paragraph_doc)

        st.subheader("🧪 Generated Test Cases")
        st.code(test_cases)
        
# 🧩 Step 4: Logical Diagram (via imported module)
        with st.spinner("Generating logical diagram..."):
            try:
                diagram_code = generate_logic_diagram(paragraph_doc)
                st.subheader("📊 Logical Flow Diagram")
                st.markdown(f"```mermaid\n{diagram_code}\n```")
            except Exception as e:
                st.error(f"❌ Failed to generate diagram: {e}")

        # Generate and offer PDF download
        pdf_path = generate_pdf_report(paragraph_doc, test_cases)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Stakeholder PDF Report",
                    data=f,
                    file_name="cobol_analysis_report.pdf",
                    mime="application/pdf" 
                )
