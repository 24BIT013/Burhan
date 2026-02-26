# Frontend (Next.js)

This folder now contains a standalone Next.js frontend for Vercel.

## Local run

```bash
npm install
npm run dev
```

Create `.env.local` from `.env.example` and set:

```bash
NEXT_PUBLIC_BACKEND_URL=https://burhan-2.onrender.com
```

## Vercel settings

- Root Directory: `frontend`
- Build Command: `npm run build`
- Output: default Next.js
- Environment Variable: `NEXT_PUBLIC_BACKEND_URL` (your Render backend URL)

