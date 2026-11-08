
from dotenv import load_dotenv
from backend.ai import analyze_email

load_dotenv()

subject = "URGENT: CNC machine stopped"

body = """
Our CNC milling machine has suddenly stopped
during production.

The control panel displays error code E-204.

We restarted the machine, but the problem remains.

We cannot continue production.

Please arrange technical support as soon as possible.
"""

print("Analyzing customer email...\n")

analysis = analyze_email(subject, body)

print("CATEGORY:", analysis.category)

print("PRIORITY:", analysis.priority)

print("SUMMARY:", analysis.summary)

print("MACHINE MODEL:", analysis.machine_model)

print("ERROR CODES:", analysis.error_codes)

print("ISSUE:", analysis.issue_description)

print("MISSING INFORMATION:", analysis.missing_information)

print("RECOMMENDED DEPARTMENT:", analysis.recommended_department)

print("EVIDENCE:", analysis.evidence_summary)
