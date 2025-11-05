from generators.business_rules_generator import generate_business_requirements, format_requirements_to_document
from agents.test_case_generator import generate_test_cases
from generators.report_generator import generate_pdf_report


def main():
    with open("data/sample.cbl", "r") as file:
        cobol_code = file.read()

    print("\n🔍 Generating business requirements...\n")
    bullet_points = generate_business_requirements(cobol_code)
    print(bullet_points)

    print("\n📝 Converting to paragraph-style documentation...\n")
    paragraph_doc = format_requirements_to_document(bullet_points)
    print(paragraph_doc)

    print("\n🧪 Generating test cases...\n")
    test_cases = generate_test_cases(bullet_points)
    print(test_cases)

     # ✅ Generate stakeholder PDF report
    print("\n📄 Generating stakeholder report...\n")
    generate_pdf_report(paragraph_doc, test_cases)


    # Optional: Save output to file
    with open("outputs/business_requirements.txt", "w") as out_file:
        out_file.write(paragraph_doc)

    with open("outputs/test_cases.txt", "w") as f:
        f.write(test_cases)

if __name__ == "__main__":
    main()
