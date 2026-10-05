import Icon from "./Icon.jsx";
import Logo from "./Logo.jsx";
const LINKS = [
  { id: "dashboard", label: "Dashboard", icon: "dashboard" },
  { id: "scan", label: "Scan job", icon: "search" },
  { id: "history", label: "History", icon: "history" },
  { id: "report", label: "Report a scam", icon: "flag" },
];

export default function Sidebar({ page, onNavigate, user, onLogout }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <Logo />
        <span className="brand-name">JobTrust</span>
      </div>

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

      <div className="user-box">
        <div className="user-name">{user.name}</div>
        <div className="user-email">{user.email}</div>
        <button className="link-btn" onClick={onLogout}>Sign out</button>
      </div>
    </aside>
  );
}
