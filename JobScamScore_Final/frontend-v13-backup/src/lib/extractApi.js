// Asks the backend (/api/extract) to read a screenshot, PDF or job link.
// It returns the job TEXT only. The engines run later, when you press Analyze.
const BASE = "http://127.0.0.1:5000";

async function handle(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `The server answered with status ${res.status}.`);
  return data;
}

export async function extractFromFile(file) {
  const body = new FormData();
  body.append("file", file);
  return handle(await fetch(`${BASE}/api/extract`, { method: "POST", body }));
}

export async function extractFromUrl(url) {
  return handle(await fetch(`${BASE}/api/extract`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  }));
}

// "Rs. 8,00,000" -> "800000".  "8 LPA" -> "800000".  Nothing found -> "".
export function parseSalary(text) {
  const digits = String(text || "").replace(/[^\d]/g, "");
  if (!digits) return "";
  let n = Number(digits);
  if (/lpa/i.test(text) && n < 1000) n *= 100000;
  return String(n);
}
