# Testing and Error Handling

## 1. Normal Functionality

The application was tested to confirm that the main menu, sessions, conversation flow, and session saving work correctly.

| Test | Expected Result | Result |
|---|---|---|
| Start a new session | New conversation starts | Passed |
| Enter stock information | AI responds with stock advice | Passed |
| Continue conversation | Previous messages are remembered | Passed |
| Use 4 or more turns | Conversation history is maintained | Passed |
| End a session | Summary is generated and session is saved | Passed |
| Open a saved session | Previous conversation and summary are displayed | Passed |

## 2. Error Handling

| Test | Expected Result | Result |
|---|---|---|
| Empty input | User is asked to enter a message | Passed |
| Invalid menu choice | User is asked to choose a valid option | Passed |
| API failure | Clear error message is displayed | Passed |
| Invalid JSON response | Application retries once | Passed |
| Second invalid JSON response | Clear error message is displayed | Passed |
| Empty session | Session is saved with an appropriate summary | Passed |
| Corrupted session file | Application handles the error without crashing | Passed |

## 3. JSON Validation

AI responses are checked before being accepted by the application.

The application verifies that:

- The response is valid JSON.
- The response is a JSON object.
- Required fields are present.
- Required fields are not empty.
- `priority` is `low`, `medium`, or `high`.
- `recommendations` is a list.

The sample session file was also checked using:

```bash
python -m json.tool samples/sample_session.json
```

The JSON file was successfully validated.

## 4. Session Testing

Previously saved sessions were opened to confirm that the application can display stored conversations and summaries.

The application also handles older sessions that do not contain a summary.

## 5. Conclusion

The tests confirmed that the main application functions correctly and that common input, API, JSON, and session-related errors are handled without crashing the application.