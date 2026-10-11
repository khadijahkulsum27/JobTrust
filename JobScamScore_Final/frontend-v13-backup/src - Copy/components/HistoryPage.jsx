import { useEffect, useState } from "react";
import { fetchReport } from "../lib/reportsApi.js";
import { loadHistory } from "../lib/history.js";
import { getSaved, toggleSaved, downloadJson } from "../lib/saved.js";
import { DECISION } from "../lib/format.js";
import ReportView from "./ReportView.jsx";

const FILTERS = [["ALL", "All"], ["TRUSTED", "Trusted"], ["REVIEW", "Needs review"], ["HIGH_RISK", "High risk"], ["SAVED", "★ Saved"]];

export default function HistoryPage() {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("ALL");
  const [saved, setSaved] = useState(getSaved());
  const [open, setOpen] = useState(null); // { submission, report }
  const [opening, setOpening] = useState(false);

  useEffect(() => {
    loadHistory().then(setRows);
  }, []);

  async function openReport(id) {
    const row = rows.find((r) => r.processing_id === id);
    if (row && row.report) return setOpen({ submission: row.submission || row, report: row.report });
    setOpening(true); setError("");
    try { setOpen(await fetchReport(id)); } catch (e) { setError(e.message); }
    setOpening(false);
  }

  if (open) {
    const s = open.submission;
    return (
      <>
        <h1 className="page-title">{s.job_title || "Past report"}</h1>
        <p className="muted hist-sub">{s.company_name}</p>
        <ReportView report={open.report} onReset={() => setOpen(null)} resetLabel="Back to history" />
      </>
    );
  }

  const list = rows || [];
  const count = (d) => list.filter((r) => r.decision === d).length;
  const shown = list.filter((r) => {
    const text = (r.job_title + " " + r.company_name).toLowerCase();
    const okFilter = filter === "ALL" ? true : filter === "SAVED" ? saved.includes(r.processing_id) : r.decision === filter;
    return okFilter && text.includes(query.trim().toLowerCase());
  });

  return (
    <>
      <h1 className="page-title">Every job you've checked</h1>
      <p className="muted hist-sub">Open a report, star the ones you want to keep, and back them up. Reports are saved in this browser.</p>

      <div className="hist-stats">
        {[["Total scans", list.length, ""], ["Trusted", count("TRUSTED"), "t-good"], ["Needs review", count("REVIEW"), "t-warn"], ["High risk", count("HIGH_RISK"), "t-bad"]].map(([name, n, cls]) => (
          <div className="tile" key={name}><strong className={cls}>{rows ? n : "–"}</strong><span>{name}</span></div>
        ))}
      </div>

      {error && <div className="notice" role="alert"><strong>Something went wrong.</strong> {error} Is Flask running at http://127.0.0.1:5000?</div>}

      <div className="tile hist-tools">
        <input className="hist-search" type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search by job title or company…" aria-label="Search history" />
        <div className="chips">
          {FILTERS.map(([key, label]) => (
            <button key={key} className={"chip" + (filter === key ? " on" : "")} onClick={() => setFilter(key)}>
              {label}{key === "SAVED" ? ` (${saved.length})` : ""}
            </button>
          ))}
        </div>
        <div className="hist-meta">
          <span className="muted">{rows ? `${shown.length} of ${list.length} scans` : "Loading…"}</span>
          <button className="link-btn" disabled={!saved.length} onClick={() => downloadJson(list.filter((r) => saved.includes(r.processing_id)))}>
            Export saved (JSON backup)
          </button>
        </div>
      </div>

      {rows && shown.length === 0 && <p className="muted hist-empty">{list.length ? "No scans match this search or filter." : "No scans yet. Check your first job and it will appear here."}</p>}

      <div className="hist-grid">
        {shown.map((r) => {
          const d = DECISION[r.decision] || { label: r.decision, cls: "warn" };
          const isSaved = saved.includes(r.processing_id);
          return (
            <article className="hist-card" key={r.processing_id}>
              <button className="hist-open" onClick={() => openReport(r.processing_id)} disabled={opening}>
                <span className={"pill " + d.cls}>{d.label}</span>
                <strong>{r.job_title}</strong>
                <span className="muted">{r.company_name}</span>
                <span className="hist-foot">
                  <b className="score">{Math.round(r.trust_score)}<small>/100</small></b>
                  <small className="muted">{new Date(r.created_timestamp).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}</small>
                </span>
              </button>
              <button className={"star" + (isSaved ? " on" : "")} aria-pressed={isSaved} aria-label={isSaved ? "Remove from saved" : "Save this report"} onClick={() => setSaved(toggleSaved(r.processing_id))}>★</button>
            </article>
          );
        })}
      </div>
    </>
  );
}
