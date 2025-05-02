## Webhook Receiver

This module will receive relevant GitHub events and verify them. It is meant to be used with [automated terraform review](https://github.com/Ishuu1124/Automated_code_review).
Commands from GitHub PRs are verified and corresponding task are sent to Redis servers to be picked up.

---

## How to use:

- Set the Redis database url in `.env`. The same url must be set in the review application for it to accept the tasks.
- Dockerfile can be used to host the app, and application url can be provided as webhook url for a GitHub bot.
- Ensure that `/webhook` is added to the end of the application url when setting it as webhook url.

## Functioning details:

- Using FastAPI to create a server on port 8080
- Server has routes `health` and `webhook`
-   `/health`: returns `{'status': 'ok'}` if server is up
-   `/webhook`: the route that handles GitHub events sent to the API. It checks the type of event and the command used (if any). Upon successful validation, it queues a Celery task to the provided Redis URL, returning `{"status": "Queued"}`. If validation fails or the event type doesn't match, returns `{"status": ""}` instead.
