"""Trace + one-line online eval (judgeval ≥0.0.51)."""
from judgeval.common.tracer import Tracer
from judgeval.scorers import AnswerRelevancyScorer

from agent.tools.web_search_tool import WebSearchTool
from agent.tools.email_draft_tool import EmailDraftTool

judgment = Tracer(project_name="research-email-agent")

web_tool = WebSearchTool()
email_tool = EmailDraftTool()


@judgment.observe(span_type="tool")
def research_step(topic: str) -> str:
    return web_tool.run(topic)


@judgment.observe(span_type="tool")
def draft_email_step(research: str) -> str:
    return email_tool.run(research)


@judgment.observe(span_type="function")
def run_agent(topic: str) -> str:
    """End-to-end; CLI calls this."""
    research = research_step(topic)
    email = draft_email_step(research)

    # 🔎 real-time Answer-Relevancy score
    judgment.async_evaluate(
        scorers=[AnswerRelevancyScorer(threshold=0.5)],
        input=research,
        actual_output=email,
        model="gpt-4o-mini",   # any judge model name works
    )

    return email
