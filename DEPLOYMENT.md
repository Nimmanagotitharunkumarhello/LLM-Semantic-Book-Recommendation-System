# 🚀 Full Stack Deployment Guide
(Next.js Frontend + FastAPI Backend)

This guide documents how to deploy this application using a **Split Architecture**:
*   **Frontend**: Vercel (Free Tier)
*   **Backend**: Render (Free Tier)

---

## 1. Architecture Overview
Because the AI model (PyTorch/FAISS) causes the backend to exceed Vercel's serverless size limits, we host it separately on Render.

```mermaid
graph LR
    User[Browser] -- "1. Visit Website" --> Vercel[Next.js Frontend\n(Vercel)]
    Vercel -- "2. API Requests\n(Search/Filter)" --> Render[FastAPI Backend\n(Render)]
    Render -- "3. Logic/AI" --> Model[FAISS + PyTorch\n(CPU Optimized)]
```

---

## 2. Backend Deployment (Render)

We use **Render** because it supports Docker/Python natively and allows custom build commands.

### Prerequisites (Already committed)
*   `render.yaml`: Blueprint for deployment.
*   `.python-version`: Forces Python 3.10.
*   `requirements.txt`: Optimized for CPU-only (saves RAM).

### Steps
1.  Go to [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub Repo.
4.  **Configuration**:
    *   **Build Command**: `pip install -r backend/requirements.txt`
    *   **Start Command**: `uvicorn backend.api.main:app --host 0.0.0.0 --port 10000`
    *   **Instance Type**: Free (512MB RAM).
5.  **Troubleshooting "Out of Memory"**:
    *   If the build crashes, ensure you are deploying the commit that uses `device='cpu'` in `search.py` and the CPU-only wheels in `requirements.txt`.
    *   **Action**: Click "Manual Deploy" -> "Clear build cache & deploy" to force a clean re-install.

### Success Criteria
*   Wait for the service to show **"Live"**.
*   Copy your Backend URL: `https://your-app-name.onrender.com`

---

## 3. Frontend Deployment (Vercel)

We use **Vercel** for the Next.js frontend.

### Steps
1.  Go to [Vercel Dashboard](https://vercel.com/new).
2.  **Import** your GitHub Repo.
3.  **Configure Project**:
    *   **Framework Preset**: Next.js (Auto-detected).
    *   **Root Directory**: `frontend` (or select root if using `vercel.json` rewrite).
4.  **Environment Variables (The Connection)**:
    *   **IMPORTANT**: You must tell the frontend where the backend lives.
    *   **Name**: `NEXT_PUBLIC_API_URL`
    *   **Value**: `https://your-app-name.onrender.com` (Paste your Render URL here).
5.  Click **Deploy**.

---

## 4. Verification
1.  Open the Vercel URL on your phone/laptop.
2.  Type a query (e.g., "Sad robot story").
3.  If results appear, the **Connection** is working!
