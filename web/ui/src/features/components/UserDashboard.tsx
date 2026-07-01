// placeholder for the user dashboard - i will use this page to learn front end 
export function UserDashboard() {
  return (
    <section className="flex min-h-[50vh] flex-col items-center justify-center text-center">
      <div className="flex flex-col items-center border border-dashed border-paleo-line bg-paleo-panel px-8 py-12 text-center">
        <span className="text-5xl" role="img" aria-label="Under construction">
          🦴
        </span>
        <h2 className="mt-6 font-cinzel text-2xl uppercase tracking-wide text-paleo-cream">
          Dashboard under construction
        </h2>
        <p className="mt-3 max-w-sm font-crimson text-base italic leading-relaxed text-paleo-dim">
          We're still excavating this one. Soon you'll see genus counts, fossil
          timelines, and diet breakdowns all in one place.
        </p>
        <p className="mt-6 inline-flex items-center gap-2 border border-paleo-line px-3 py-1 font-mono text-[10px] uppercase tracking-[0.25em] text-paleo-accent">
          🚧 Coming soon
        </p>
      </div>
    </section>
  );
}
