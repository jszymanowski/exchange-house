import os

import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    workers = int(os.getenv("WORKERS", 4))

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, workers=workers)
