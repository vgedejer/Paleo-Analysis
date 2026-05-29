/**
 * A reusable error panel. Note the optional `onRetry` callback prop — passing
 * behavior DOWN as a function is how a child lets a parent decide what happens,
 * keeping this component generic. (React Query gives you a `refetch` function
 * that slots right into this.)
 */
export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
      <p className="font-medium">Something went wrong.</p>
      <p className="mt-1 text-red-700">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 rounded-md bg-red-600 px-3 py-1.5 text-white transition hover:bg-red-700"
        >
          Retry
        </button>
      )}
    </div>
  );
}
