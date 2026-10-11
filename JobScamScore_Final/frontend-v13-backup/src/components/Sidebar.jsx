import Icon from "./Icon.jsx";

const LINKS = [
  { id: "dashboard", label: "Dashboard", icon: "dashboard" },
  { id: "scan", label: "Scan job", icon: "search" },
  { id: "history", label: "History", icon: "history" },
  { id: "report", label: "Report a scam", icon: "flag" },
];

export default function Sidebar({ page, onNavigate }) {
  return (
    <aside className="sidebar">
      <nav className="nav" aria-label="Main">
        {LINKS.map((l) => (
          <button
            key={l.id}
            className={"nav-item" + (page === l.id ? " active" : "")}
            onClick={() => onNavigate(l.id)}
            aria-current={page === l.id ? "page" : undefined}
          >
            <span className="nav-icon"><Icon name={l.icon} /></span>
            {l.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-foot">
        <div>Better decisions.</div>
        <div>Safer applications.</div>
      </div>
    </aside>
  );
}