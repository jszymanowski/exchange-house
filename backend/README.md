# Exchange House API

## Local development

### Set up pre-commit

On a new machine, the defined pre-commit config must be installed:

```bash
uv run pre-commit install

# Run against all files
uv run pre-commit run --all-files
```

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
