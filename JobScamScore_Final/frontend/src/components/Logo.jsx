// Logo: a score ring that is 75% full with a tick inside.
// It echoes the circular trust-score gauge used on the result page.
export default function Logo({ size = 38 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" aria-hidden="true">
      <defs>
        <linearGradient id="logoGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#4f7cff" />
          <stop offset="1" stopColor="#a78bfa" />
        </linearGradient>
      </defs>
      <circle cx="20" cy="20" r="16" fill="none" stroke="rgba(255,255,255,0.14)" strokeWidth="4" />
      <circle cx="20" cy="20" r="16" fill="none" stroke="url(#logoGrad)" strokeWidth="4"
        strokeLinecap="round" strokeDasharray="75 100" transform="rotate(-90 20 20)" />
      <path d="M13.5 20.5l4.5 4.5 8.5-9.5" fill="none" stroke="#fff" strokeWidth="3"
        strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
