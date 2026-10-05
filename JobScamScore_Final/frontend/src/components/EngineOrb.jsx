// Hero diagram: 4 engines feed one glowing "trust score" orb.
const LEFT = [
  { name: "Identity", tag: "Engine 1", text: "Company, website, email and domain." },
  { name: "Content", tag: "Engine 2", text: "Wording, urgency, contacts and pay." },
];
const RIGHT = [
  { name: "Intelligence", tag: "Engine 3", text: "Scam patterns and salary sense." },
  { name: "Cyber safety", tag: "Engine 4", text: "HTTPS, domain age, phishing." },
];

function EngineCard({ name, tag, text }) {
  return (
    <div className="engine-card">
      <span className="engine-tag">{tag}</span>
      <strong>{name}</strong>
      <p>{text}</p>
    </div>
  );
}

export default function EngineOrb() {
  return (
    <div className="orb-hero">
      <svg className="orb-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        <path d="M27,24 C40,24 38,50 50,50" /><path d="M27,76 C40,76 38,50 50,50" />
        <path d="M73,24 C60,24 62,50 50,50" /><path d="M73,76 C60,76 62,50 50,50" />
      </svg>
      <div className="orb-col">{LEFT.map((e) => <EngineCard key={e.name} {...e} />)}</div>
      <div className="orb-center">
        <div className="orb"><span>Trust<br />score</span></div>
      </div>
      <div className="orb-col">{RIGHT.map((e) => <EngineCard key={e.name} {...e} />)}</div>
    </div>
  );
}
