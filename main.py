import asyncio
# Ensure project root is on path when running as script
import os, sys
sys.path.append(os.path.dirname(__file__))
import uvicorn

def main():
    """Launch FastAPI web server (controllers.controller:app) on port 8080."""
    uvicorn.run("controllers.controller:app", host="0.0.0.0", port=8080, reload=True)

if __name__ == "__main__":
    main()
