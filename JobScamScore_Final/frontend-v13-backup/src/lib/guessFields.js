// Best-effort guesses for the job title and company name from text read out of
// a screenshot, PDF or web page. They are only GUESSES: the form shows them
// so the user can check and correct them. Returns "" when nothing is found.

const tidy = (s) => s.replace(/[|•·:\-–—]+$/g, "").replace(/\s+/g, " ").trim();
const toLines = (text) => text.split("\n").map((l) => l.trim()).filter(Boolean);

export function guessJobTitle(text) {
  const lines = toLines(text);

  // 1) A labelled line, e.g. "Job Title: Data Analyst"
  const labelled = /^(?:job\s*title|position|role|designation|vacancy|opening)\s*[:\-–]\s*(.{3,100})$/i;
  for (const line of lines) {
    const m = line.match(labelled);
    if (m) return tidy(m[1]);
  }

  // 2) "We're Hiring | Data Analyst". Ignores the #Hiring hashtag.
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/(?:^|[^#\w])hiring\b\s*[:|\-–!]*\s*(.*)$/i);
    if (!m) continue;
    let title = m[1].trim();
    let next = i + 1;
    if (!title && lines[next]) { title = lines[next]; next++; }
    if (!title) continue;
    // A short capitalised line right after is usually the rest of a wrapped title.
    const more = lines[next];
    if (more && more.split(/\s+/).length <= 4 && /^[A-Z]/.test(more) && !/[:.!?]$/.test(more)) title += " " + more;
    return tidy(title).slice(0, 100);
  }
  return "";
}

export function guessCompany(text) {
  const lines = toLines(text);

  // 1) A labelled line, e.g. "Company: Acme Pvt Ltd"
  const labelled = /^(?:company(?:\s*name)?|organi[sz]ation|employer)\s*[:\-–]\s*(.{2,80})$/i;
  for (const line of lines) {
    const m = line.match(labelled);
    if (m) return tidy(m[1]);
  }

  // 2) "Acme Pvt Ltd is hiring" and 3) "Join Acme Pvt Ltd"
  for (const line of lines) {
    const hiring = line.match(/^([A-Z][\w&.,'\- ]{1,60}?)\s+is\s+(?:now\s+)?hiring\b/);
    if (hiring) return tidy(hiring[1]);
    const join = line.match(/\b[Jj]oin\s+(?:the\s+team\s+at\s+|us\s+at\s+)?([A-Z][\w&.\-]+(?:\s+[A-Z][\w&.\-]+){0,3})/);
    if (join) return tidy(join[1]);
  }
  return "";
}
