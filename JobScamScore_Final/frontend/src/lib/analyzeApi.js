// Sends a job to the backend and reshapes the answer for the report page.
const BASE = "http://127.0.0.1:5000";

export async function analyzeJob(payload) {
  const res = await fetch(`${BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`The server answered with status ${res.status}.`);
  return res.json();
}

// /api/analyze nests the score under trust_assessment. Flatten it.
export function normalizeAnalyze(raw) {
  const d = raw && raw.engine6 && raw.engine6.data;
  if (!d) throw new Error("The server replied, but the final report (engine 6) was missing.");
  const t = d.trust_assessment || {};
  return {
    processing_id: raw.processing_id,
    trust_score: t.trust_score,
    decision: t.decision,
    risk: t.risk,
    confidence: t.confidence,
    summary: d.summary,
    recommendation: d.recommendation,
    engine_findings: d.engine_findings || [],
    positive_findings: d.positive_findings || [],
    negative_findings: d.negative_findings || [],
    uncertain_findings: d.uncertain_findings || [],
    conflict_findings: d.conflict_findings || [],
  };
}
