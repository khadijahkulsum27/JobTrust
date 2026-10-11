// Dashboard + History data. (Kept in its own file so your existing api.js stays untouched.)
const BASE = "http://127.0.0.1:5000";

export async function fetchReports() {
  const res = await fetch(`${BASE}/api/reports`);
  if (!res.ok) throw new Error(`The server answered with status ${res.status}.`);
  return res.json();
}

// One past report. The database stores it flat, so we only gather the pieces.
export async function fetchReport(id) {
  const res = await fetch(`${BASE}/api/reports/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error(`The server answered with status ${res.status}.`);
  const raw = await res.json();
  const r = raw.report || {};
  const f = raw.findings || {};
  return {
    submission: raw.submission || {},
    report: {
      processing_id: id,
      trust_score: r.trust_score,
      decision: r.decision,
      risk: r.risk,
      confidence: r.confidence,
      summary: r.summary,
      recommendation: r.recommendation,
      engine_findings: f.engine_findings || [],
      positive_findings: f.positive_findings || [],
      negative_findings: f.negative_findings || [],
      uncertain_findings: f.uncertain_findings || [],
      conflict_findings: f.conflict_findings || [],
    },
  };
}
