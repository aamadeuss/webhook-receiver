# Webhook Receiver

This module will receive relevant GitHub events and verify them. It is meant to be used with [automated terraform review](https://github.com/Ishuu1124/Automated_code_review).
Commands from GitHub PRs are verified and corresponding task are sent to Redis servers to be picked up.

---

## Need for webhook receiver

- An independent application to receive, validate and process events.
- To prevent GitHub timeouts (= 10s) for webhook deliveries when large tasks are involved.
- Saves computation time for irrelevant events by validating.

## Tech stack used

- Fastapi for api service
- Celery for task queueing
- Redis for brokering and caching

## How to integrate with your repository's PRs

- Create a GitHub bot.
- Create a Redis instance to store and queue tasks.
- Set the Redis database url in `.env`. The same url must be set in the review application for it to accept the tasks.
- A public URL for the api is necessary to receive events. This can be done by running the app locally and exposing the local port to the internet, or by hosting the application to get a public URL.
  - The URL can then be used as the webhook URL to receive payloads.
  - Dockerfile can be used to host the app, and application url can be provided as webhook url for a GitHub bot.
  - Ensure that `/webhook` is added to the end of the application url when setting it as webhook url.

## Functioning details:

- Using FastAPI to create a server on port 8080
- Server has routes `health` and `webhook`
  - `/health`: returns `{'status': 'ok'}` if server is up.
    <img width="1428" alt="image" src="https://github.com/user-attachments/assets/5c5ff0ba-ff53-4fea-91c2-ad5a4cce3ad0" />
  - `/webhook`: the route that handles GitHub events sent to the API. It checks the type of event and the command used (if any). Upon successful validation, it queues a Celery task to the provided Redis URL, returning `{"status": "Queued"}`. If validation fails or the event type doesn't match, returns `{"status": ""}` instead.
    <img width="1440" alt="image" src="https://github.com/user-attachments/assets/15a0675e-7214-4ae3-b888-faccb27f5d66" />

