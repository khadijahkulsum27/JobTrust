// Three reusable card types:
//  FeatureCard = tall card that highlights one feature (glow follows the mouse)
//  InfoCard    = small card with one short fact
//  Steps       = vertical timeline for a real sequence

export function FeatureCard({ icon, title, text }) {
  function track(e) {
    const r = e.currentTarget.getBoundingClientRect();
    e.currentTarget.style.setProperty("--mx", e.clientX - r.left + "px");
    e.currentTarget.style.setProperty("--my", e.clientY - r.top + "px");
  }
  return (
    <article className="feature-card" onMouseMove={track}>
      <span className="feature-icon" aria-hidden="true">{icon}</span>
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

export function InfoCard({ icon, title, text }) {
  return (
    <div className="info-card">
      <span className="info-icon" aria-hidden="true">{icon}</span>
      <div>
        <strong>{title}</strong>
        <p>{text}</p>
      </div>
    </div>
  );
}

export function Steps({ items }) {
  return (
    <ol className="steps">
      {items.map((s, i) => (
        <li key={s.title} className="step">
          <span className="step-dot">{i + 1}</span>
          <div>
            <h3>{s.title}</h3>
            <p>{s.text}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}
