// Logo: a shield outline with a tick inside (shape inspired by the reference image).
export default function Logo({ size = 38 }) {
  const shield = "M20 3 C25 6 30 7 34 7 V19 C34 27 28.5 33 20 37 C11.5 33 6 27 6 19 V7 C10 7 15 6 20 3 Z";
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" aria-hidden="true" style={{ overflow: "visible" }}>
      <defs>
        <linearGradient id="shieldGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#9fd0ff" />
          <stop offset="1" stopColor="#4d9cf0" />
        </linearGradient>
        <filter id="shieldGlow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="1.1" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g filter="url(#shieldGlow)">
        <path d={shield} fill="rgba(92,200,255,0.10)" stroke="url(#shieldGrad)" strokeWidth="2.4" strokeLinejoin="round" />
        <path d={shield} fill="none" stroke="#9fd0ff" strokeOpacity="0.55" strokeWidth="1"
          transform="translate(20 20) scale(0.8) translate(-20 -20)" />
      </g>
      <path d="M13.5 20.5l4.5 4.5 8.5-9.5" fill="none" stroke="#fff" strokeWidth="2.8"
        strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}