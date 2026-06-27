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

PAGE_W, PAGE_H = 595.32, 841.92
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "Format.pdf")

F = "Helvetica"
FB = "Helvetica-Bold"


def y(top):
    """Convert a pdfplumber 'top' (distance from top of page) to a reportlab
    y-coordinate (distance from bottom of page)."""
    return PAGE_H - top


def draw_text(c, x, baseline, text, size=9, font=F, max_width=None, align="left"):
    """Draw a single line of text at a given baseline (pdfplumber 'bottom'
    coordinate of the text). Shrinks font to fit max_width if needed."""
    if text is None:
        text = ""
    text = str(text)
    if not text:
        return
    c.setFont(font, size)
    if max_width:
        while c.stringWidth(text, font, size) > max_width and size > 5:
            size -= 0.5
            c.setFont(font, size)
    if align == "left":
        c.drawString(x, y(baseline), text)
    elif align == "center":
        c.drawCentredString(x, y(baseline), text)
    elif align == "right":
        c.drawRightString(x, y(baseline), text)


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


def whiteout(c, x0, top0, x1, top1, pad=1.5):
    """Paint a white rectangle over a region of the original template,
    specified in pdfplumber top-down coordinates, so we can redraw that
    label ourselves (e.g. to make it bold or change its wording)."""
    c.setFillColorRGB(1, 1, 1)
    c.rect(x0 - pad, y(top1) - pad, (x1 - x0) + 2 * pad, (top1 - top0) + 2 * pad,
           fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)


