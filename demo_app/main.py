```python
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import requests
import os

app = FastAPI()

# Replace with your actual Claude API key
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_API_KEY"

@app.get("/")
async def home():
    return FileResponse("demo_index.html")


@app.post("/api/claude")
async def chat(request: Request):

    body = await request.json()

    model = body.get("model", "claude-sonnet-4-6")
    system = body.get("system", "You are a helpful assistant.")
    user = body.get("user", "")

    if not user:
        return JSONResponse(
            status_code=400,
            content={"error": "user message required"}
        )

    try:

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": model,
                "max_tokens": 1024,
                "system": system,
                "messages": [
                    {
                        "role": "user",
                        "content": user
                    }
                ]
            }
        )

        data = response.json()

        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "error": data.get("error", {}).get(
                        "message",
                        "Anthropic API error"
                    )
                }
            )

        return data

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```
