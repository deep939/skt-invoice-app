"""
Fills the SKT Tax Invoice PDF template with user-supplied data by overlaying
text at coordinates matched to the original PDF's table grid.

Coordinates were derived from pdfplumber inspection of Format.pdf
(page size: 595.32 x 841.92 pts).
"""
import io
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

PAGE_W, PAGE_H = 595.32, 841.92
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "Format.pdf")

# pdfplumber gives "top" (distance from top of page). reportlab draws from
# the bottom-left, so y_reportlab = PAGE_H - top_from_plumber.
def y(top):
    return PAGE_H - top


def draw_text(c, x, top_baseline, text, size=9, font="Helvetica", max_width=None):
    """Draw a single line of text. top_baseline = pdfplumber 'bottom' coordinate
    of the row's text baseline area (we pass the row's bottom-of-text-line value)."""
    if text is None:
        text = ""
    text = str(text)
    c.setFont(font, size)
    if max_width:
        # shrink font to fit if needed
        while c.stringWidth(text, font, size) > max_width and size > 5:
            size -= 0.5
            c.setFont(font, size)
    c.drawString(x, y(top_baseline), text)


def wrap_text(c, text, font, size, max_width):
    """Greedy word-wrap; returns list of lines that fit within max_width."""
    if not text:
        return [""]
    words = str(text).split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def fmt_money(val):
    try:
        v = float(val)
        return f"{v:,.2f}"
    except (TypeError, ValueError):
        return str(val) if val else ""


