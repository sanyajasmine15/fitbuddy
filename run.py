import os
import uvicorn

if __name__ == "__main__":
    codespace = os.getenv("CODESPACE_NAME")

    if codespace:
        print("\nFitBuddy is running!")
        print(f"Open in Chrome: https://{codespace}-8000.app.github.dev\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )