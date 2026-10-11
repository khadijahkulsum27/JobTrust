// History lives in THIS BROWSER. Every finished scan is saved here, so the
// History and Dashboard pages work even though the backend has no history route.
// If the backend ever gets /api/reports, its rows are merged in automatically.
import { fetchReports } from "./reportsApi.js";

const KEY = "jobtrust_history";

function getLocal() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}

export function saveLocal(row) {
  const rows = [row, ...getLocal().filter((r) => r.processing_id !== row.processing_id)].slice(0, 200);
  try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch { /* storage full or blocked */ }
}

export async function loadHistory() {
  const local = getLocal();
  let remote = [];
  try { remote = await fetchReports(); } catch { /* backend history is optional */ }
  const seen = new Set(local.map((r) => r.processing_id));
  return [...local, ...remote.filter((r) => !seen.has(r.processing_id))]
    .sort((a, b) => new Date(b.created_timestamp) - new Date(a.created_timestamp));
}
