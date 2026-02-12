# Vercel Deployment Guide

This project is deployed as two separate Vercel projects: one for the **Backend** (FastAPI) and one for the **Frontend** (Next.js).

## 1. Deploy the Backend (FastAPI)

1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..."** -> **"Project"**.
2.  Import your GitHub repository: `gsarwarkhan/Hackathon-2-Q4`.
3.  **Configure Project:**
    *   **Project Name:** `hackathon-backend` (or similar).
    *   **Root Directory:** Click "Edit" and select `backend`.
    *   **Framework Preset:** Select "Other".
    *   **Environment Variables:**
        *   `DATABASE_URL`: Your Neon DB Connection String.
        *   `BETTER_AUTH_SECRET`: A random string (e.g., generated via `openssl rand -hex 32`).
        *   `OPENAI_API_KEY`: Your OpenAI Key.
    *   **Install Command:** `pip install -r requirements.txt` (Vercel usually auto-detects this).
    *   **Output Directory:** `.` (default).
4.  Click **Deploy**.
5.  **Copy the Domain**: Once deployed, copy the domain (e.g., `https://hackathon-backend-xyz.vercel.app`).

## 2. Deploy the Frontend (Next.js)

1.  Go to your Vercel Dashboard -> **"Add New..."** -> **"Project"**.
2.  Import the **same** GitHub repository again.
3.  **Configure Project:**
    *   **Project Name:** `hackathon-frontend`.
    *   **Root Directory:** Click "Edit" and select `frontend`.
    *   **Framework Preset:** Vercel should auto-detect "Next.js".
    *   **Environment Variables:**
        *   `API_BASE_URL`: Paste the **Backend Domain** from Step 1 (e.g., `https://hackathon-backend-xyz.vercel.app`).
        *   `BETTER_AUTH_SECRET`: **Must match** the one in the Backend.
        *   `BETTER_AUTH_URL`: The URL of *this* frontend (e.g., `https://hackathon-frontend-xyz.vercel.app`). *Note: for the initial deploy, you might not know this yet. You can leave it blank or redeploy after you get the domain.*
4.  Click **Deploy**.

## 3. Verify Connectivity

1.  Open your **Frontend URL**.
2.  Try to Log In or Sign Up.
3.  If successful, the Frontend is correctly communicating with the Backend!

> **Troubleshooting**: If you get 404s or connection errors, check the `API_BASE_URL` variable in the Frontend project settings and ensure it does **not** have a trailing slash (unless your code expects it, but usually standard is without).
