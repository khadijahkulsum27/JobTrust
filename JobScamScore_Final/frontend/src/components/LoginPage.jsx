import Logo from "./Logo.jsx";
import { useState } from "react";

// FRONTEND-ONLY demo login. The backend has no login API,
// so the user is just remembered in this browser.
export default function LoginPage({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (mode === "signup" && !name.trim()) return setError("Please enter your name.");
    if (!/^\S+@\S+\.\S+$/.test(email)) return setError("Enter a valid email address, like you@example.com.");
    if (password.length < 6) return setError("Password needs at least 6 characters.");
    setError("");
    onLogin({ name: name.trim() || email.split("@")[0], email });
  }

  return (
    <main className="login-page">
      <section className="login-intro">
        <div className="brand">
          <Logo />
          <span className="brand-name">JobTrust</span>
        </div>
        <h1 className="hero-title">Got a job offer?<br />Let's check it's real.</h1>
        <p className="hero-sub">
          Paste the ad, upload a screenshot or a PDF. Four independent engines look at the
          company, the wording, the pay and the website, then explain the result in plain English.
        </p>
        <ul className="check-list">
          <li>Company identity and website</li>
          <li>Job wording and pay</li>
          <li>Scam patterns</li>
          <li>Website security</li>
        </ul>
      </section>

      <section className="card login-card" aria-labelledby="form-title">
        <h2 id="form-title">{mode === "login" ? "Welcome back" : "Create your account"}</h2>
        <p className="muted">{mode === "login" ? "Log in to see your saved reports." : "It takes less than a minute."}</p>

        <form onSubmit={handleSubmit} noValidate>
          {mode === "signup" && (
            <label className="field"><span>Your name</span>
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Asha Kumar" autoComplete="name" />
            </label>
          )}
          <label className="field"><span>Email</span>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" />
          </label>
          <label className="field"><span>Password</span>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 6 characters" autoComplete={mode === "login" ? "current-password" : "new-password"} />
          </label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button type="submit" className="btn-pill btn-block">{mode === "login" ? "Log in" : "Create account"}</button>
        </form>

        <p className="switch-line">
          {mode === "login" ? "New here?" : "Already have an account?"}{" "}
          <button type="button" className="link-btn" onClick={() => { setMode(mode === "login" ? "signup" : "login"); setError(""); }}>
            {mode === "login" ? "Create an account" : "Log in"}
          </button>
        </p>
        <p className="demo-note">Demo login: accounts are stored only in this browser.</p>
      </section>
    </main>
  );
}
