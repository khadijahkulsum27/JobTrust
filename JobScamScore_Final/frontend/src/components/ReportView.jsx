import Ring from "./Ring.jsx";
import { DECISION } from "../lib/format.js";

const ENGINE_NAMES = {
  engine_1: "Digital Identity Verification",
  engine_2: "AI Content Intelligence",
  engine_3: "Job Posting Intelligence",
  engine_4: "Cyber Threat Intelligence",
};

const GROUPS = [
  ["Good signs", "positive_findings", "good"],
  ["Red flags", "negative_findings", "bad"],
  ["Not sure yet", "uncertain_findings", "warn"],
  ["Engines disagree", "conflict_findings", "info"],
];

// Shows one trust report. Expects the flat shape from normalizeAnalyze().
export default function ReportView({ report, onReset, resetLabel = "Check another job" }) {
  const d = DECISION[report.decision] || { label: report.decision, cls: "warn" };
  const scored = report.engine_findings.map((e) => e.engine);
  const notScored = Object.keys(ENGINE_NAMES).filter((k) => !scored.includes(k)).map((k) => ENGINE_NAMES[k]);
  return (
    <div className="report">
      <section className="tile report-top">
        <Ring value={report.trust_score || 0} unit="" label="out of 100" size={190} />
        <div>
          <span className={"pill " + d.cls}>{d.label}</span>
          <h2>{report.risk} risk</h2>
          <p className="muted">Confidence {Math.round(report.confidence || 0)}%</p>
          <p className="report-summary">{report.summary}</p>
        </div>
      </section>

      {notScored.length > 0 && (
        <div className="notice warn" role="status">
          <strong>Incomplete check:</strong> only {scored.length} of 4 engines could score this job
          (not scored: {notScored.join(", ")}). Adding the company website and email and scanning
          again gives a fuller result, so treat this label with care.
        </div>
      )}

      <h3 className="section-title">What each engine found</h3>
      <div className="engine-grid">
        {report.engine_findings.map((e) => (
          <div className="tile" key={e.engine}>
            <div className="bar-head"><strong>{e.name}</strong><span>{Math.round(e.trust_score)}/100</span></div>
            <div className="bar-track"><div className="bar-fill good" style={{ width: e.trust_score + "%" }} /></div>
            <p className="muted engine-note">{e.explanation}</p>
          </div>
        ))}
      </div>

      <div className="finding-grid">
        {GROUPS.map(([title, key, cls]) =>
          report[key].length > 0 && (
            <div className={"tile finding " + cls} key={key}>
              <h3>{title}</h3>
              <ul>{report[key].map((t, i) => <li key={i}>{t}</li>)}</ul>
            </div>
          )
        )}
      </div>

      {report.recommendation && (
        <section className="recommend">
          <strong>What to do next</strong>
          <p>{report.recommendation}</p>
        </section>
      )}
      <button className="btn-pill" onClick={onReset}>{resetLabel}</button>
    </div>
  );
}
