import { useRef, useState } from "react";
import { analyzeJob, normalizeAnalyze } from "../lib/analyzeApi.js";
import { extractFromFile, extractFromUrl, parseSalary } from "../lib/extractApi.js";
import { saveLocal } from "../lib/history.js";
import { guessJobTitle, guessCompany } from "../lib/guessFields.js";
import ReportView from "./ReportView.jsx";

const EMPTY = { job_title: "", company_name: "", job_description: "", website: "", email: "", salary: "", experience_level: "fresher" };
const READABLE = [".pdf", ".png", ".jpg", ".jpeg"];

export default function ScanPage() {
  const [form, setForm] = useState(EMPTY);
  const [tab, setTab] = useState("text");
  const [linkUrl, setLinkUrl] = useState("");
  const [status, setStatus] = useState("idle"); // idle | reading | loading | done
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const [report, setReport] = useState(null);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const formRef = useRef(form); // always the latest form, even inside async callbacks
  formRef.current = form;

  // Puts text read by the backend into the form (never overwrites what you typed).
  function applyExtracted(data, label, fromLink) {
    const text = (data.raw_text || "").trim();
    if (!text) return setError("No text could be read from this input.");
    const cur = formRef.current;
    const title = cur.job_title ? "" : guessJobTitle(text);
    const company = cur.company_name ? "" : guessCompany(text);
    setForm((f) => ({
      ...f,
      job_description: text,
      job_title: f.job_title || title,
      company_name: f.company_name || company,
      // A job-page link is NOT the company website, so never copy it into that box.
      website: f.website || (fromLink ? "" : data.website || ""),
      email: f.email || data.email || "",
      salary: f.salary !== "" ? f.salary : parseSalary(data.salary),
    }));

    const guessed = [title && "job title", company && "company name"].filter(Boolean);
    const missing = [!cur.job_title && !title && "job title", !cur.company_name && !company && "company name"].filter(Boolean);
    let msg = `Text read from ${label}.`;
    if (guessed.length) msg += ` The ${guessed.join(" and ")} ${guessed.length > 1 ? "were" : "was"} guessed from the text, so please check.`;
    if (missing.length) msg += ` The ${missing.join(" and ")} could not be found in it, so please type ${missing.length > 1 ? "them" : "it"}.`;
    const noSite = !cur.website && (fromLink || !data.website);
    const noMail = !cur.email && !data.email;
    if (noSite || noMail) msg += ` No ${[noSite && "company website", noMail && "recruiter email"].filter(Boolean).join(" or ")} was found, so the check may be incomplete.`;
    msg += " A salary found is assumed to be yearly.";
    if (fromLink) msg += " Enter the company's own website below if you know it.";
    setNote(msg);
  }

  async function runExtract(task, label, fromLink = false) {
    setError(""); setNote(""); setStatus("reading");
    try { applyExtracted(await task(), label, fromLink); }
    catch (err) { setError(err.message); }
    setStatus("idle");
  }

  async function loadFile(e) {
    const f = e.target.files[0];
    e.target.value = "";
    if (!f) return;
    const ext = "." + f.name.split(".").pop().toLowerCase();
    if (ext === ".txt") {
      setError(""); setNote(`Text loaded from ${f.name}.`);
      const text = await f.text();
      return setForm((cur) => ({ ...cur, job_description: text }));
    }
    if (!READABLE.includes(ext)) return setError("Choose a .txt, .pdf, .png or .jpg file.");
    runExtract(() => extractFromFile(f), f.name);
  }

  function readLink() {
    const url = linkUrl.trim();
    if (!/^https?:\/\/\S+\.\S+/.test(url)) return setError("Enter a full link that starts with http:// or https://");
    runExtract(() => extractFromUrl(url), "the link", true);
  }

  async function submit(e) {
    e.preventDefault();
    if (!form.job_title.trim() || !form.company_name.trim()) return setError("Enter the job title and the company name.");
    if (form.job_description.trim().length < 50) return setError("The job description needs at least 50 characters.");
    let website = form.website.trim();
    if (website && !/^https?:\/\//i.test(website)) website = "https://" + website;
    if (website && !/^https?:\/\/[^\s/]+\.[^\s/]+/.test(website)) return setError("The company website does not look like a web address, for example https://www.example.com");
    if (form.email.trim() && !/^\S+@\S+\.\S+$/.test(form.email.trim())) return setError("The recruiter email does not look right, for example careers@example.com");
    const payload = {
      company_name: form.company_name.trim(),
      job_title: form.job_title.trim(),
      job_description: form.job_description.trim(),
      experience_level: form.experience_level,
    };
    if (website) payload.website = website;
    if (form.email.trim()) payload.email = form.email.trim();
    if (form.salary !== "") payload.salary = Number(form.salary);

    setError(""); setStatus("loading");
    try {
      const rep = normalizeAnalyze(await analyzeJob(payload));
      saveLocal({
        processing_id: rep.processing_id || String(Date.now()),
        company_name: payload.company_name, job_title: payload.job_title,
        trust_score: rep.trust_score, decision: rep.decision, risk: rep.risk,
        created_timestamp: new Date().toISOString(), submission: payload, report: rep,
      });
      setReport(rep);
      setStatus("done");
    } catch (err) {
      setError(err.message + " Is your Flask server running at http://127.0.0.1:5000?");
      setStatus("idle");
    }
  }

  function reset() { setForm(EMPTY); setLinkUrl(""); setNote(""); setReport(null); setStatus("idle"); }

  if (status === "done" && report) return (<><h1 className="page-title">Your trust report</h1><ReportView report={report} onReset={reset} /></>);

  const busy = status === "reading" || status === "loading";
  return (
    <>
      <h1 className="page-title">Scan a job posting</h1>
      <p className="muted scan-sub">Paste the job, upload a file, or give a link. Four engines check it and explain the result.</p>

      <div className="scan-layout">
        <form className="tile" onSubmit={submit} noValidate>
          <div className="tabs" role="tablist" aria-label="How do you want to add the job?">
            {[["text", "Paste text"], ["file", "Upload file"], ["link", "Job link"]].map(([id, label]) => (
              <button key={id} type="button" role="tab" aria-selected={tab === id} className={tab === id ? "on" : ""} onClick={() => setTab(id)}>{label}</button>
            ))}
          </div>

          {tab === "file" && (
            <label className="field"><span>Screenshot, PDF or .txt file</span>
              <input type="file" accept=".txt,.pdf,.png,.jpg,.jpeg" onChange={loadFile} disabled={busy} />
              <small className="muted">{status === "reading" ? "Reading the file… screenshots can take a minute the first time." : "Images and PDFs are read by your backend's input processing layer."}</small>
            </label>
          )}
          {tab === "link" && (
            <label className="field"><span>Link to the job page</span>
              <div className="link-row">
                <input value={linkUrl} onChange={(e) => setLinkUrl(e.target.value)} placeholder="https://example.com/jobs/123" />
                <button type="button" className="btn-pill btn-small" onClick={readLink} disabled={busy}>{status === "reading" ? "Reading…" : "Read page"}</button>
              </div>
            </label>
          )}
          {note && <p className="note">{note}</p>}

          <div className="form-grid">
            <label className="field"><span>Job title *</span><input value={form.job_title} onChange={set("job_title")} placeholder="e.g. Software Developer" /></label>
            <label className="field"><span>Company name *</span><input value={form.company_name} onChange={set("company_name")} placeholder="e.g. Acme Pvt Ltd" /></label>
          </div>

          <label className="field"><span>Job description *</span>
            <textarea rows="7" value={form.job_description} onChange={set("job_description")} placeholder="Paste the full job ad here (at least 50 characters)." />
            <small className="muted">{form.job_description.length} characters</small>
          </label>

          <div className="form-grid">
            <label className="field"><span>Company website</span><input value={form.website} onChange={set("website")} placeholder="https://www.example.com" /></label>
            <label className="field"><span>Recruiter email</span><input value={form.email} onChange={set("email")} placeholder="careers@example.com" /></label>
            <label className="field"><span>Yearly salary (₹)</span><input type="number" min="0" value={form.salary} onChange={set("salary")} placeholder="800000" /></label>
            <label className="field"><span>Experience level</span>
              <select value={form.experience_level} onChange={set("experience_level")}>
                <option value="fresher">Fresher</option><option value="junior">Junior</option><option value="mid">Mid</option><option value="senior">Senior</option>
              </select>
            </label>
          </div>

          {(!form.website.trim() || !form.email.trim()) && (
            <p className="note warn">For a full check add both the company website and the recruiter email. Engine 1 needs both and Engine 4 needs the website. Without them those engines cannot score and the result is marked incomplete.</p>
          )}
          {error && <p className="form-error" role="alert">{error}</p>}
          <button type="submit" className="btn-pill" disabled={busy}>
            {status === "loading" ? "Four engines are checking this job…" : "Analyze job"}
          </button>
        </form>

        <aside className="tile side-list">
          <h3>Every scan checks</h3>
          <ul>
            <li><strong>Company identity</strong><span>Website, email domain, registration.</span></li>
            <li><strong>Job content</strong><span>Wording, urgency, contacts, pay.</span></li>
            <li><strong>Scam patterns</strong><span>Behaviour and salary sense.</span></li>
            <li><strong>Website safety</strong><span>HTTPS, domain age, phishing.</span></li>
          </ul>
        </aside>
      </div>
    </>
  );
}
