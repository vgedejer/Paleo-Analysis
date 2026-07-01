/**
 * A reusable error panel. Note the optional `onRetry` callback prop — passing
 * behavior DOWN as a function is how a child lets a parent decide what happens,
 * keeping this component generic. (React Query gives you a `refetch` function
 * that slots right into this.)
 */
export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="border border-red-900/60 bg-red-950/30 p-4 text-sm text-red-200">
      <p className="font-mono text-xs uppercase tracking-[0.25em] text-red-300">
        Something went wrong.
      </p>
      <p className="mt-2 font-crimson italic text-red-200/80">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 border border-paleo-accent px-4 py-2 font-mono text-xs uppercase tracking-[0.25em] text-paleo-accent transition-colors hover:bg-paleo-accent hover:text-paleo-bg"
        >
          Retry
        </button>
      )}
    </div>
  );
}
