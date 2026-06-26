// ---- Config ----
const MAX_ROWS = 10;
const IGST_RATE = 0.18;
const API_ENDPOINT = "/api/generate-invoice";

const itemsBody = document.getElementById("itemsBody");
const addRowBtn = document.getElementById("addRowBtn");
const rowCountEl = document.getElementById("rowCount");
const form = document.getElementById("invoiceForm");
const submitBtn = document.getElementById("submitBtn");
const statusBanner = document.getElementById("statusBanner");

let rowIdSeq = 0;

function createRow() {
  rowIdSeq += 1;
  const id = rowIdSeq;
  const row = document.createElement("div");
  row.className = "item-row";
  row.dataset.rowId = id;
  row.innerHTML = `
    <div class="sl-no"></div>
    <div><input type="text" class="f-desc" placeholder="Description of work / goods"></div>
    <div><input type="number" class="f-qty" placeholder="0" min="0" step="any"></div>
    <div><input type="number" class="f-rate" placeholder="0.00" min="0" step="0.01"></div>
    <div><input type="number" class="f-discount" placeholder="0.00" min="0" step="0.01"></div>
    <div class="f-amount-display">0.00</div>
    <div><button type="button" class="remove-row" title="Remove row">&times;</button></div>
  `;
  itemsBody.appendChild(row);

  row.querySelectorAll("input").forEach((inp) => {
    inp.addEventListener("input", recalcAll);
  });
  row.querySelector(".remove-row").addEventListener("click", () => {
    row.remove();
    renumberRows();
    recalcAll();
  });

  renumberRows();
  updateAddButtonState();
}

function renumberRows() {
  const rows = itemsBody.querySelectorAll(".item-row");
  rows.forEach((row, idx) => {
    row.querySelector(".sl-no").textContent = idx + 1;
    row.querySelector(".remove-row").disabled = rows.length === 1;
  });
  rowCountEl.textContent = `${rows.length} / ${MAX_ROWS} rows`;
}

function updateAddButtonState() {
  const count = itemsBody.querySelectorAll(".item-row").length;
  addRowBtn.disabled = count >= MAX_ROWS;
}

addRowBtn.addEventListener("click", () => {
  if (itemsBody.querySelectorAll(".item-row").length < MAX_ROWS) {
    createRow();
  }
});

function fmt(n) {
  if (!isFinite(n)) n = 0;
  return n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function recalcAll() {
  let subtotal = 0;
  const rows = itemsBody.querySelectorAll(".item-row");
  rows.forEach((row) => {
    const qty = parseFloat(row.querySelector(".f-qty").value) || 0;
    const rate = parseFloat(row.querySelector(".f-rate").value) || 0;
    const discount = parseFloat(row.querySelector(".f-discount").value) || 0;
    const amount = qty * rate - discount;
    row.querySelector(".f-amount-display").textContent = fmt(amount);
    subtotal += amount;
  });

  const igst = subtotal * IGST_RATE;
  const total = subtotal + igst;

  document.getElementById("sumSubtotal").textContent = fmt(subtotal);
  document.getElementById("sumIgst").textContent = fmt(igst);
  document.getElementById("sumTotal").textContent = fmt(total);
  document.getElementById("sumWords").textContent = numberToWords(Math.round(total)) + " Only";

  updateAddButtonState();
}

// ---- Number to words (Indian numbering system) ----
function numberToWords(num) {
  if (num === 0) return "Zero";
  const ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
    "Eighteen", "Nineteen"];
  const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];

  function twoDigits(n) {
    if (n < 20) return ones[n];
    return tens[Math.floor(n / 10)] + (n % 10 ? " " + ones[n % 10] : "");
  }
  function threeDigits(n) {
    if (n < 100) return twoDigits(n);
    return ones[Math.floor(n / 100)] + " Hundred" + (n % 100 ? " " + twoDigits(n % 100) : "");
  }

  let result = "";
  const crore = Math.floor(num / 10000000);
  num %= 10000000;
  const lakh = Math.floor(num / 100000);
  num %= 100000;
  const thousand = Math.floor(num / 1000);
  num %= 1000;
  const hundred = num;

  if (crore) result += threeDigits(crore) + " Crore ";
  if (lakh) result += threeDigits(lakh) + " Lakh ";
  if (thousand) result += threeDigits(thousand) + " Thousand ";
  if (hundred) result += threeDigits(hundred);

  return result.trim() || "Zero";
}

