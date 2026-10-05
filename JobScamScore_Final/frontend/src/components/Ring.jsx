import { useId } from "react";

// Circular gauge: big number in the middle, coloured ring around it.
export default function Ring({ value = 0, label = "", size = 150, unit = "%" }) {
  const id = useId();
  const r = 52, c = 2 * Math.PI * r;
  const filled = (Math.max(0, Math.min(100, value)) / 100) * c;
  return (
    <div className="ring" style={{ width: size, height: size }}>
      <svg viewBox="0 0 120 120">
        <defs>
          <linearGradient id={id} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#22d3ee" /><stop offset="1" stopColor="#a78bfa" />
          </linearGradient>
        </defs>
        <circle cx="60" cy="60" r={r} className="ring-track" />
        <circle cx="60" cy="60" r={r} className="ring-fill" stroke={`url(#${id})`}
          strokeDasharray={`${filled} ${c}`} transform="rotate(-90 60 60)" />
      </svg>
      <div className="ring-center"><strong>{Math.round(value)}{unit}</strong><span>{label}</span></div>
    </div>
  );
}