def build_overlay(data: dict) -> bytes:
    """data: dict of invoice fields (see app.py for schema). Returns overlay PDF bytes."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    F = "Helvetica"
    FB = "Helvetica-Bold"

    # ---- Header row: Invoice No / Date (row 167.8 -> 182.2), baseline 181.2 ----
    draw_text(c, 100, 181.2, data.get("invoice_no", ""), size=9, font=F)
    draw_text(c, 465, 181.2, data.get("date", ""), size=9, font=F)

    # ---- Billing Details: row 182.2-196.6 is ONLY the "Billing Details" label.
    # The actual value is written into the two blank rows below it:
    # 196.6-211.0 (baseline 207.5) and 211.0-225.4... but 211.0-225.4 is shared with
    # "Address :" label, so only ONE full blank row (196.6-211.0) is available for
    # billing details before Address begins. ----
    billing_lines = wrap_text(c, data.get("billing_details", ""), F, 9, 500)
    draw_text(c, 33, 207.5, billing_lines[0] if billing_lines else "", size=9, font=F, max_width=500)
    # if there's a second line, place it in small font right under the label as a
    # fallback (rare case of very long billing details)
    if len(billing_lines) > 1:
        draw_text(c, 33, 193.5, " ".join(billing_lines[1:]), size=7.5, font=F, max_width=500)

    # ---- Address: "Address :" label is on row 225.4-241.7 (baseline 238.8); value
    # starts right after the colon on this same line. If it wraps, continuation lines
    # use the blank left-column space in rows 241.7-254.9, 254.9-268.1, 268.1-285.9
    # (baselines 252.7, 266.0, 279.3) - same baselines as the right-side WO labels
    # since they're row-aligned. ----
    addr_lines = wrap_text(c, data.get("address", ""), F, 9, 215)
    addr_row_baselines = [238.8, 252.7, 266.0, 279.3]
    for i, line in enumerate(addr_lines[:4]):
        x_pos = 96 if i == 0 else 33
        draw_text(c, x_pos, addr_row_baselines[i], line, size=9, font=F, max_width=(220 if i == 0 else 280))

    # ---- Right column fields: Vendor Code / WO No / WO Date / Period of Work ----
    draw_text(c, 390, 236.4, data.get("vendor_code", ""), size=9, font=F, max_width=160)
    draw_text(c, 363, 252.7, data.get("wo_no", ""), size=9, font=F, max_width=185)
    draw_text(c, 372, 266.0, data.get("wo_date", ""), size=9, font=F, max_width=178)
    draw_text(c, 398, 279.3, data.get("period_of_work", ""), size=9, font=F, max_width=152)

    # ---- Vendor Name (label row 285.9-302.9, baseline 301.5, centered label at
    # x~250-334). Value is written to the right of the label. ----
    draw_text(c, 345, 301.5, data.get("vendor_name", ""), size=10, font=FB, max_width=205)

    # ---- Vendor GSTIN (row 302.9-316.6, baseline 315.1): value after the label ----
    draw_text(c, 335, 315.1, data.get("vendor_gstin", ""), size=9, font=F, max_width=215)

    # ---- Line items table ----
    # Column x-starts (from grid): SL.No 28-68.4 | Item Desc 68.9-263.2 | Qty 263.7-332
    # | Rate 332.5-404 | Discount 404.5-476 | Amount 476.5-556.4
    # The template provides exactly ONE tall blank row for items: 340.6 -> 391.8 (51pt).
    # We subdivide this single row evenly into N sub-rows for N line items, drawing thin
    # divider lines between them so multiple items remain visually distinct.
    items = data.get("items", []) or []
    n = max(len(items), 1)

    row_top = 340.6
    row_bottom = 391.8
    available_height = row_bottom - row_top
    row_h = available_height / n
    item_font_size = 9 if row_h >= 11 else max(5.5, 9 * (row_h / 11))

    col_x = {"sl": 33, "desc": 73, "qty": 288, "rate": 340, "discount": 412, "amount": 482}
    col_w = {"desc": 185, "qty": 60, "rate": 60, "discount": 58, "amount": 70}

    c.setLineWidth(0.4)
    for i in range(n):
        item = items[i] if i < len(items) else {}
        row_start = row_top + row_h * i
        row_end = row_top + row_h * (i + 1)
        # baseline offset scales with row height so it never exceeds the row itself;
        # for tall rows (single item) it sits comfortably above the bottom border,
        # for short rows (many items) it sits just above the divider line.
        baseline_offset = min(5.5, row_h * 0.35)
        baseline_top = row_end - baseline_offset

        draw_text(c, col_x["sl"], baseline_top, item.get("sl_no", i + 1), size=item_font_size, font=F)

        if row_h >= 22:
            # enough room to wrap description across multiple lines within the row
            desc_lines = wrap_text(c, item.get("description", ""), F, item_font_size, col_w["desc"])
            line_gap = max(item_font_size + 1.5, 9)
            max_lines = max(1, int(row_h // line_gap))
            first_line_top = row_start + line_gap
            for li, dl in enumerate(desc_lines[:max_lines]):
                lt = first_line_top + line_gap * li
                if lt > row_end - 4:
                    break
                draw_text(c, col_x["desc"], lt, dl, size=item_font_size, font=F)
        else:
            # short row: single truncated/shrunk line, vertically matched to baseline_top
            draw_text(c, col_x["desc"], baseline_top, item.get("description", ""), size=item_font_size, font=F, max_width=col_w["desc"])

        draw_text(c, col_x["qty"], baseline_top, item.get("qty", ""), size=item_font_size, font=F, max_width=col_w["qty"])
        draw_text(c, col_x["rate"], baseline_top, fmt_money(item.get("rate", "")), size=item_font_size, font=F, max_width=col_w["rate"])
        draw_text(c, col_x["discount"], baseline_top, fmt_money(item.get("discount", "")), size=item_font_size, font=F, max_width=col_w["discount"])
        draw_text(c, col_x["amount"], baseline_top, fmt_money(item.get("amount", "")), size=item_font_size, font=F, max_width=col_w["amount"])

        # divider line between sub-rows (skip after last row, template already has the border)
        if i < n - 1:
            c.line(28.1, y(row_end), 556.4, y(row_end))

    # ---- IGST row (392.3 -> 429.9); amount goes in Amount column ----
    draw_text(c, col_x["amount"], 417.0, fmt_money(data.get("igst_amount", "")), size=9, font=F, max_width=col_w["amount"])

    # ---- TOTAL row (430.4 -> 453.7) ----
    draw_text(c, col_x["rate"], 451.0, fmt_money(data.get("total_rate", "")), size=9, font=FB, max_width=col_w["rate"])
    draw_text(c, col_x["discount"], 451.0, fmt_money(data.get("total_discount", "")), size=9, font=FB, max_width=col_w["discount"])
    draw_text(c, col_x["amount"], 451.0, fmt_money(data.get("total_amount", "")), size=9, font=FB, max_width=col_w["amount"])

    # ---- Total Invoice Value (In Figure) (rows 492.7 -> 507.7) ----
    draw_text(c, 270, 504.4, fmt_money(data.get("total_in_figure", "")), size=10, font=FB)

    # ---- Total Invoice Value (In Words) (rows 508.1 -> 540.4) ----
    words_lines = wrap_text(c, data.get("total_in_words", ""), F, 9, 280)
    word_tops = [530.1, 543.0]
    for i, line in enumerate(words_lines[:2]):
        draw_text(c, 270, word_tops[i], line, size=9, font=F)

    c.save()
    buf.seek(0)
    return buf.read()


def fill_invoice_pdf(data: dict) -> bytes:
    overlay_bytes = build_overlay(data)
    overlay_reader = PdfReader(io.BytesIO(overlay_bytes))
    base_reader = PdfReader(TEMPLATE_PATH)

    writer = PdfWriter()
    base_page = base_reader.pages[0]
    base_page.merge_page(overlay_reader.pages[0])
    writer.add_page(base_page)

    # include any extra pages from template untouched (none expected here)
    for p in base_reader.pages[1:]:
        writer.add_page(p)

    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return out.read()
