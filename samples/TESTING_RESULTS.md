# Testing Results

## Purpose

This document records testing performed on the Duka Stock Advisor application.

## Functional Tests

| Test | Expected Result | Result |
|---|---|---|
| Start a new session | Session starts successfully | Passed |
| Enter stock information | AI responds with stock advice | Passed |
| Continue conversation | AI remembers previous information | Passed |
| Use 4+ conversation turns | Conversation memory works | Passed |
| End session | Summary is generated and session is saved | Passed |
| Open saved session | Previous conversation can be viewed | Passed |

## Error Handling Tests

| Test | Expected Result | Result |
|---|---|---|
| Empty user input | User is asked to enter a message | Passed |
| Invalid menu choice | User is shown an error and menu continues | Passed |
| API failure | Clear error message is displayed | Passed |
| Invalid AI JSON | Application retries once | Passed |
| Missing/malformed session | Application handles the error without crashing | Passed |

## JSON Validation

The sample session was checked using:

```text
python -m json.tool samples/sample_session.json