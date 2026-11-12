# Luzon-Connect-Support-Ticket-Co-Pilot

A small support-agent demo for my Patunay application. It uses fictional Luzon Connect tickets and help articles to suggest a ticket category and a cited customer reply. An agent can edit or approve the suggestion before the mock helpdesk records it.

## How it works

1. `gemini_copilot.py` sends a sample ticket and the Markdown help articles to Gemini.
2. Gemini suggests a category, a draft reply with article citations, and a conflict note.
3. The agent reviews the output in the terminal and can edit the category or reply.
4. If the agent approves, `sandbox.py` records the final result in `tickets.jsonl`. No reply is sent to a real customer.

The script offers three sample cases: a single matching article, articles with different helpful-vote counts, and close vote counts where recency takes priority.

## Run the demo

Use Python 3.10 or newer. In a PowerShell terminal opened in this repository:

```powershell
python -m pip install google-genai pydantic
$env:GEMINI_API_KEY = Read-Host "Enter Gemini API key"
python gemini_copilot.py
```

Enter the Gemini key only when the terminal prompts you. Do not add it to the repository. The public keys in `sandbox.py` are fictional demo keys for the mock helpdesk, not the Gemini key.

## Conflict policy

Compare articles only when they apply to the same customer issue. If applicable articles disagree, flag the conflict and show both sources to the agent. Normally, rank the article with more helpful votes first. If the vote counts differ by **at most 10% of the higher count**, rank the more recently updated article first. For example, 22 and 20 differ by about 9.1% of 22, so the newer article takes priority.

This rule is currently given to Gemini as an instruction. The Python code does not yet independently detect contradictions or calculate article ranking. The agent must check the articles and draft before approval.

## Assumptions and limitations

The real knowledge-base export, resolved tickets, helpdesk API specification, and helpdesk key were not supplied. I created a small fictional sample and local mock helpdesk functions. Helpful-vote counts are sample values, not live feedback. See `notes/ideas/assumptions.md` for my detailed decisions.

The current script lets the user choose one of three sample tickets and sends Gemini only the articles assigned to that case.

## Next steps

- Let agents select any open ticket.
- Retrieve relevant articles before calling Gemini.
- Enforce the conflict and ranking rule in Python.
- Verify that citations refer to supplied articles.
- Add a clearer and more visually appealing agent review screen and persistent ticket storage.
- Test the regular, conflict, and recency cases end to end.
- Implement a "Did this help?" Button

## AI tools used

I used ChatGPT to understand the brief, learn the file formats and Git workflow, discuss tradeoffs, draft and debug parts of the Python code, help write the README, and revise the assumptions document. I chose the sample ticket scenarios and articles, proposed helpful votes and the 10% recency rule, and reviewed the co-pilot’s output. The demo uses the Gemini API to suggest ticket categories and cited replies. An agent can edit or approve those suggestions before the mock helpdesk saves them. I did not train a model or use real company data.