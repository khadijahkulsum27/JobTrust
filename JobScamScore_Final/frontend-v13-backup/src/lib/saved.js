// "Saved" reports (the star button). Kept in this browser only.
const KEY = "jobtrust_saved";

export function getSaved() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}

export function toggleSaved(id) {
  const now = getSaved();
  const next = now.includes(id) ? now.filter((x) => x !== id) : [...now, id];
  localStorage.setItem(KEY, JSON.stringify(next));
  return next;
}

// Downloads the given rows as a .json backup file.
export function downloadJson(rows) {
  const blob = new Blob([JSON.stringify(rows, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "jobtrust-saved-reports.json";
  a.click();
  URL.revokeObjectURL(a.href);
}
