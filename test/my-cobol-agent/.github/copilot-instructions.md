### Purpose

This repo is a small legacy COBOL analysis assistant that: reads COBOL source, extracts business requirements via LLM prompts, converts them to stakeholder-friendly text, generates test cases and a PDF/Word report, and (optionally) displays a Streamlit UI. These instructions help an AI coding agent make productive, low-risk changes.

### Big picture / architecture
- `src/main.py` — linear CLI-style runner: reads `data/sample.cbl`, calls generators, writes outputs to `outputs/`.
- `src/app.py` — Streamlit UI that mirrors `main.py` flows and offers a PDF download.
- `src/generators/*` — LLM-driven transforms:
  - `business_rules_generator.py` — extracts bullet-point business requirements and formats them to paragraph text.
  - `diagram_generator.py` — returns Mermaid flowchart code from business text.
  - `report_generator.py` — creates a Word (.docx) then tries to convert it to PDF.
- `src/agents/test_case_generator.py` — creates human-readable test cases from requirements.
- `src/parsers/cobol_parser.py` — a placeholder parser class for future deterministic parsing.

Data flow: COBOL text -> `generate_business_requirements()` -> bullet text -> `format_requirements_to_document()` -> paragraph text -> `generate_test_cases()` + `generate_logic_diagram()` -> `generate_pdf_report()` -> outputs in `outputs/`.

Why this structure: the code separates concerns by keeping LLM prompts in small modules; outputs are plain text artifacts that get passed between modules rather than structured objects.

### Running & debugging (project-specific)
- Install dependencies (requirements list is incomplete; developer should add missing deps if needed):

```bash
python -m pip install -r requirements.txt
python -m pip install python-docx docx2pdf streamlit
```

- Run the CLI runner:

```bash
python src/main.py
```

- Run the Streamlit UI:

```bash
streamlit run src/app.py
```

- Environment: the code expects an OpenAI API key loaded from environment or `.env` (`OPENAI_API_KEY` / `OPENAI_API_KEY` naming varies — the code uses both `OpenAI()` and `OpenAI(api_key=...)`). Use `python-dotenv` and a `.env` file for local runs.

### Project conventions & gotchas (concrete, discoverable patterns)
- Modules primarily exchange plain text (LLM prompts & responses). Treat generator outputs as human-readable strings, not strict JSON. Example: `generate_business_requirements()` returns bullet points (string) consumed by `format_requirements_to_document()` and `generate_test_cases()`.
- Type hints are sometimes inconsistent: `generate_test_cases` annotates `requirements: dict` but callers pass a string. When modifying signatures, preserve backward-compatible string handling.
- Many source files include literal Markdown code fences (```python) wrapped around the code. Avoid introducing or leaving extra triple-backticks when editing files — remove them so files contain valid Python code.
- PDF conversion uses `docx2pdf` which generally requires Windows or macOS. `report_generator.py` already falls back to returning the `.docx` when conversion fails — keep that behavior.
- LLM clients: modules sometimes call `OpenAI()` without passing `api_key` and sometimes pass `api_key=os.getenv("OPENAI_API_KEY")`. Use environment-backed instantiation and prefer not to hardcode keys.

### Useful file references (examples to inspect when changing behavior)
- Main runner: [src/main.py](src/main.py)
- Streamlit UI: [src/app.py](src/app.py)
- Business rules generator: [src/generators/business_rules_generator.py](src/generators/business_rules_generator.py)
- Test case agent: [src/agents/test_case_generator.py](src/agents/test_case_generator.py)
- Diagram generator: [src/generators/diagram_generator.py](src/generators/diagram_generator.py)
- Report generator: [src/generators/report_generator.py](src/generators/report_generator.py)

### Small editing rules for AI agents
- Preserve textual prompts exactly unless intentionally improving prompt wording; prompts drive output format expectations.
- When changing an interface (e.g., return type), update all call sites in `src/` and `src/app.py`/`src/main.py`.
- Keep fallback behavior in `report_generator.py` for platforms without PDF conversion.
- Remove literal triple-backticks from Python files before committing — they currently wrap many source files and break execution.

### Quick checklist before PR
- Run `python src/main.py` and `streamlit run src/app.py` locally (after setting `OPENAI_API_KEY`).
- Ensure modified files have no leading/trailing Markdown fences (```python). Search the repo for "```python" and remove only where it wraps actual .py files.
- Add missing runtime dependencies to `requirements.txt` if you introduce them.

If anything here is unclear or you'd like additional detail (examples of prompt shape, preferred model names, or a suggested `requirements.txt`), tell me which area to expand. 
