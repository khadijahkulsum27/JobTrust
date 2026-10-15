import Ring from "./Ring.jsx";
import Icon from "./Icon.jsx";
import { DECISION } from "../lib/format.js";

const GOOD = "#34d399";
const WARN = "#fbbf24";
const BAD = "#fb7185";
const BLUE = "#8ab4ff";

const ORDER = ["engine_1", "engine_2", "engine_3", "engine_4"];

const INFO = {
  engine_1: {
    name: "Digital Identity Verification",
    icon: "building",
    what: "Checks the website, the recruiter's email, the domain's age and our small company list.",
  },
  engine_2: {
    name: "AI Content Intelligence",
    icon: "doc",
    what: "Checks the wording of the ad only. A high score means no obvious scam phrases were found. It does not prove the job or company is real.",
  },
  engine_3: {
    name: "Job Posting Intelligence",
    icon: "chart",
    what: "Looks for scam patterns and pay that does not fit the job. Wording only. It does not prove the job or company is real.",
  },
  engine_4: {
    name: "Cyber Threat Intelligence",
    icon: "shield",
    what: "Checks the website's security, its age, and safety lists (VirusTotal and Google Safe Browsing).",
  },
};

const ML_LABELS = {
  LIKELY_FAKE: { text: "The wording looks like fake ads", color: BAD },
  UNSURE: { text: "Not sure", color: WARN },
  LIKELY_GENUINE: { text: "The wording looks like genuine ads", color: GOOD },
};

const LEVEL = {
  bad: { icon: "✕", color: BAD, word: "Serious warning" },
  warn: { icon: "!", color: WARN, word: "Be careful" },
  good: { icon: "✓", color: GOOD, word: "Good sign" },
};

const colorFor = (score) => (score >= 75 ? GOOD : score >= 50 ? WARN : BAD);
const barClass = (score) => (score >= 75 ? "good" : score >= 50 ? "warn" : "bad");

function IconBadge({ name, mark, color }) {
  return (
    <span
      style={{
        flex: "0 0 44px",
        width: 44,
        height: 44,
        borderRadius: "50%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: color + "26",
        color: color,
        fontWeight: 700,
        fontSize: 20,
      }}
    >
      {name ? <Icon name={name} /> : mark}
    </span>
  );
}

