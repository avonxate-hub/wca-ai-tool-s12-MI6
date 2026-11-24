# Saved Session Data Format

## Overview

The Duka Stock Advisor saves completed conversations as JSON files in the `sessions/` directory.

Each saved session contains the date and time of the session, the conversation history, and the final session summary.

## Session Structure

A saved session contains these main fields:

- `date` — The date when the session was created.
- `time` — The time when the session was created.
- `conversation` — The messages exchanged during the session.
- `summary` — The final summary generated when the session ends.

## Conversation

The `conversation` field contains the messages exchanged between the shop owner and the AI.

Each message contains:

- `role` — Identifies whether the message came from the `user` or the `model`.
- `content` — Contains the actual message content.

User messages contain information or questions entered by the shop owner.

Model messages contain the AI's structured JSON response.

## Session Summary

When a session ends, the application generates a summary containing:

- `summary` — A brief description of what happened during the session.
- `key_stock_issues` — Important stock issues discussed.
- `recommended_actions` — Important actions recommended during the session.

## Example

```json
{
    "date": "2026-11-22",
    "time": "14:00:00",
    "conversation": [
        {
            "role": "user",
            "content": "I have 10 bags of unga in stock."
        },
        {
            "role": "model",
            "content": "AI response"
        }
    ],
    "summary": {
        "summary": "The shop owner discussed unga stock levels.",
        "key_stock_issues": [
            "Unga stock needs to be monitored."
        ],
        "recommended_actions": [
            "Monitor daily unga sales."
        ]
    }
}
```

## Storage

Saved sessions are stored locally in the `sessions/` directory.

The session filename includes the date and time so that different sessions can be stored separately and identified easily.

This allows the user to open previous sessions from the application's **Open Past Session** menu option.