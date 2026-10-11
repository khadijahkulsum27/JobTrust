import { useEffect, useState } from "react";
import { loadHistory } from "../lib/history.js";
import { DECISION } from "../lib/format.js";

const TIPS = [
  "Verify the company's official website",
  "Never pay money to get a job",
  "Check that the contact details match the company",
  "Be careful with urgent offers",
];

const CHECKS = [
  ["Company identity", "Website, email domain, registration"],
  ["Job content", "Wording, urgency, contacts, pay"],
  ["Scam patterns", "Behaviour and salary sense"],
  ["Website safety", "HTTPS, domain age, phishing"],
];

function formatDate(value) {
  const d = new Date(value);
  return isNaN(d) ? "" : d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

export default function Dashboard({ user, onNavigate }) {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    loadHistory().then(setReports);
  }, []);

  const list = reports || [];
  const total = list.length;
  const count = (d) => list.filter((r) => r.decision === d).length;
  const high = count("HIGH_RISK"), review = count("REVIEW"), trusted = count("TRUSTED");
  const pct = (n) => (total ? Math.round((n / total) * 100) : 0);

  const a = total ? (high / total) * 100 : 0;
  const b = total ? ((high + review) / total) * 100 : 0;
  const donut = total
    ? `conic-gradient(var(--bad) 0 ${a}%, var(--warn) ${a}% ${b}%, var(--good) ${b}% 100%)`
    : "conic-gradient(var(--line) 0 100%)";

  return (
    <div className="dash">
      <div className="dash-main">
        <header className="welcome">
          <p className="muted">Welcome back</p>
          <h1 className="page-title">Hi {user.name}, let's make sure your next job is real.</h1>
          <p className="muted dash-sub">
            Check a job ad before you apply. Four engines look at the company, the wording,
            the scam patterns and the website.
          </p>
          <button className="btn-pill" onClick={() => onNavigate("scan")}>Check a job now</button>
        </header>

        <section className="stat-grid" aria-label="Your scans">
          {[
            ["Total scans", total, ""],
            ["High risk", high, "t-bad"],
            ["Needs review", review, "t-warn"],
            ["Trusted", trusted, "t-good"],
          ].map(([label, n, cls]) => (
            <div className="stat-card" key={label}>
              <strong className={cls}>{reports ? n : "–"}</strong>
              <span>{label}</span>
            </div>
          ))}
        </section>

        <section className="tile">
          <div className="tile-head">
            <h3>Recent scan results</h3>
            <button className="link-btn" onClick={() => onNavigate("history")}>View all</button>
          </div>
          {reports && total === 0 && <p className="muted">No scans yet. Check your first job to see it here.</p>}
          <ul className="recent-list">
            {list.slice(0, 5).map((r) => {
              const d = DECISION[r.decision] || { label: r.decision, cls: "warn" };
              const score = Math.round(r.trust_score || 0);
              return (
                <li key={r.processing_id}>
                  <div className="recent-title"><strong>{r.job_title}</strong><span>{r.company_name}</span></div>
                  <span className={"score-ring " + d.cls} style={{ "--p": score }}><b>{score}</b></span>
                  <span className={"pill " + d.cls}>{d.label}</span>
                  <span className="recent-date">{formatDate(r.created_timestamp)}</span>
                </li>
              );
            })}
          </ul>
        </section>

        <section className="tile">
          <h3>Risk distribution</h3>
          <div className="distro">
            <div className="donut" style={{ background: donut }}>
              <div className="donut-hole">
                <strong>{reports ? total : "–"}</strong>
                <span>Total scans</span>
              </div>
            </div>
            <ul className="legend">
              {[["High risk", high, "bad"], ["Needs review", review, "warn"], ["Trusted", trusted, "good"]].map(([name, n, cls]) => (
                <li key={name}>
                  <span className={"dot " + cls} />
                  <span>{name}</span>
                  <span>{pct(n)}%</span>
                  <span>{n}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>

      <aside className="dash-side">
        <section className="tile">
          <h3>What every scan checks</h3>
          <ul className="scan-checks">
            {CHECKS.map(([title, text]) => (
              <li key={title}><strong>{title}</strong><span>{text}</span></li>
            ))}
          </ul>
        </section>
        <section className="tile">
          <h3>Quick tips</h3>
          <ul className="tips">
            {TIPS.map((t) => <li key={t}>{t}</li>)}
          </ul>
        </section>
      </aside>
    </div>
  );
}