import json
from pathlib import Path
from sandbox import get_ticket, update_ticket, publish_ticket

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
    cases = {
        "1": ("Base case", "T-004", ["red_light.md"]),
        "2": (
            "Conflict with different votes",
            "T-006",
            ["router_crash.md", "router_crash_2.md"],
        ),
        "3": (
            "Close votes; newer article first",
            "T-005",
            ["slow_speed.md", "slow_speed_2.md"],
        ),
    }

    print("1. Base case: blinking red light")
    print("2. Conflict case: router crashing")
    print("3. Recency case: slow internet")

    choice = input("Choose a test (1, 2, or 3): ").strip()
    if choice not in cases:
        raise SystemExit("Please choose 1, 2, or 3.")

    label, ticket_id, filenames = cases[choice]

    ticket = get_ticket(ticket_id, "luzon")
    if isinstance(ticket, str):
        raise SystemExit(ticket)

    folder = Path(__file__).parent
    articles = [
        {
            "filename": name,
            "content": (folder / name).read_text(encoding="utf-8"),
        }
        for name in filenames
    ]

    print(f"\nTesting: {label}")
    print("Asking Gemini...", flush=True)

    draft = draft_reply(ticket, articles)

    print("Gemini replied.")
    print("\nSuggested category:", draft.category)
    print("Citations:", draft.citations)
    print("Conflict:", draft.conflict_note or "None")
    print("\nSuggested reply:\n", draft.reply)

    edited_category = input(
        "\nEdit category, or press Enter to keep suggestion: "
    ).strip()
    final_category = edited_category or draft.category

    edited_reply = input(
        "\nType an edited reply, or press Enter to keep the draft:\n"
    ).strip()
    final_reply = edited_reply or draft.reply

    print("\nFinal category:", final_category)
    print("Final reply:", final_reply)

    update_result = update_ticket(
        ticket_id, final_category, final_reply, "luzon"
    )
    print(update_result)

    approval = input(
        "\nAgent: approve this reply? (yes/no): "
    ).strip().lower()

    if approval == "yes":
        publish_result = publish_ticket(
            ticket_id, final_category, final_reply, "connect"
        )
        print(publish_result)
    else:
        print("Not approved. Ticket remains For Review.")