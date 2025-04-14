import os

import uvicorn

if __name__ == "__main__":
    environment = os.getenv("ENV", "development")
    is_development = environment == "development"
    is_production = environment == "production"

    default_workers = 4 if is_production else 1

    port = int(os.getenv("PORT", 8080))
    workers = int(os.getenv("WORKERS", default_workers))

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, workers=workers, reload=is_development)
