import { useEffect, useState } from "react";
import { loadHistory } from "../lib/history.js";
import EngineOrb from "./EngineOrb.jsx";
import Ring from "./Ring.jsx";
import { DECISION } from "../lib/format.js";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Counts scans per day for the last 7 days.
function lastSevenDays(reports) {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - i);
    days.push({ key: d.toDateString(), label: DAYS[d.getDay()], count: 0 });
  }
  reports.forEach((r) => {
    const slot = days.find((x) => x.key === new Date(r.created_timestamp).toDateString());
    if (slot) slot.count++;
  });
  return days;
}

export default function Dashboard({ user, onNavigate }) {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    loadHistory().then(setReports);
  }, []);

  const list = reports || [];
  const total = list.length;
  const count = (d) => list.filter((r) => r.decision === d).length;
  const trusted = count("TRUSTED"), review = count("REVIEW"), high = count("HIGH_RISK");
  const pct = (n) => (total ? Math.round((n / total) * 100) : 0);
  const week = lastSevenDays(list);
  const maxDay = Math.max(1, ...week.map((d) => d.count));

  return (
    <>
      <header className="welcome">
        <p className="muted">Welcome back</p>
        <h1 className="page-title">Hi {user.name}, let's make sure your next job is real.</h1>
        <button className="btn-pill" onClick={() => onNavigate("scan")}>Check a job now</button>
      </header>

      <EngineOrb />


      <section className="bento" aria-label="Your scans">
        <div className="tile tile-wide">
          <h3>Your scans</h3>
          <div className="stat-row">
            <div><strong>{reports ? total : "–"}</strong><span>Total scans</span></div>
            <div><strong className="t-bad">{reports ? high : "–"}</strong><span>High risk</span></div>
            <div><strong className="t-good">{reports ? trusted : "–"}</strong><span>Trusted</span></div>
          </div>
        </div>

        <div className="tile tile-center">
          <h3>Trusted share</h3>
          <Ring value={pct(trusted)} label="trusted" />
        </div>

        <div className="tile">
          <h3>Risk breakdown</h3>
          {[["Trusted", trusted, "good"], ["Needs review", review, "warn"], ["High risk", high, "bad"]].map(([name, n, cls]) => (
            <div className="bar-row" key={name}>
              <div className="bar-head"><span>{name}</span><span>{n} ({pct(n)}%)</span></div>
              <div className="bar-track"><div className={"bar-fill " + cls} style={{ width: pct(n) + "%" }} /></div>
            </div>
          ))}
        </div>

        <div className="tile tile-wide">
          <h3>Scans in the last 7 days</h3>
          <div className="week">
            {week.map((d) => (
              <div className="week-col" key={d.key}>
                <span className="week-count">{d.count || ""}</span>
                <div className="week-bar" style={{ height: 8 + (d.count / maxDay) * 80 + "px" }} />
                <span className="week-day">{d.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="tile tile-full">
          <div className="tile-head">
            <h3>Recent scans</h3>
            <button className="link-btn" onClick={() => onNavigate("history")}>View all</button>
          </div>
          {reports && total === 0 && <p className="muted">No scans yet. Check your first job to see it here.</p>}
          <ul className="recent">
            {list.slice(0, 5).map((r) => {
              const d = DECISION[r.decision] || { label: r.decision, cls: "warn" };
              return (
                <li key={r.processing_id}>
                  <div><strong>{r.job_title}</strong><span>{r.company_name}</span></div>
                  <b className="score">{Math.round(r.trust_score)}</b>
                  <span className={"pill " + d.cls}>{d.label}</span>
                </li>
              );
            })}
          </ul>
        </div>
      </section>
    </>
  );
}
