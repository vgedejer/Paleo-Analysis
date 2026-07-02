/**
 * A presentational ("dumb") component: it takes props, renders markup, holds no
 * state, and triggers no side effects. These are the easiest components to
 * reason about, test, and reuse — keep as much of your UI in this form as you can.
 */
export function Spinner({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-paleo-dim" role="status">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-paleo-line border-t-paleo-accent" />
      <span className="font-mono text-xs uppercase tracking-[0.25em]">{label}</span>
    </div>
  );
}
