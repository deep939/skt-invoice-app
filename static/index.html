<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swathi Kiran Transport — Invoice Generator</title>
<style>
  :root {
    --ink: #1c1d1f;
    --paper: #faf8f5;
    --line: #d9d4cc;
    --line-strong: #b9b2a6;
    --accent: #b13c2f;
    --accent-dark: #8c2e23;
    --muted: #6b6660;
    --field-bg: #ffffff;
    --mono: "IBM Plex Mono", "SF Mono", Menlo, Consolas, monospace;
    --serif: "Source Serif 4", "Georgia", serif;
    --sans: "Inter", "Helvetica Neue", Arial, sans-serif;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    -webkit-font-smoothing: antialiased;
  }

  .topbar {
    border-bottom: 3px solid var(--ink);
    padding: 22px 28px 18px;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }

  .brand {
    display: flex;
    align-items: baseline;
    gap: 12px;
  }

  .brand .mark {
    font-family: var(--serif);
    font-weight: 700;
    font-size: 22px;
    letter-spacing: 0.01em;
  }

  .brand .mark span { color: var(--accent); }

  .brand .tag {
    font-family: var(--mono);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
  }

  .topbar .doc-label {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.08em;
    color: var(--muted);
    text-transform: uppercase;
  }

  main {
    max-width: 920px;
    margin: 0 auto;
    padding: 36px 24px 80px;
  }

  .lede {
    margin: 0 0 32px;
    font-family: var(--serif);
    font-size: 17px;
    line-height: 1.5;
    color: var(--ink);
    max-width: 58ch;
  }

  .lede strong { color: var(--accent-dark); }

  fieldset {
    border: none;
    margin: 0 0 36px;
    padding: 0;
  }

  legend {
    font-family: var(--mono);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--accent-dark);
    padding: 0 0 10px;
    border-bottom: 1px solid var(--line-strong);
    width: 100%;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  legend .num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--ink);
    color: var(--paper);
    font-size: 10px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px 24px;
  }

  .grid.cols-1 { grid-template-columns: 1fr; }

  .field { display: flex; flex-direction: column; gap: 6px; }
  .field.span-2 { grid-column: 1 / -1; }

  label {
    font-size: 12.5px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.01em;
  }

  label .opt {
    font-weight: 400;
    font-style: italic;
    color: #a39c8f;
    margin-left: 4px;
  }

  input[type="text"],
  input[type="date"],
  input[type="number"],
  textarea {
    font-family: var(--sans);
    font-size: 14.5px;
    padding: 10px 12px;
    border: 1.5px solid var(--line);
    border-radius: 3px;
    background: var(--field-bg);
    color: var(--ink);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }

  textarea { resize: vertical; min-height: 56px; font-family: var(--sans); }

  input:focus, textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(177, 60, 47, 0.12);
  }

  input::placeholder, textarea::placeholder { color: #b8b2a6; }

  /* ---- Line items table ---- */
  .items-wrap {
    border: 1.5px solid var(--line-strong);
    border-radius: 4px;
    overflow: hidden;
  }

  .items-head, .item-row {
    display: grid;
    grid-template-columns: 40px 1fr 70px 100px 90px 110px 36px;
    gap: 0;
    align-items: stretch;
  }

  .items-head {
    background: var(--ink);
    color: var(--paper);
    font-family: var(--mono);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .items-head > div {
    padding: 9px 10px;
    border-right: 1px solid rgba(255,255,255,0.12);
  }
  .items-head > div:last-child { border-right: none; }

  .item-row {
    border-top: 1px solid var(--line);
    background: var(--field-bg);
  }

  .item-row:nth-child(even) { background: #fdfcfa; }

  .item-row > div {
    padding: 7px 8px;
    border-right: 1px solid var(--line);
    display: flex;
    align-items: center;
  }
  .item-row > div:last-child { border-right: none; justify-content: center; }

  .item-row input {
    width: 100%;
    border: none;
    padding: 6px 4px;
    font-size: 13.5px;
    background: transparent;
  }
  .item-row input:focus {
    box-shadow: none;
    background: #fff6ee;
  }

  .item-row .sl-no {
    justify-content: center;
    font-family: var(--mono);
    color: var(--muted);
    font-size: 13px;
  }

  .remove-row {
    border: none;
    background: none;
    color: #b9b2a6;
    font-size: 18px;
    cursor: pointer;
    line-height: 1;
    padding: 2px 6px;
    border-radius: 3px;
  }
  .remove-row:hover { color: var(--accent); background: #f6e9e6; }
  .remove-row:disabled { opacity: 0.25; cursor: not-allowed; }

  .items-foot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: #f3efe8;
    border-top: 1px solid var(--line-strong);
  }

  .add-row-btn {
    font-family: var(--mono);
    font-size: 11.5px;
    letter-spacing: 0.04em;
    border: 1.5px dashed var(--line-strong);
    background: transparent;
    color: var(--accent-dark);
    padding: 7px 14px;
    border-radius: 3px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
  }
  .add-row-btn:hover { border-color: var(--accent); background: #fff6f0; }
  .add-row-btn:disabled { opacity: 0.4; cursor: not-allowed; }

  .row-count {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
  }

  /* ---- Totals summary ---- */
  .totals-panel {
    margin-top: 18px;
    display: grid;
    grid-template-columns: 1fr 220px;
    gap: 8px 0;
    max-width: 420px;
    margin-left: auto;
    font-family: var(--mono);
    font-size: 13px;
  }

  .totals-panel .t-label { color: var(--muted); padding: 5px 0; }
  .totals-panel .t-value { text-align: right; padding: 5px 0; font-weight: 600; }
  .totals-panel .t-grand {
    border-top: 1.5px solid var(--ink);
    margin-top: 4px;
    padding-top: 10px;
    font-size: 15px;
  }
  .totals-panel .t-grand .t-value { color: var(--accent-dark); }

  .words-row {
    margin-top: 14px;
    font-family: var(--serif);
    font-style: italic;
    font-size: 13.5px;
    color: var(--muted);
    text-align: right;
  }

  /* ---- Submit area ---- */
  .submit-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding-top: 24px;
    border-top: 1px solid var(--line);
    flex-wrap: wrap;
  }

  .submit-note {
    font-size: 12.5px;
    color: var(--muted);
    max-width: 40ch;
  }

  .submit-btn {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 14.5px;
    background: var(--ink);
    color: var(--paper);
    border: none;
    padding: 14px 28px;
    border-radius: 3px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    transition: background 0.15s ease, transform 0.1s ease;
    white-space: nowrap;
  }
  .submit-btn:hover { background: var(--accent-dark); }
  .submit-btn:active { transform: translateY(1px); }
  .submit-btn:disabled { background: #b9b2a6; cursor: wait; }

  .submit-btn .arrow { transition: transform 0.15s ease; }
  .submit-btn:hover .arrow { transform: translateX(3px); }

  /* ---- Status / error banner ---- */
  .status-banner {
    display: none;
    margin: 0 0 24px;
    padding: 13px 16px;
    border-radius: 3px;
    font-size: 13.5px;
    border: 1.5px solid;
  }
  .status-banner.show { display: block; }
  .status-banner.error {
    background: #fbeceb;
    border-color: #d98178;
    color: #7a2a20;
  }
  .status-banner.success {
    background: #ecf3ea;
    border-color: #8fae7c;
    color: #34541f;
  }

  .download-link {
    display: inline-block;
    margin-top: 8px;
    font-weight: 700;
    color: var(--accent-dark);
    text-decoration: underline;
  }

  @media (max-width: 720px) {
    .grid { grid-template-columns: 1fr; }
    .items-head, .item-row {
      grid-template-columns: 32px 1fr 56px 78px 78px 88px 28px;
      font-size: 11px;
    }
    .totals-panel { grid-template-columns: 1fr 160px; max-width: 100%; }
    .topbar { padding: 18px; }
    main { padding: 24px 16px 60px; }
  }

  @media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
  }
</style>
</head>
<body>

<div class="topbar">
  <div class="brand">
    <div class="mark">SKT <span>·</span> Swathi Kiran Transport</div>
  </div>
  <div class="doc-label">Tax Invoice Builder</div>
</div>

<main>
  <p class="lede">
    Fill in the details below and generate a ready-to-send
    <strong>Tax Invoice PDF</strong> in the official SKT format —
    no manual retyping into the template required.
  </p>

  <div class="status-banner" id="statusBanner"></div>

  <form id="invoiceForm">

    <fieldset>
      <legend><span class="num">1</span>Invoice Details</legend>
      <div class="grid">
        <div class="field">
          <label for="invoice_no">Invoice No.</label>
          <input type="text" id="invoice_no" name="invoice_no" placeholder="e.g. SKT/2026/045" required>
        </div>
        <div class="field">
          <label for="date">Date</label>
          <input type="date" id="date" name="date" required>
        </div>
      </div>
    </fieldset>

    <fieldset>
      <legend><span class="num">2</span>Billing &amp; Address</legend>
      <div class="grid">
        <div class="field span-2">
          <label for="billing_details">Billing Details</label>
          <input type="text" id="billing_details" name="billing_details" placeholder="Company / recipient name and GSTIN">
        </div>
        <div class="field span-2">
          <label for="address">Address</label>
          <textarea id="address" name="address" placeholder="Full billing address"></textarea>
        </div>
      </div>
    </fieldset>

    <fieldset>
      <legend><span class="num">3</span>Work Order Details</legend>
      <div class="grid">
        <div class="field">
          <label for="vendor_code">Vendor Code</label>
          <input type="text" id="vendor_code" name="vendor_code" placeholder="e.g. VND-101">
        </div>
        <div class="field">
          <label for="wo_no">WO No.</label>
          <input type="text" id="wo_no" name="wo_no" placeholder="Work order number">
        </div>
        <div class="field">
          <label for="wo_date">WO Date</label>
          <input type="date" id="wo_date" name="wo_date">
        </div>
        <div class="field">
          <label for="period_of_work">Period of Work</label>
          <input type="text" id="period_of_work" name="period_of_work" placeholder="e.g. June 2026">
        </div>
      </div>
    </fieldset>

    <fieldset>
      <legend><span class="num">4</span>Vendor</legend>
      <div class="grid">
        <div class="field">
          <label for="vendor_name">Vendor Name</label>
          <input type="text" id="vendor_name" name="vendor_name" placeholder="e.g. Swathi Kiran Transport" required>
        </div>
        <div class="field">
          <label for="vendor_gstin">Vendor GSTIN</label>
          <input type="text" id="vendor_gstin" name="vendor_gstin" placeholder="15-digit GSTIN">
        </div>
      </div>
    </fieldset>

    <fieldset>
      <legend><span class="num">5</span>Line Items</legend>

      <div class="items-wrap">
        <div class="items-head">
          <div>Sl.</div>
          <div>Item Description</div>
          <div>Qty</div>
          <div>Rate</div>
          <div>Discount</div>
          <div>Amount</div>
          <div></div>
        </div>
        <div id="itemsBody"><!-- rows injected by JS --></div>
      </div>

      <div class="items-foot">
        <button type="button" class="add-row-btn" id="addRowBtn">+ Add line item</button>
        <span class="row-count" id="rowCount">1 / 10 rows</span>
      </div>

      <div class="totals-panel">
        <div class="t-label">Subtotal (before tax)</div>
        <div class="t-value" id="sumSubtotal">0.00</div>

        <div class="t-label">IGST @ 18%</div>
        <div class="t-value" id="sumIgst">0.00</div>

        <div class="t-label t-grand">Total Invoice Value</div>
        <div class="t-value t-grand" id="sumTotal">0.00</div>
      </div>
      <div class="words-row" id="sumWords">Zero Only</div>
    </fieldset>

    <div class="submit-bar">
      <p class="submit-note">
        Amounts are calculated automatically from Qty, Rate and Discount.
        Review the figures, then generate your PDF.
      </p>
      <button type="submit" class="submit-btn" id="submitBtn">
        Generate Invoice PDF <span class="arrow">→</span>
      </button>
    </div>
  </form>
</main>

<script src="app.js"></script>
</body>
</html>
