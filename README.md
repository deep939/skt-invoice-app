# SKT Tax Invoice Generator

A simple web app for Swathi Kiran Transport to fill in invoice details and
download a completed Tax Invoice PDF in the official company format.

## What's inside

```
invoice_app/
├── app.py              Flask backend — serves the form and the PDF API
├── fill_pdf.py          Core logic that overlays form data onto Format.pdf
├── Format.pdf            The original invoice template (do not delete/rename)
├── requirements.txt       Python dependencies
├── Procfile              Start command for Render / Railway / Heroku-style hosts
└── static/
    ├── index.html        The invoice form (UI)
    └── app.js            Form logic: dynamic rows, live totals, submit/download
```

## How it works

1. The person filling the form enters invoice details and up to 10 line items.
2. Amounts (per-row Amount, IGST @ 18%, and the grand Total) are calculated
   automatically in the browser as they type.
3. On "Generate Invoice PDF", the form sends the data as JSON to
   `POST /api/generate-invoice`.
4. The backend overlays that data onto `Format.pdf` at the exact coordinates
   of the original template (using `pypdf` + `reportlab`) and returns the
   filled PDF, which the browser downloads automatically.

No data is stored anywhere — each request is generated and returned in memory.

## Running locally

```bash
cd invoice_app
pip install -r requirements.txt
python3 app.py
```

Then open **http://localhost:5000** in your browser.

## Deploying so others can use it via a link

The easiest free option is **Render**. Steps:

1. Create a free account at https://render.com
2. Push this `invoice_app` folder to a GitHub repository (or use Render's
   "Deploy from a folder" / drag-and-drop option if available on your plan).
3. In Render, click **New → Web Service**, connect the repo.
4. Render will detect `requirements.txt` automatically. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
     (this is already in the included `Procfile`, so Render may pick it up
     automatically)
5. Click **Create Web Service**. After the build finishes (1–3 minutes),
   Render gives you a public URL like `https://skt-invoice.onrender.com` —
   that's the link to share.

**Alternative platforms** that work the same way (push code, auto-detect
`Procfile`/`requirements.txt`): Railway (https://railway.app) and
Fly.io (https://fly.io). All have free tiers suitable for light, internal use.

> Note: on Render's free tier the app may "sleep" after periods of
> inactivity and take ~30–60 seconds to wake up on the next visit. This is
> normal for free hosting and does not affect the generated PDFs.

## Customizing

- **Template**: If the invoice template ever changes, replace `Format.pdf`
  and re-check/adjust the coordinates in `fill_pdf.py` (they're tied to the
  exact pixel positions of the original PDF's labels and table grid).
- **Max line items**: Currently capped at 10 (`MAX_ROWS` in `static/app.js`).
  Increase if needed — note that all items are fit into the single
  fixed-height row in the original template, so very high counts will
  render with a smaller font per row.
- **Tax rate**: IGST is hardcoded at 18% (`IGST_RATE` in `static/app.js`).