// ---- Status banner ----
function showStatus(type, html) {
  statusBanner.className = `status-banner show ${type}`;
  statusBanner.innerHTML = html;
}
function hideStatus() {
  statusBanner.className = "status-banner";
  statusBanner.innerHTML = "";
}

// ---- Form submit ----
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideStatus();

  const rows = Array.from(itemsBody.querySelectorAll(".item-row"));
  const items = rows.map((row, idx) => {
    const qty = parseFloat(row.querySelector(".f-qty").value) || 0;
    const rate = parseFloat(row.querySelector(".f-rate").value) || 0;
    const discount = parseFloat(row.querySelector(".f-discount").value) || 0;
    return {
      sl_no: idx + 1,
      description: row.querySelector(".f-desc").value.trim(),
      qty: qty,
      rate: rate,
      discount: discount,
      amount: qty * rate - discount,
    };
  });

  const subtotal = items.reduce((s, it) => s + it.amount, 0);
  const igst = subtotal * IGST_RATE;
  const total = subtotal + igst;

  const totalRate = items.reduce((s, it) => s + it.qty * it.rate, 0);
  const totalDiscount = items.reduce((s, it) => s + it.discount, 0);

  const payload = {
    invoice_no: document.getElementById("invoice_no").value.trim(),
    date: formatDateDisplay(document.getElementById("date").value),
    billing_details: document.getElementById("billing_details").value.trim(),
    address: document.getElementById("address").value.trim(),
    vendor_code: document.getElementById("vendor_code").value.trim(),
    wo_no: document.getElementById("wo_no").value.trim(),
    wo_date: formatDateDisplay(document.getElementById("wo_date").value),
    period_of_work: document.getElementById("period_of_work").value.trim(),
    vendor_name: document.getElementById("vendor_name").value.trim(),
    vendor_gstin: document.getElementById("vendor_gstin").value.trim(),
    items: items,
    igst_amount: igst,
    total_rate: totalRate,
    total_discount: totalDiscount,
    total_amount: total,
    total_in_figure: fmt(total),
    total_in_words: numberToWords(Math.round(total)) + " Only",
  };

  if (!payload.invoice_no || !payload.date) {
    showStatus("error", "Please fill in at least the Invoice No. and Date before generating the PDF.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Generating…";

  try {
    const res = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      let msg = "Something went wrong while generating the PDF.";
      try {
        const errJson = await res.json();
        if (errJson.error) msg = errJson.error;
      } catch (_) {}
      throw new Error(msg);
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const safeInvoiceNo = (payload.invoice_no || "output").replace(/[^A-Za-z0-9_-]+/g, "_");
    const filename = `Invoice_${safeInvoiceNo}.pdf`;

    showStatus(
      "success",
      `Your invoice PDF is ready. <a class="download-link" id="dlLink" href="${url}" download="${filename}">Download ${filename}</a>`
    );

    // auto-trigger download as well
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (err) {
    showStatus("error", `Couldn't generate the PDF: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Generate Invoice PDF <span class="arrow">→</span>';
  }
});

function formatDateDisplay(isoDate) {
  if (!isoDate) return "";
  const [y, m, d] = isoDate.split("-");
  if (!y || !m || !d) return isoDate;
  return `${d}-${m}-${y}`;
}

// ---- Init ----
createRow();
recalcAll();

// default date to today
(function setDefaultDate() {
  const today = new Date();
  const iso = today.toISOString().slice(0, 10);
  document.getElementById("date").value = iso;
})();
