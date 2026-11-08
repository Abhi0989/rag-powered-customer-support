
import streamlit as st
from dotenv import load_dotenv

from backend.db import get_db
from backend.workflow import save_review_decision
from backend.case_retrieval import get_customer_context

load_dotenv()

st.set_page_config(
    page_title="Innovac | AI Email Assistant",
    page_icon="📨",
    layout="wide"
)

st.title("📨 Innovac AI Email Case Assistant")
st.caption(
    "AI email analysis · Customer history · Technical knowledge · "
    "Employee review"
)

# --------------------------------------------------
# 1. DATABASE CONNECTION
# --------------------------------------------------

try:
    db = get_db()
    st.sidebar.success("MongoDB connected")
except Exception as exc:
    st.error(f"Could not connect to MongoDB: {exc}")
    st.code("brew services start mongodb/brew/mongodb-community@8.0")
    st.stop()


# --------------------------------------------------
# 2. INBOX FILTERS
# --------------------------------------------------

st.sidebar.header("Email Inbox")

status_filter = st.sidebar.selectbox(
    "Filter by status",
    ["All", "pending_review", "approved", "rejected"]
)

if st.sidebar.button("Refresh inbox"):
    st.rerun()


# --------------------------------------------------
# 3. LOAD EMAILS FROM MONGODB
# --------------------------------------------------

query = {"direction": "inbound"}

if status_filter != "All":
    query["status"] = status_filter

emails = list(
    db.emails.find(query).sort("created_at", -1)
)

st.sidebar.metric("Emails found", len(emails))

if not emails:
    st.info(
        "No emails found for this filter. "
        "Process an incoming email using test_gmail_pipeline.py "
        "and refresh the inbox."
    )
    st.stop()


# --------------------------------------------------
# 4. EMAIL SELECTION
# --------------------------------------------------

email_options = {
    email["_id"]: email
    for email in emails
}


def email_label(email_id):
    email = email_options[email_id]

    subject = email.get("subject", "No subject")
    sender = email.get("sender", "Unknown sender")
    status = email.get("status", "unknown")

    return f"{subject} | {sender} | {status}"


selected_email_id = st.selectbox(
    "Select an incoming email",
    options=list(email_options.keys()),
    format_func=email_label
)

selected_email = email_options[selected_email_id]


# --------------------------------------------------
# 5. EMAIL DETAILS
# --------------------------------------------------

st.divider()
st.subheader("1. Incoming customer email")

left, right = st.columns(2)

with left:
    st.write("**Sender:**", selected_email.get("sender", ""))
    st.write("**Subject:**", selected_email.get("subject", ""))

with right:
    st.write("**Email ID:**", selected_email.get("_id", ""))
    st.write("**Workflow status:**", selected_email.get("status", ""))

st.text_area(
    "Original email",
    value=selected_email.get("body", ""),
    height=180,
    disabled=True
)


# --------------------------------------------------
# 6. AI ANALYSIS
# --------------------------------------------------

st.divider()
st.subheader("2. AI email analysis")

analysis = selected_email.get("analysis", {})

a, b, c = st.columns(3)

a.metric(
    "Priority",
    analysis.get("priority", "Unknown")
)

b.metric(
    "Category",
    analysis.get("category", "Unknown")
)

c.metric(
    "Customer history",
    "Found" if selected_email.get(
        "customer_context_found"
    ) else "Not found"
)

st.write("**Issue summary**")
st.write(analysis.get("summary", "No summary available."))

st.write("**Machine model**")
st.write(analysis.get("machine_model") or "Not identified")

st.write("**Error codes**")
st.write(", ".join(analysis.get("error_codes", [])) or "None identified")

st.write("**Issue description**")
st.write(analysis.get("issue_description", "Not available"))

missing_information = analysis.get("missing_information", [])

if missing_information:
    st.warning(
        "Missing information: " + "; ".join(missing_information)
    )


# --------------------------------------------------
# 7. CUSTOMER HISTORY
# --------------------------------------------------

st.divider()
st.subheader("3. Customer information and history")

sender = selected_email.get("sender", "")

# The sender stored by the pipeline is already normalized.
context = get_customer_context(db, sender)

if context.get("customer_found"):

    customer = context.get("customer", {})

    st.write(
        "**Customer:**",
        customer.get("company_name", "Unknown customer")
    )

    st.write(
        "**Primary email:**",
        customer.get("email", "Not available")
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Machines", len(context.get("machines", [])))
    col2.metric("Previous cases", len(context.get("cases", [])))
    col3.metric("Service records", len(context.get("service_records", [])))

    with st.expander("Customer profile"):
        st.json(customer)

    with st.expander("Registered machines"):
        st.json(context.get("machines", []))

    with st.expander("Previous technical cases"):
        st.json(context.get("cases", []))

    with st.expander("Service history"):
        st.json(context.get("service_records", []))

    with st.expander("Warranty information"):
        st.json(context.get("warranties", []))

    with st.expander("Maintenance plans"):
        st.json(context.get("maintenance_plans", []))

    with st.expander("Technical knowledge documents"):
        for document in context.get("knowledge_documents", []):
            st.markdown(
                f"**{document.get('title', 'Technical document')}**"
            )
            st.write(document.get("text", ""))

else:
    st.warning("No matching customer record was found.")


# --------------------------------------------------
# 8. AI GENERATED RESPONSE
# --------------------------------------------------

st.divider()
st.subheader("4. AI suggested response")

st.caption(
    "Review and edit the suggested response before making a decision. "
    "This dashboard does not send emails."
)

current_status = selected_email.get("status", "pending_review")

if current_status == "pending_review":
    initial_draft = selected_email.get("draft", "")

else:
    initial_draft = selected_email.get(
        "reviewed_draft",
        selected_email.get("draft", "")
    )

draft = st.text_area(
    "Editable response draft",
    value=initial_draft,
    height=250,
    key=f"draft_{selected_email_id}"
)


# --------------------------------------------------
# 9. EMPLOYEE APPROVAL WORKFLOW
# --------------------------------------------------

st.divider()
st.subheader("5. Employee review")

if current_status == "pending_review":

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Approve draft",
            type="primary",
            use_container_width=True
        ):
            try:
                save_review_decision(
                    db,
                    selected_email_id,
                    "approved",
                    draft
                )

                st.success(
                    "Draft approved and saved to the audit log."
                )

                st.rerun()

            except Exception as exc:
                st.error(f"Approval failed: {exc}")

    with col2:
        if st.button(
            "Reject draft",
            use_container_width=True
        ):
            try:
                save_review_decision(
                    db,
                    selected_email_id,
                    "rejected",
                    draft
                )

                st.warning(
                    "Draft rejected. Decision recorded in the audit log."
                )

                st.rerun()

            except Exception as exc:
                st.error(f"Rejection failed: {exc}")

else:

    st.info(
        f"This email has already been marked as: {current_status}"
    )

    st.write("**Reviewed response:**")
    st.write(selected_email.get("reviewed_draft", ""))


# --------------------------------------------------
# 10. SAFETY NOTICE
# --------------------------------------------------

st.divider()

st.caption(
    "Innovac AI Email Case Assistant | Local AI · MongoDB · Gmail API · "
    "Human approval required | No automatic email sending"
)
