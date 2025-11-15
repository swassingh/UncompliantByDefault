"""
Main entry point for UncompliantByDefault backend.
This intentionally contains non-compliant code patterns.
"""
import uvicorn
from fastapi import FastAPI
from api import router

app = FastAPI(title="UncompliantByDefault API", version="1.0.0")
app.include_router(router)

if __name__ == "__main__":
    # Hardcoded port - non-compliant
    uvicorn.run(app, host="0.0.0.0", port=8000)

