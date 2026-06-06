/**
 * A presentational ("dumb") component: it takes props, renders markup, holds no
 * state, and triggers no side effects. These are the easiest components to
 * reason about, test, and reuse — keep as much of your UI in this form as you can.
 */
export function Spinner({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-fossil-700" role="status">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-fossil-100 border-t-fossil-700" />
      <span className="text-sm">{label}</span>
    </div>
  );
}