// Shows one trust report. Expects the flat shape from normalizeAnalyze().
export default function ReportView({ report, onReset, resetLabel = "Check another job" }) {
  const d = DECISION[report.decision] || { label: report.decision, cls: "warn" };
  const findings = report.engine_findings || [];
  const byKey = {};
  findings.forEach((f) => {
    byKey[f.engine] = f;
  });

  const ranCount = ORDER.filter((k) => byKey[k] && typeof byKey[k].trust_score === "number").length;
  const incomplete = ranCount < 4;
  const plain = report.plain_explanation || null;
  // Old reports (no plain explanation) were scored the old way, so keep hiding their score when incomplete.
  const showScore = !incomplete || !!plain;

  const why = plain && Array.isArray(plain.why) ? plain.why : null;
  const glance = why
    ? {
        good: why.filter((i) => i.level === "good").map((i) => i.text),
        bad: why.filter((i) => i.level === "bad").map((i) => i.text),
        warn: why.filter((i) => i.level === "warn").map((i) => i.text),
      }
    : {
        good: report.positive_findings || [],
        bad: report.negative_findings || [],
        warn: report.uncertain_findings || [],
      };

  const CARDS = [
    { key: "good", title: "Good signs", color: GOOD, mark: "✓", empty: "Nothing positive was reported." },
    { key: "bad", title: "Red flags", color: glance.bad.length ? BAD : WARN, mark: "!", empty: "No serious warning signs reported." },
    { key: "warn", title: "Not sure yet", color: BLUE, mark: "?", empty: "Nothing is unclear." },
  ];

  const steps = plain && Array.isArray(plain.advice) && plain.advice.length
    ? plain.advice
    : report.recommendation
    ? [report.recommendation]
    : [];

  const ml = report.ml_opinion && report.ml_opinion.available ? report.ml_opinion : null;
  const mlLabel = ml ? ML_LABELS[ml.label] || { text: ml.label, color: BLUE } : null;

  function scrollToEngines() {
    const el = document.getElementById("engine-analysis");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <div className="report" style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <p className="muted" style={{ margin: 0 }}>Understand the signals behind this job posting.</p>

      {/* Score card + completeness card */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 20 }}>
        <section className="tile report-top" style={{ flex: "2 1 420px", boxSizing: "border-box", margin: 0 }}>
          {showScore ? (
            <Ring value={report.trust_score || 0} unit="" label="out of 100" size={170} />
          ) : (
            <div className="ring" style={{ width: 170, height: 170 }}>
              <div className="ring-center"><strong>?</strong><span>not enough data</span></div>
            </div>
          )}
          <div>
            <span className={"pill " + (showScore ? d.cls : "warn")}>{showScore ? d.label : "Not enough information"}</span>
            <h2>{showScore ? report.risk + " risk" : "Incomplete check"}</h2>
            <p className="muted">Confidence {Math.round(report.confidence || 0)}%</p>
            <p className="report-summary">
              {showScore
                ? report.summary
                : `Only ${ranCount} of 4 engines could check this job, so we cannot give a trustworthy score. Add the company website and the recruiter email, then scan again.`}
            </p>
          </div>
        </section>

        <section className="tile" style={{ flex: "1 1 260px", boxSizing: "border-box", margin: 0 }}>
          <div style={{ display: "flex", gap: 14, alignItems: "center" }}>
            <IconBadge name="doc" color={incomplete ? WARN : BLUE} />
            <div>
              <strong style={{ fontSize: 18 }}>Check completeness</strong>
              <div className="muted">{ranCount} of 4 analysis engines ran</div>
            </div>
          </div>
          <button className="link-btn" style={{ marginTop: 14 }} onClick={scrollToEngines}>
            Review evidence below
          </button>
        </section>
      </div>

      {incomplete && (
        <div className="notice warn" role="status" style={{ margin: 0 }}>
          <strong>Incomplete check:</strong>{" "}
          {plain && plain.incomplete_note
            ? plain.incomplete_note
            : `only ${ranCount} of 4 engines could score this job. Adding the company website and email and scanning again gives a fuller result, so treat this label with care.`}
        </div>
      )}

      {/* Engine analysis: 2 x 2 grid */}
      <div id="engine-analysis">
        <h3 className="section-title" style={{ margin: "0 0 12px" }}>Engine analysis</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 16 }}>
          {ORDER.map((key) => {
            const f = byKey[key];
            const info = INFO[key];
            const score = f && typeof f.trust_score === "number" ? Math.round(f.trust_score) : null;
            const c = score === null ? "#64748b" : colorFor(score);
            return (
              <div className="tile" key={key} style={{ boxSizing: "border-box", margin: 0, display: "flex", gap: 14 }}>
                <IconBadge name={info.icon} color={c} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                    <strong>{info.name}</strong>
                    <span className="muted">{score === null ? "Could not run" : score + "/100"}</span>
                  </div>
                  <div className="bar-track" style={{ margin: "8px 0" }}>
                    {score !== null && <div className={"bar-fill " + barClass(score)} style={{ width: score + "%" }} />}
                  </div>
                  <p className="muted" style={{ margin: 0, fontSize: 13 }}>
                    {score === null
                      ? "This check could not run. Add the company website and the recruiter email, then scan again."
                      : info.what}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Findings at a glance: three cards side by side */}
      <div>
        <h3 className="section-title" style={{ margin: "0 0 12px" }}>Findings at a glance</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 16 }}>
          {CARDS.map((c) => {
            const list = glance[c.key];
            const shown = list.slice(0, 4);
            return (
              <div
                key={c.key}
                className="tile"
                style={{ boxSizing: "border-box", margin: 0, border: "1px solid " + c.color + "88", background: c.color + "10" }}
              >
                <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 10 }}>
                  <IconBadge mark={c.mark} color={c.color} />
                  <strong style={{ fontSize: 18, color: c.key === "bad" ? c.color : "inherit" }}>{c.title}</strong>
                </div>
                {shown.length === 0 ? (
                  <p className="muted" style={{ margin: 0 }}>{c.empty}</p>
                ) : (
                  <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
                    {shown.map((t, i) => (
                      <li key={i} style={{ display: "flex", gap: 8, padding: "4px 0", fontSize: 14 }}>
                        <span style={{ color: c.key === "warn" ? WARN : c.color, fontWeight: 700 }}>
                          {c.key === "good" ? "✓" : "•"}
                        </span>
                        <span>{t}</span>
                      </li>
                    ))}
                  </ul>
                )}
                {why && list.length > shown.length && (
                  <p className="muted" style={{ margin: "8px 0 0", fontSize: 13 }}>
                    +{list.length - shown.length} more, see "Why we think so" below
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Second opinion from the trained text model */}
      {ml && (
        <section className="tile" style={{ boxSizing: "border-box", margin: 0, display: "flex", gap: 14 }}>
          <IconBadge name="cpu" color={BLUE} />
          <div>
            <strong style={{ fontSize: 18 }}>Second opinion: text model</strong>
            <div style={{ margin: "8px 0" }}>
              <span
                style={{
                  display: "inline-block",
                  padding: "4px 12px",
                  borderRadius: 999,
                  background: mlLabel.color + "26",
                  color: mlLabel.color,
                  fontWeight: 600,
                }}
              >
                {mlLabel.text}
              </span>
            </div>
            <div>Model score: {Number(ml.fake_probability).toFixed(2)} out of 1, not a true probability</div>
            <p className="muted" style={{ margin: "6px 0 0", fontSize: 13 }}>{ml.note}</p>
          </div>
        </section>
      )}

      {/* Why we think so */}
      {why && why.length > 0 && (
        <section className="tile" style={{ boxSizing: "border-box", margin: 0 }}>
          <h3 className="section-title" style={{ margin: "0 0 8px" }}>Why we think so</h3>
          {plain.headline && <p style={{ margin: "0 0 8px", fontWeight: 600 }}>{plain.headline}</p>}
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {why.map((item, i) => {
              const l = LEVEL[item.level] || LEVEL.warn;
              return (
                <li key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start", padding: "8px 0" }}>
                  <span
                    aria-label={l.word}
                    style={{
                      flex: "0 0 26px", height: 26, borderRadius: "50%", display: "flex",
                      alignItems: "center", justifyContent: "center", fontWeight: 700,
                      color: "#070b1f", background: l.color,
                    }}
                  >
                    {l.icon}
                  </span>
                  <span>{item.text}</span>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {/* What you should do + button */}
      <section className="tile" style={{ boxSizing: "border-box", margin: 0 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12 }}>
          <IconBadge name="shield" color={BLUE} />
          <strong style={{ fontSize: 18 }}>What you should do</strong>
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16, alignItems: "stretch" }}>
          <div style={{ flex: "1 1 400px", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16 }}>
            {steps.map((t, i) => (
              <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <span
                  style={{
                    flex: "0 0 28px", height: 28, borderRadius: "50%", display: "flex",
                    alignItems: "center", justifyContent: "center", fontWeight: 700,
                    background: BLUE + "33", color: BLUE,
                  }}
                >
                  {i + 1}
                </span>
                <span style={{ fontSize: 14 }}>{t}</span>
              </div>
            ))}
          </div>
          <div style={{ display: "flex", alignItems: "center" }}>
            <button className="btn-pill" onClick={onReset}>{resetLabel}</button>
          </div>
        </div>
      </section>

      <p className="muted" style={{ margin: 0, fontSize: 13 }}>
        ⓘ Use this analysis as guidance, not a final decision.
      </p>
    </div>
  );
}