def build_overlay(data: dict) -> bytes:
    """data: dict of invoice fields (see app.py for schema). Returns overlay PDF bytes."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))

    LABEL_SIZE = 9.5
    VALUE_SIZE = 9.5

    # ============================================================
    # Row 1: Invoice No / Date  (row 167.8-182.2); baseline nudged up
    # 2pt from the row's bottom border (182.2) for clean visual spacing
    # ============================================================
    INV_BASELINE = 179.2
    whiteout(c, 33.0, 169.0, 97.6, 181.2)
    draw_text(c, 33, INV_BASELINE, "Invoice No:", size=LABEL_SIZE, font=FB)
    draw_text(c, 102, INV_BASELINE, data.get("invoice_no", ""), size=VALUE_SIZE, font=F, max_width=290)

    whiteout(c, 427.6, 169.0, 461.5, 181.2)
    draw_text(c, 427.6, INV_BASELINE, "Date :", size=LABEL_SIZE, font=FB)
    draw_text(c, 465, INV_BASELINE, data.get("date", ""), size=VALUE_SIZE, font=F, max_width=90)

    # ============================================================
    # Billing Details: label row 182.2-196.6; baseline nudged up 2pt
    # from the row's bottom border (196.6). Value goes in the blank
    # row below it, 196.6-211.0 (baseline 207.5)
    # ============================================================
    BILLING_LABEL_BASELINE = 194.5
    whiteout(c, 33.0, 184.0, 108.5, 196.6)
    draw_text(c, 33, BILLING_LABEL_BASELINE, "Billing Details", size=LABEL_SIZE, font=FB)

    billing_lines = wrap_text(c, data.get("billing_details", ""), F, VALUE_SIZE, 500)
    draw_text(c, 33, 207.5, billing_lines[0] if billing_lines else "", size=VALUE_SIZE, font=F, max_width=500)
    if len(billing_lines) > 1:
        draw_text(c, 33, 220.0, " ".join(billing_lines[1:]), size=7.5, font=F, max_width=500)

    # ============================================================
    # Address: label on row 225.4-241.7; baseline nudged up 1.5pt from
    # the original 238.8 for consistent clearance. Value starts right
    # after the colon, continuation lines below (252.7/266.0/279.3)
    # ============================================================
    ADDR_BASELINE = 237.3
    whiteout(c, 33.0, 226.5, 93.6, 238.8)
    draw_text(c, 33, ADDR_BASELINE, "Address :", size=LABEL_SIZE, font=FB)

    addr_lines = wrap_text(c, data.get("address", ""), F, VALUE_SIZE, 215)
    addr_row_baselines = [ADDR_BASELINE, 252.7, 266.0, 279.3]
    for i, line in enumerate(addr_lines[:4]):
        x_pos = 100 if i == 0 else 33
        draw_text(c, x_pos, addr_row_baselines[i], line, size=VALUE_SIZE, font=F,
                   max_width=(216 if i == 0 else 280))

    # ============================================================
    # Right column: Vendor Code / WO No / WO Date / Period of Work
    # ============================================================
    whiteout(c, 326.5, 227.4, 385.8, 236.4)
    draw_text(c, 326.5, 236.4, "Vendor Code:", size=LABEL_SIZE, font=FB)
    draw_text(c, 392, 236.4, data.get("vendor_code", ""), size=VALUE_SIZE, font=F, max_width=160)

    whiteout(c, 326.5, 243.7, 359.8, 252.7)
    draw_text(c, 326.5, 252.7, "WO No:", size=LABEL_SIZE, font=FB)
    draw_text(c, 365, 252.7, data.get("wo_no", ""), size=VALUE_SIZE, font=F, max_width=185)

    whiteout(c, 326.5, 257.0, 368.7, 266.0)
    draw_text(c, 326.5, 266.0, "WO Date:", size=LABEL_SIZE, font=FB)
    draw_text(c, 374, 266.0, data.get("wo_date", ""), size=VALUE_SIZE, font=F, max_width=178)

    whiteout(c, 326.5, 270.3, 393.9, 279.3)
    draw_text(c, 326.5, 279.3, "Period of Work:", size=LABEL_SIZE, font=FB)
    draw_text(c, 400, 279.3, data.get("period_of_work", ""), size=VALUE_SIZE, font=F, max_width=150)

    # ============================================================
    # Vendor Name row (285.9-302.9): per request, do NOT print the
    # "Vendor Name" label — show only the value, centered in the band.
    # Baseline nudged up 2pt from the row's bottom border (302.9).
    # ============================================================
    whiteout(c, 28.6, 286.4, 555.9, 302.4, pad=0.0)
    draw_text(c, 292, 300.0, data.get("vendor_name", ""), size=11, font=FB, align="center", max_width=520)

    # ============================================================
    # GSTIN row (302.9-316.6): relabel "Vendor GSTIN:" -> "GSTIN:"
    # Baseline nudged up 2pt from the row's bottom border (316.6).
    # ============================================================
    whiteout(c, 254.0, 304.0, 330.4, 316.6)
    draw_text(c, 254, 313.5, "GSTIN:", size=LABEL_SIZE, font=FB)
    draw_text(c, 296, 313.5, data.get("vendor_gstin", ""), size=VALUE_SIZE, font=F, max_width=255)

    # ============================================================
    # Line items table
    # Columns: SL.No 28-68.4 | Item Desc 68.9-263.2 | Qty 263.7-332
    # | Rate 332.5-404 | Discount 404.5-476 | Amount 476.5-556.4
    # Single tall blank row in template: 340.6 -> 391.8 (51pt), subdivided
    # evenly into N equal-height sub-rows, each laid out as ONE line:
    # description + qty + rate + discount + amount all on the same baseline.
    # ============================================================
    items = data.get("items", []) or []
    n = max(len(items), 1)

    row_top = 340.6
    row_bottom = 391.8

    # The template's single "blank" items area actually contains a hidden
    # internal horizontal rule at 353.9-354.4 (a leftover from the original
    # 2-row design) that we don't want competing with our own row dividers.
    # Paint over it before drawing anything else in this block.
    whiteout(c, 28.1, 353.9, 556.4, 354.4, pad=0.3)

    row_h = (row_bottom - row_top) / n

    # Font size degrades gracefully as more items are packed into the fixed
    # 51.2pt block, with a 6.5pt floor that stays legible when printed.
    if row_h >= 16:
        item_font_size = 9.0
    elif row_h >= 11:
        item_font_size = 8.0
    elif row_h >= 8:
        item_font_size = 7.5
    elif row_h >= 6.2:
        item_font_size = 7.0
    else:
        item_font_size = 6.5

    # Divider lines between rows only when there's enough row height to fit
    # the font comfortably above them with clearance; below that threshold
    # we skip dividers altogether (a tightly packed list reads better than
    # rows with text crowding right up against grid lines).
    draw_dividers = row_h >= (item_font_size + 3)

    col_x = {"sl": 33, "desc": 73, "qty": 288, "rate": 340, "discount": 412, "amount": 482}
    col_w = {"desc": 185, "qty": 60, "rate": 60, "discount": 58, "amount": 70}

    c.setLineWidth(0.4)
    for i in range(n):
        item = items[i] if i < len(items) else {}
        row_a = row_top + row_h * i
        row_b = row_top + row_h * (i + 1)
        # baseline offset from the row's bottom edge: enough clearance for
        # the font's descender, capped so it never exceeds the row itself
        offset = min(row_h * 0.4, item_font_size * 0.55 + 1.0)
        offset = max(offset, item_font_size * 0.3)
        baseline = row_b - offset

        draw_text(c, col_x["sl"], baseline, item.get("sl_no", i + 1), size=item_font_size, font=F)
        draw_text(c, col_x["desc"], baseline, item.get("description", ""), size=item_font_size, font=F, max_width=col_w["desc"])
        draw_text(c, col_x["qty"], baseline, item.get("qty", ""), size=item_font_size, font=F, max_width=col_w["qty"])
        draw_text(c, col_x["rate"], baseline, fmt_money(item.get("rate", "")), size=item_font_size, font=F, max_width=col_w["rate"])
        draw_text(c, col_x["discount"], baseline, fmt_money(item.get("discount", "")), size=item_font_size, font=F, max_width=col_w["discount"])
        draw_text(c, col_x["amount"], baseline, fmt_money(item.get("amount", "")), size=item_font_size, font=F, max_width=col_w["amount"])

        # divider line between sub-rows (not after the last one; template's
        # own border already closes the bottom of the block). Skipped when
        # rows are too tight to fit text with clearance above the line.
        if i < n - 1 and draw_dividers:
            c.line(28.1, y(row_b), 556.4, y(row_b))

    # ============================================================
    # IGST row (392.3 -> 429.9); amount goes in Amount column
    # ============================================================
    draw_text(c, col_x["amount"], 417.0, fmt_money(data.get("igst_amount", "")), size=9, font=F, max_width=col_w["amount"])

    # ============================================================
    # TOTAL row (430.4 -> 453.7)
    # ============================================================
    draw_text(c, col_x["rate"], 451.0, fmt_money(data.get("total_rate", "")), size=9, font=FB, max_width=col_w["rate"])
    draw_text(c, col_x["discount"], 451.0, fmt_money(data.get("total_discount", "")), size=9, font=FB, max_width=col_w["discount"])
    draw_text(c, col_x["amount"], 451.0, fmt_money(data.get("total_amount", "")), size=9, font=FB, max_width=col_w["amount"])

    # ============================================================
    # Total Invoice Value (In Figure) (rows 492.7 -> 507.7)
    # ============================================================
    draw_text(c, 270, 504.4, fmt_money(data.get("total_in_figure", "")), size=10, font=FB)

    # ============================================================
    # Total Invoice Value (In Words) (rows 508.1 -> 540.4)
    # ============================================================
    words_lines = wrap_text(c, data.get("total_in_words", ""), F, 9, 280)
    word_tops = [530.1, 543.0]
    for i, line in enumerate(words_lines[:2]):
        draw_text(c, 270, word_tops[i], line, size=9, font=F)

    c.save()
    buf.seek(0)
    return buf.read()


def build_border_overlay() -> bytes:
    """A few of the original template's border lines are built from many
    short, thin rect segments stacked end-to-end. When merged together
    with the data overlay in a single content stream, some of those
    segments can lose rendering fidelity and leave visible gaps (seen at
    the left edge near "Invoice No"/"Billing Details" and at the
    header/first-item-row divider in the line items table). Drawing
    these specific lines in their own separate overlay, merged onto the
    page as an independent pass, avoids that interaction entirely and
    guarantees crisp, continuous borders."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(PAGE_W, PAGE_H))
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.6)
    c.line(28.1, y(136.8), 28.1, y(540.4))      # left outer border, full table height
    c.line(556.4, y(136.8), 556.4, y(540.4))    # right outer border, full table height
    c.line(28.1, y(340.6), 556.4, y(340.6))     # header row / first item row divider
    c.save()
    buf.seek(0)
    return buf.read()


def fill_invoice_pdf(data: dict) -> bytes:
    overlay_bytes = build_overlay(data)
    overlay_reader = PdfReader(io.BytesIO(overlay_bytes))

    border_overlay_bytes = build_border_overlay()
    border_reader = PdfReader(io.BytesIO(border_overlay_bytes))

    base_reader = PdfReader(TEMPLATE_PATH)

    writer = PdfWriter()
    base_page = base_reader.pages[0]
    base_page.merge_page(overlay_reader.pages[0])
    base_page.merge_page(border_reader.pages[0])
    writer.add_page(base_page)

    for p in base_reader.pages[1:]:
        writer.add_page(p)

    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return out.read()
