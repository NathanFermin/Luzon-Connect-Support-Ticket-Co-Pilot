import json
from pathlib import Path

from google import genai
from google.genai import types
from pydantic import BaseModel

class CopilotDraft(BaseModel):
    category: str
    reply: str
    citations: list[str]
    conflict_note: str

def draft_reply(ticket: dict, articles: list[dict]) -> CopilotDraft:
    """Ask Gemini for a draft; an agent must review it before publishing."""
    client = genai.Client()

    rules = """
You are a co-pilot for Luzon Connect support agents.
Suggest a ticket category and draft a polite customer reply.
Use only the supplied help articles. Cite their filenames in the reply.
Return cited filenames in the citations list.

There are three distinct cases you must keep in mind:
    1. Regular case: Use the relevant article to draft a cited solution.
    2. Conflicting articles: Show the article with more helpful votes first, but clearly flag the disagreement and show the other article too.
    3. Tie or close vote counts: Show the more recently updated article first, while still flagging the disagreement.

    Vote counts are close when their difference is at most "10%" of the higher count. For example, 22 and 20 are close. 
    In that case, rank the more recently updated article first.

Do not claim the customer's issue is solved. Do not send the reply.
A human agent must review or edit it.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            rules
            + "\n\nTicket and available articles:\n"
            + json.dumps({"ticket": ticket, "articles": articles})
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CopilotDraft,
        ),
    )

    draft = response.parsed
    if draft is None:
        raise RuntimeError("Gemini did not return a draft.")

    return draft


if __name__ == "__main__":
    # First test. Later, replace this with get_ticket("T-004", "luzon").
    ticket = {"id": "T-004", "message": "My router is blinking red."}

    folder = Path(__file__).parent
    articles = [
        {"filename": path.name, "content": path.read_text(encoding="utf-8")}
        for path in folder.glob("*.md")
    ]

    if not articles:
        raise RuntimeError(f"No .md articles found in {folder}")

    print("Asking Gemini...", flush=True)
    draft = draft_reply(ticket, articles)
    print("Gemini replied.", flush=True)
    print("Category:", draft.category)
    print("Reply:", draft.reply)
    print("Citations:", draft.citations)
    print("Conflict:", draft.conflict_note or "None")