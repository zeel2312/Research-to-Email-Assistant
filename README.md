# 📨 Research-to-Email Assistant (Gemini + LangChain + Judgeval)

Generate clear, stakeholder-friendly email digests from any topic **in one CLI command** – with full tracing and online evaluations powered by **Judgment Labs / judgeval**.

<br>

| Stack | Why I chose it |
|-------|-----------------|
| **Google Gemini 2.0 Flash** | Fast, cost-efficient model for concise summaries |
| **LangChain** | Easy tool/LLM chaining with a huge ecosystem |
| **judgeval** | Real-time tracing + quality metrics (Answer Relevancy) |

<br>

## ✨ Features
* 🔍 **Web & Wikipedia search** (Serper Google Search optional)\
* 📝 **Gemini-drafted email** capped at 180 words\
* 📈 **Judgeval tracing** – every run auto-streams to the Judgment dashboard\
* ✅ **Answer Relevancy eval**  (online) – flags off-topic emails\
* Zero OpenAI keys required

---

## 🚀 Quick Start

```bash
git clone <your-fork> && cd research_email_agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # fill in keys
# └─ GEMINI_API_KEY=<your-key>
# └─ (optional) SERPER_API_KEY=<google search key>
# └─ JUDGMENT_API_KEY / JUDGMENT_ORG_ID  ← get free at app.judgmentlabs.ai

python run.py "Explain how AI works in simple terms"
```

You’ll see:
```bash
🔍 View Trace: judgeval trace link here
=== Draft Email ===
Subject: AI Explained Simply
...
```

## 🗂 Project Structure
```bash
research_email_agent/
├─ agent/                       # core logic
│   ├─ tools/                   # WebSearchTool + EmailDraftTool
│   ├─ main_agent.py            # tracing + eval orchestration
│   └─ config.py
├─ run.py                       # CLI entry
├─ .env.example                 # sample secrets
├─ requirements.txt
└─ traces/                      # local JSON traces (git-ignored)
```

## 🛠️ How Tracing & Evals Work

1. A global Tracer object is created in main_agent.py

2. Functions are decorated with @judgment.observe(span_type="…") → spans auto-record inputs/outputs.

3. After drafting the email, we call:
   ```bash
   judgment.async_evaluate(
    scorers=[AnswerRelevancyScorer(threshold=0.5)],
    input=research,
    actual_output=email,
    model="gpt-4o-mini",
   )
   ```

Judgeval queues the eval; the score appears on the `draft_email_step` span in seconds.

## 🤝 Contributing
PRs, issues, and docs tweaks welcome!

