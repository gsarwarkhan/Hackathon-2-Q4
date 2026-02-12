from main import app

# This is the entry point for Vercel Serverless Functions
# It exposes the FastAPI app instance as a serverless handler
# No need for 'handler = app' alias with modern Vercel python runtime, 
# but good for clarity if needed.
