// placeholder for the user dashboard - i will use this page to learn front end 
export function UserDashboard() {
  return (
    <section className="flex min-h-[50vh] flex-col items-center justify-center text-center">
      <div className="rounded-2xl border border-dashed border-fossil-100 bg-white px-8 py-12">
        <span className="text-5xl" role="img" aria-label="Under construction">
          🦴
        </span>
        <h2 className="mt-4 text-xl font-bold text-fossil-900">
          Dashboard under construction
        </h2>
        <p className="mt-2 max-w-sm text-sm text-fossil-700/70">
          We're still excavating this one. Soon you'll see genus counts, fossil
          timelines, and diet breakdowns all in one place.
        </p>
        <p className="mt-6 inline-flex items-center gap-2 rounded-full bg-fossil-100 px-3 py-1 text-xs font-medium text-fossil-700">
          🚧 Coming soon
        </p>
      </div>
    </section>
  );
}
