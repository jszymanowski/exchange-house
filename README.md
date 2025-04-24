# Exchange House API

## Background workers (Celery)

### Administration

#### Manually enqueuing a job

From a worker console, run a command from the `/app/app` folder like:

```bash
celery -A my_app call my_app.tasks.my_task --args='[arg1, arg2]' --kwargs='{"kwarg1": "value1"}'

# Example for exchange rate refresh (no args necessary):
celery -A celery_app call app.tasks.exchange_rate_refresh
```

If successful, the task UUID will be displayed.
