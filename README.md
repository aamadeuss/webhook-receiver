## Webhook Receiver

This module will receive relevant GitHub events and verify them. It is meant to be used with (automated terraform review)[https://github.com/Ishuu1124/Automated_code_review].
Commands are verified and corresponding task are sent to Redis servers to be picked up.

---

## How to use:

- Set the Redis database url in `.env`. The same url must be set in the review application for it to accept the tasks.
- Dockerfile can be used to host the app, and application url can be provided as webhook url for a GitHub bot.
