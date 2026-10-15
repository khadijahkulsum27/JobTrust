import { useEffect, useState } from "react";
import { loadHistory } from "../lib/history.js";
import { DECISION } from "../lib/format.js";
import Icon from "./Icon.jsx";
import "../dashboard-extra.css";

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

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const DAY_MS = 24 * 60 * 60 * 1000;

const COLORS = { bad: "#fb7185", warn: "#fbbf24", good: "#34d399", blue: "#8ab4ff" };

function formatDate(value) {
  const d = new Date(value);
  return isNaN(d) ? "" : d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function formatTime(value) {
  const d = new Date(value);
  return isNaN(d) ? "" : d.toLocaleTimeString("en-IN", { hour: "numeric", minute: "2-digit" });
}

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

// Scans in the last 7 days against the 7 days before that. Real numbers only.
function weekCounts(list, test) {
  const now = Date.now();
  let cur = 0;
  let prev = 0;
  list.forEach((r) => {
    if (!test(r)) return;
    const age = now - new Date(r.created_timestamp).getTime();
    if (isNaN(age) || age < 0) return;
    if (age < 7 * DAY_MS) cur++;
    else if (age < 14 * DAY_MS) prev++;
  });
  return { cur, prev };
}

function Trend({ cur, prev, kind }) {
  if (prev === 0) {
    return (
      <div className="dx-trend" style={{ color: "#9fb0da" }}>
        {cur > 0 ? cur + " this week" : "None this week"}
      </div>
    );
  }
  const pct = Math.round(((cur - prev) / prev) * 100);
  const up = pct >= 0;
  let color = COLORS.warn;
  if (kind === "high") color = up ? COLORS.bad : COLORS.good;
  else if (kind === "trusted" || kind === "total") color = up ? COLORS.good : COLORS.bad;
  return (
    <div className="dx-trend" style={{ color }}>
      {up ? "↗ +" : "↘ "}{pct}% <small>vs last week</small>
    </div>
  );
}

function Illustration() {
  return (
    <svg className="dx-illus" viewBox="0 0 240 200" aria-hidden="true">
      <defs>
        <linearGradient id="dxDoc" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#8ab4ff" />
          <stop offset="1" stopColor="#4f7cff" />
        </linearGradient>
        <linearGradient id="dxLens" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#69e0bb" />
          <stop offset="1" stopColor="#4f7cff" />
        </linearGradient>
      </defs>
      <path d="M30 40 l4 -10 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 z" fill="#8ab4ff" opacity="0.7" />
      <path d="M205 30 l3 -7 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3 z" fill="#69e0bb" opacity="0.8" />
      <g transform="rotate(-8 100 100)">
        <rect x="45" y="22" width="120" height="150" rx="12" fill="rgba(79,124,255,0.18)" stroke="url(#dxDoc)" strokeWidth="2.5" />
        <rect x="60" y="36" width="90" height="18" rx="5" fill="url(#dxDoc)" opacity="0.9" />
        <text x="105" y="49" textAnchor="middle" fontSize="10" fontWeight="700" fill="#07102b">JOB OFFER</text>
        <rect x="60" y="68" width="90" height="6" rx="3" fill="#8ab4ff" opacity="0.55" />
        <rect x="60" y="84" width="70" height="6" rx="3" fill="#8ab4ff" opacity="0.4" />
        <rect x="60" y="100" width="80" height="6" rx="3" fill="#8ab4ff" opacity="0.4" />
        <rect x="60" y="116" width="55" height="6" rx="3" fill="#8ab4ff" opacity="0.3" />
      </g>
      <circle cx="158" cy="128" r="36" fill="rgba(7,11,31,0.85)" stroke="url(#dxLens)" strokeWidth="6" />
      <path d="M158 108 l18 7 v14 c0 12 -9 19 -18 23 c-9 -4 -18 -11 -18 -23 v-14 z" fill="rgba(105,224,187,0.15)" stroke="#69e0bb" strokeWidth="3" strokeLinejoin="round" />
      <path d="M149 130 l7 7 14 -15" fill="none" stroke="#69e0bb" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
      <line x1="184" y1="156" x2="214" y2="186" stroke="url(#dxLens)" strokeWidth="10" strokeLinecap="round" />
    </svg>
  );
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

  const week = lastSevenDays(list);
  const maxDay = Math.max(1, ...week.map((d) => d.count));

  const STATS = [
    { kind: "total", label: "Total scans", n: total, color: COLORS.blue, icon: <Icon name="doc" />, week: weekCounts(list, () => true) },
    { kind: "high", label: "High risk", n: high, color: COLORS.bad, icon: "!", week: weekCounts(list, (r) => r.decision === "HIGH_RISK") },
    { kind: "review", label: "Needs review", n: review, color: COLORS.warn, icon: "▲", week: weekCounts(list, (r) => r.decision === "REVIEW") },
    { kind: "trusted", label: "Trusted", n: trusted, color: COLORS.good, icon: <Icon name="shield" />, week: weekCounts(list, (r) => r.decision === "TRUSTED") },
  ];

  return (
    <div className="dash">
      <div className="dash-main">
        <header className="welcome dx-welcome">
          <Illustration />
          <p className="muted">Welcome back</p>
          <h1 className="page-title">
            Your next big opportunity starts with a <span className="dx-mint">smart check.</span>
          </h1>
          <p className="muted dash-sub">
            Check a job ad before you apply. Four engines look at the company, the wording,
            the scam patterns and the website.
          </p>
          <button className="btn-pill" onClick={() => onNavigate("scan")}>Check a job now</button>
        </header>

        <section className="dx-stats" aria-label="Your scans">
          {STATS.map((s) => (
            <div className="dx-stat" key={s.kind}>
              <span className="dx-stat-icon" style={{ background: s.color + "26", color: s.color }}>{s.icon}</span>
              <strong className="dx-stat-num">{reports ? s.n : "–"}</strong>
              <span className="dx-stat-label">{s.label}</span>
              {reports && <Trend cur={s.week.cur} prev={s.week.prev} kind={s.kind} />}
            </div>
          ))}
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

      <div className="dash-wide">
        <section className="tile">
          <div className="tile-head">
            <h3>Recent scan results</h3>
            <button className="link-btn" onClick={() => onNavigate("history")}>View all</button>
          </div>
          {reports && total === 0 && <p className="muted">No scans yet. Check your first job to see it here.</p>}
          {total > 0 && (
            <>
              <div className="dx-recent-head">
                <span />
                <span>Job title / Company</span>
                <span>Score</span>
                <span>Risk level</span>
                <span>Date</span>
                <span />
              </div>
              <ul className="dx-recent">
                {list.slice(0, 5).map((r) => {
                  const d = DECISION[r.decision] || { label: r.decision, cls: "warn" };
                  const score = Math.round(r.trust_score || 0);
                  const c = COLORS[d.cls] || COLORS.blue;
                  return (
                    <li key={r.processing_id} onClick={() => onNavigate("history")}>
                      <span className="dx-job-icon" style={{ background: c + "26", color: c }}><Icon name="building" /></span>
                      <div className="dx-recent-title"><strong>{r.job_title}</strong><span>{r.company_name}</span></div>
                      <span className={"score-ring " + d.cls} style={{ "--p": score }}><b>{score}</b></span>
                      <span className={"pill " + d.cls}>{d.label}</span>
                      <span className="dx-date">{formatDate(r.created_timestamp)}<br />{formatTime(r.created_timestamp)}</span>
                      <span className="dx-arrow">›</span>
                    </li>
                  );
                })}
              </ul>
            </>
          )}
        </section>

        <div className="dash-pair">
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

          <section className="tile">
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
          </section>
        </div>
      </div>
    </div>
  );
}