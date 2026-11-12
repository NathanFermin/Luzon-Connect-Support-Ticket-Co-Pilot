# Assumptions and decisions

## Sample data

- The company’s files and real helpdesk sandbox were not supplied. The articles and tickets in this repository are all fictional samples.
- The help articles are written for Luzon Connect support agents. The co-pilot turns their guidance into customer-facing drafts.
- The sample router articles assume one router model, so differences between articles represent different guidance rather than different devices.
- Each article has a category, an update date, and a helpful-vote count. The sample files use `MM-DD-YYYY` dates.
- Helpful-vote counts are fixed sample data. I considered a “Did this help?” button that would update them, but have not implemented it.

## Conflict rule

1. Compare articles only if they apply to the same ticket and conditions.
2. If applicable articles contradict each other, show both and flag the conflict.
3. Rank the article with more helpful votes first. If the counts differ by at most 10% of the higher count, rank the newer article first. For example, 20 and 18 differ by exactly 10% of 20.
4. Let the agent make the final decision.

An older article may have more votes simply because it has been available or shown for longer. Vote count does not measure how often an article was seen or whether it actually resolved a problem. A newer date also does not guarantee correct advice.

This policy is currently expressed in the instructions to Gemini. The code does not yet enforce it independently.

## Mock helpdesk

- No real API specification or key was provided. I assumed the helpdesk lets the co-pilot read a ticket, mark a draft for review, and record an agent-approved reply.
- The keys in `sandbox.py` are public demo values that simulate access roles. They are not real security.
- “For Review” means a draft is awaiting agent approval. “Solved” currently means an agent approved a reply and the mock saved it; it does not prove the customer’s issue was fixed.
- Open tickets are stored in memory. Restarting the program resets them, and publishing the same ticket after a restart could duplicate a line in `tickets.jsonl`.

## Gemini

- Gemini suggests the category and reply using the supplied articles. Its private key is supplied through the `GEMINI_API_KEY` environment variable.
- Free-tier limits and model availability may affect whether a request succeeds.
- The current script uses a fixed test ticket and sends all sample articles. Article retrieval and broader testing are future work.