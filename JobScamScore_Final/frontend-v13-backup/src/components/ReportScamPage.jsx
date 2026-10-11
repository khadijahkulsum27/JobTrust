import { useState } from "react";
import { downloadJson } from "../lib/saved.js";

const KEY = "jobtrust_scam_reports";
const TYPES = ["Asked for a registration or training fee", "Fake offer letter or interview", "Asked for ID or bank details", "Work-from-home / task scam", "Other"];

function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } }

// Saved on this device only. The backend has no reporting route.
export default function ReportScamPage() {
  const [items, setItems] = useState(load());
  const [form, setForm] = useState({ job_title: "", company: "", type: TYPES[0], story: "" });
  const [error, setError] = useState("");
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  function persist(next) {
    setItems(next);
    try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* ignore */ }
  }
  function submit(e) {
    e.preventDefault();
    if (!form.job_title.trim()) return setError("Please enter the job title.");
    if (form.story.trim().length < 20) return setError("Describe what happened in at least 20 characters.");
    setError("");
    persist([{ id: Date.now(), date: new Date().toISOString(), ...form }, ...items]);
    setForm({ job_title: "", company: "", type: TYPES[0], story: "" });
  }

  return (
    <>
      <h1 className="page-title">Report a scam</h1>
      <p className="muted hist-sub">Keep a record of scams you met. These notes are saved on this device only and are not sent anywhere.</p>
      <div className="scan-layout">
        <form className="tile" onSubmit={submit} noValidate>
          <div className="form-grid">
            <label className="field"><span>Job title *</span><input value={form.job_title} onChange={set("job_title")} placeholder="e.g. Data Entry Executive" /></label>
            <label className="field"><span>Company or website</span><input value={form.company} onChange={set("company")} placeholder="Optional" /></label>
          </div>
          <label className="field"><span>Type of scam</span>
            <select value={form.type} onChange={set("type")}>{TYPES.map((t) => <option key={t}>{t}</option>)}</select>
          </label>
          <label className="field"><span>What happened? *</span>
            <textarea rows="6" maxLength="2000" value={form.story} onChange={set("story")} placeholder="Describe what you were asked to do." />
            <small className="muted">{form.story.length}/2000</small>
          </label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button type="submit" className="btn-pill">Save report</button>
        </form>
        <aside className="tile side-list">
          <h3>Your notes ({items.length})</h3>
          {items.length === 0 && <p className="muted">Nothing saved yet.</p>}
          <ul>
            {items.map((i) => (
              <li key={i.id}>
                <strong>{i.job_title}</strong><span>{i.type}</span>
                <button className="link-btn" onClick={() => persist(items.filter((x) => x.id !== i.id))}>Delete</button>
              </li>
            ))}
          </ul>
          <button className="link-btn" disabled={!items.length} onClick={() => downloadJson(items)}>Export as JSON</button>
        </aside>
      </div>
    </>
  );
}
