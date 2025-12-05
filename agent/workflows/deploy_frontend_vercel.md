---
description: Deploy frontend to Vercel and configure custom domain
---

# Deploy Frontend to Vercel

This workflow will guide you through deploying the frontend application to Vercel and setting up a custom domain.

## Prerequisites

- A Vercel account (https://vercel.com)
- A custom domain name that you own

## Steps

1.  **Build the Frontend**
    Ensure the frontend builds correctly.

    ```bash
    cd frontend
    npm run build
    ```

2.  **Install Vercel CLI**
    If you haven't already, install the Vercel CLI globally.

    ```bash
    npm install -g vercel
    ```

3.  **Deploy to Vercel**
    Run the deployment command. You will be prompted to log in and configure the project.

    ```bash
    cd frontend
    vercel
    ```

    - Set up and deploy: `Y`
    - Which scope: [Select your account]
    - Link to existing project: `N`
    - Project name: `jamfterraform` (or your preferred name)
    - Directory: `./`
    - Build Command: `npm run build`
    - Output Directory: `dist`
    - Development Command: `npm run dev`

4.  **Production Deployment**
    Once the preview deployment is working, deploy to production.

    ```bash
    vercel --prod
    ```

5.  **Configure Custom Domain (jamfaform.workshopse.com)**

    1.  Go to your Vercel Dashboard: https://vercel.com/dashboard
    2.  Select your project (`jamfterraform`).
    3.  Go to **Settings** > **Domains**.
    4.  Enter `jamfaform.workshopse.com` and click **Add**.
    5.  **DNS Configuration**:
        - Log in to your domain registrar (where you bought `workshopse.com`).
        - Add a **CNAME** record:
          - **Type**: CNAME
          - **Name/Host**: `jamfaform`
          - **Value/Target**: Use the value shown in your Vercel dashboard (e.g., `feace5010d2ea34c.vercel-dns-017.com` or `cname.vercel-dns.com`).
        - Wait for propagation (usually a few minutes, up to 24h).

6.  **Update Backend CORS (Completed)**

    - `backend/main.py` has already been updated to allow `https://jamfaform.workshopse.com`.
    - **Action Required**: Redeploy your backend on Railway to apply this change.

## Verification

- Visit your custom domain URL.
- Ensure the application loads and can communicate with the backend (check the Status indicator).
