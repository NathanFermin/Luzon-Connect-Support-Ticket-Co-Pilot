import json
from pathlib import Path

SANDBOX_KEY = "luzon"
AGENT_SANDBOX_KEY = "connect"

unresolved_tickets = [
    {"id": "T-004", "message": "My router is blinking red.", "category": None, "status": "open", "reply": None},
    {"id": "T-005", "message": "My internet is slow.", "category": None, "status": "open", "reply": None},
    {"id": "T-006", "message": "Why is my router crashing?", "category": None, "status": "open", "reply": None},
]

def authenticate(api_key) -> bool:
    if api_key == SANDBOX_KEY:
        return True
    return False

def agent_authenticate(api_key) -> bool:
    if api_key == AGENT_SANDBOX_KEY:
        return True
    return False

def get_ticket(ticket_id, api_key) -> dict | str:
    """
    Get the details of a ticket by its ID.
    Return the ticket's ID, message, category, status, and reply if found
    Otherwise return "Ticket not found."
    """
    if not authenticate(api_key):
        return "Unauthorized access."
    for ticket in unresolved_tickets:
        if ticket["id"] == ticket_id:
            return ticket.copy()
    return "Ticket not found."


def update_ticket(ticket_id, category, reply, api_key) -> str:
    """
    Update the details of a ticket by its ID.
    Return a success message if the ticket is found and updated,
    Otherwise return "Ticket not found."
    This is only for flagging a ticket for review.
    """
    if not authenticate(api_key):
        return "Unauthorized access."
    for ticket in unresolved_tickets:
        if ticket["id"] == ticket_id:
            ticket["category"] = category
            ticket["status"] = "For Review"
            ticket["reply"] = reply
            return f"Ticket ID: {ticket['id']} updated successfully."
    return "Ticket not found."

def publish_ticket(ticket_id, category, reply, api_key) -> str:
    """
    Publish the details of a ticket by its ID.
    Return a success message if the ticket is found and published,
    Otherwise return "Ticket not found."
    This is only for publishing a ticket to the resolved tickets list.
    """
    if not agent_authenticate(api_key):
        return "Unauthorized access."
    for ticket in unresolved_tickets:
        if ticket["id"] == ticket_id and ticket["status"] == "For Review":
            ticket["category"] = category
            ticket["status"] = "Solved"
            ticket["reply"] = reply
            tickets_file = Path(__file__).with_name("tickets.jsonl")
            with tickets_file.open("a", encoding="utf-8") as file:
                file.write(json.dumps(ticket) + "\n")
            unresolved_tickets.remove(ticket)
            return f"Ticket ID: {ticket['id']} published successfully."
    return "Ticket must be For Review before publishing."