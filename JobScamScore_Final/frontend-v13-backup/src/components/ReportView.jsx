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
  ["How the engines compare", "conflict_findings", "info"],
];
const ML_LABELS = {
  LIKELY_FAKE: "The wording looks like fake ads",
  UNSURE: "Not sure",
  LIKELY_GENUINE: "The wording looks like genuine ads",
};

// Shows one trust report. Expects the flat shape from normalizeAnalyze().
export default function ReportView({ report, onReset, resetLabel = "Check another job" }) {
  const d = DECISION[report.decision] || { label: report.decision, cls: "warn" };
  const scored = report.engine_findings.map((e) => e.engine);
  const notScored = Object.keys(ENGINE_NAMES).filter((k) => !scored.includes(k)).map((k) => ENGINE_NAMES[k]);
  const incomplete = notScored.length > 0;
  return (
    <div className="report">
      <section className="tile report-top">
                {incomplete ? (
          <div className="ring" style={{ width: 190, height: 190 }}>
            <div className="ring-center"><strong>?</strong><span>not enough data</span></div>
          </div>
        ) : (
          <Ring value={report.trust_score || 0} unit="" label="out of 100" size={190} />
        )}
        <div>
          <span className={"pill " + (incomplete ? "warn" : d.cls)}>{incomplete ? "Not enough information" : d.label}</span>
          <h2>{incomplete ? "Incomplete check" : report.risk + " risk"}</h2>
          <p className="muted">Confidence {Math.round(report.confidence || 0)}%</p>
          <p className="report-summary">
            {incomplete
              ? `Only ${scored.length} of 4 engines could check this job, so we cannot give a trustworthy score. The partial score from those engines was ${Math.round(report.trust_score || 0)}/100. Add the company website and the recruiter email, then scan again.`
              : report.summary}
          </p>
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
                        <p className="muted engine-note">
              {e.engine === "engine_2" || e.engine === "engine_3"
                ? "Checks the wording of the ad only. A high score means no obvious scam phrases were found. It does not prove the job or company is real."
                : e.explanation}
            </p>
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

      {report.ml_opinion && report.ml_opinion.available && (
        <div className="tile finding info">
          <h3>Second opinion: text model</h3>
          <ul>
            <li>{ML_LABELS[report.ml_opinion.label] || report.ml_opinion.label}</li>
            <li>Model score: {Number(report.ml_opinion.fake_probability).toFixed(2)} out of 1 (not a true probability)</li>
            <li>{report.ml_opinion.note}</li>
          </ul>
        </div>
      )}
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
