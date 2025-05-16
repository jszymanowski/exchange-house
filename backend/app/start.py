import os

import uvicorn

if __name__ == "__main__":
    environment = os.getenv("ENV", "development")
    is_development = environment == "development"
    is_production = environment == "production"

    default_workers = 4 if is_production else 1

    port = int(os.getenv("PORT", 8080))
    workers = int(os.getenv("API_WORKERS", default_workers))

    if port <= 0 or port > 65535:
        raise ValueError(f"Invalid port number: {port}")
    if workers <= 0:
        raise ValueError(f"Invalid number of workers: {workers}")

    try:
        print(f"Starting server on port {port} with {workers} workers in {environment} mode")
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, workers=workers, reload=is_development)
    except Exception as e:
        print(f"Failed to start server: {e}")
        import sys

        sys.exit(1)
