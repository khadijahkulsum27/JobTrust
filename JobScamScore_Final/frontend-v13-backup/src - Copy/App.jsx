import { useState } from "react";
import LoginPage from "./components/LoginPage.jsx";
import Sidebar from "./components/Sidebar.jsx";
import ReportScamPage from "./components/ReportScamPage.jsx";
import HistoryPage from "./components/HistoryPage.jsx";
import ScanPage from "./components/ScanPage.jsx";
import Dashboard from "./components/Dashboard.jsx";

function loadUser() {
  try { return JSON.parse(localStorage.getItem("jobtrust_user")); } catch { return null; }
}

// Each page is a placeholder for now. We replace them one by one in Steps 2-5.
const PAGES = {
  dashboard: { title: "Dashboard", note: "Step 2: welcome message, scan totals and risk breakdown." },
  scan: { title: "Scan a job", note: "Step 3: paste text, upload a file, or enter a link." },
  history: { title: "History", note: "Step 4: every past scan, with search, filters and saved reports." },
  report: { title: "Report a scam", note: "Step 5: a form to report a scam you met." },
};

export default function App() {
  const [user, setUser] = useState(loadUser());
  const [page, setPage] = useState("dashboard");

  function handleLogin(u) {
    localStorage.setItem("jobtrust_user", JSON.stringify(u));
    setUser(u);
  }
  function handleLogout() {
    localStorage.removeItem("jobtrust_user");
    setUser(null);
    setPage("dashboard");
  }

  return (
    <>
      <div className="bg-motion" aria-hidden="true"><span /><span /><span /></div>
      {!user ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <div className="app-shell">
          <Sidebar page={page} onNavigate={setPage} user={user} onLogout={handleLogout} />
          <main className="app-main">
            {page === "report" ? (
              <ReportScamPage />
            ) : page === "scan" ? (
              <ScanPage />
            ) : page === "history" ? (
              <HistoryPage />
            ) : page === "dashboard" ? (
              <Dashboard user={user} onNavigate={setPage} />
            ) : (
              <>
                <h1 className="page-title">{PAGES[page].title}</h1>
                <p className="muted">{PAGES[page].note}</p>
              </>
            )}
          </main>
        </div>
      )}
    </>
  );
}
