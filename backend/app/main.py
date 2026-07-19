from fastapi import FastAPI

app = FastAPI(
    title="Agentic-XDR API",
    version="1.0.0",
    description="Backend API for Agentic-XDR",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Agentic-XDR",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Agentic-XDR API",
        "version": "1.0.0",
    }


@app.get("/version")
async def version():
    return {
        "application": "Agentic-XDR",
        "version": "1.0.0",
        "environment": "development",
    }