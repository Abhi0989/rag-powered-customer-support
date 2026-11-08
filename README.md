# AI-Powered Email Case Assistant

A local demonstration of an AI email workflow with MongoDB, semantic retrieval (RAG),
OpenAI, structured validation, and employee review.

## 1. Requirements

- Python 3.10+
- MongoDB Community Server running locally, or a MongoDB Atlas connection string
- OpenAI API key

## 2. Setup on macOS

```bash
mkdir ai_email_case_assistant
cd ai_email_case_assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env .env
```

Edit `.env` and add your OpenAI API key.

If you use Homebrew MongoDB Community Server, start it with the service command
appropriate to your installed MongoDB version, for example:

```bash
brew services start mongodb-community
```

Check MongoDB is available:

```bash
mongosh
```

For MongoDB Atlas, replace `MONGODB_URI` in `.env` with your Atlas connection string.

## 3. Run

```bash
streamlit run app.py
```

In the sidebar, click **Load / reset demo data**. Choose a sample email and click
**Process email with AI**.

## 4. What the demo shows

1. Customer lookup by sender email.
2. Relational-style retrieval across customer, order, case and email collections.
3. Semantic retrieval over policy knowledge chunks using embeddings and cosine similarity.
4. AI classification and structured output validated with Pydantic.
5. Grounded email draft generation.
6. Employee edit / approve / reject workflow.
7. Audit log of employee decisions.

## 5. Important design note

This demo computes vector similarity in Python over stored embeddings so it can run
without configuring a MongoDB Atlas Vector Search index. For production, move the
semantic search into MongoDB Atlas Vector Search and create a vector index on
`knowledge_chunks.embedding` with the correct embedding dimensions (1536 for
`text-embedding-3-small`).

## 6. Production improvements

- Gmail / Microsoft Graph integration with OAuth and webhook or polling.
- Background processing with Celery or a queue.
- Attachment scanning, OCR and document extraction.
- Access control, tenant isolation and role-based permissions.
- PII minimization, encryption, retention policy and GDPR review.
- Idempotency keys, retries, dead-letter queue and observability.
- Human approval before any outbound email.
- Evaluation dataset for retrieval quality, factuality and draft quality.
- Restrict retrieved data by customer permissions before passing it to the model.

The demo intentionally does not send email. Approval is recorded in MongoDB only.
