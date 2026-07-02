import { useEffect, useMemo, useState } from "react";

/** The page-size choices offered in the toolbar, in order. */
export const PAGE_SIZE_OPTIONS = [10, 25, 50, 100] as const;
export type PageSize = (typeof PAGE_SIZE_OPTIONS)[number];

/**
 * Client-side pagination over an already-materialised array.
 *
 * `resetKey` should encode whatever narrows the list (search text, active
 * filter, …). When it changes — or the page size changes — we jump back to
 * page 1 so the user is never stranded on a page that no longer exists. The
 * page is also clamped every render, so shrinking the list can never show an
 * empty page.
 */
export function usePagination<T>(
  items: T[],
  resetKey: unknown,
  initialPageSize: PageSize = 25,
) {
  const [pageSize, setPageSize] = useState<PageSize>(initialPageSize);
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
  }, [resetKey, pageSize]);

  const total = items.length;
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  const currentPage = Math.min(page, pageCount);
  const start = (currentPage - 1) * pageSize;

  const pageItems = useMemo(
    () => items.slice(start, start + pageSize),
    [items, start, pageSize],
  );

  return {
    pageItems,
    page: currentPage,
    pageCount,
    pageSize,
    setPageSize,
    setPage,
    total,
    rangeStart: total === 0 ? 0 : start + 1,
    rangeEnd: Math.min(start + pageSize, total),
  };
}

interface PaginationProps {
  page: number;
  pageCount: number;
  pageSize: PageSize;
  total: number;
  rangeStart: number;
  rangeEnd: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: PageSize) => void;
  /** Noun for the range read-out, e.g. "genera" or "fossils". */
  unit: string;
}

/**
 * The pagination toolbar: a page-size selector plus prev/next navigation and a
 * "start–end of total" read-out. Styled to match the dark archive theme; wraps
 * on narrow columns.
 */
export function Pagination({
  page,
  pageCount,
  pageSize,
  total,
  rangeStart,
  rangeEnd,
  onPageChange,
  onPageSizeChange,
  unit,
}: PaginationProps) {
  const navButton =
    "border border-paleo-line px-2 py-1 transition-colors enabled:hover:border-paleo-dim enabled:hover:text-paleo-cream disabled:cursor-not-allowed disabled:opacity-40";

  return (
    <nav className="mt-6 flex flex-wrap items-center justify-between gap-x-6 gap-y-3 border-t border-paleo-line pt-4 font-mono text-[10px] uppercase tracking-[0.2em] text-paleo-dim">
      <div className="flex items-center gap-2">
        <span>Show</span>
        {PAGE_SIZE_OPTIONS.map((size) => (
          <button
            key={size}
            type="button"
            onClick={() => onPageSizeChange(size)}
            aria-pressed={size === pageSize}
            className={`border px-2 py-1 transition-colors ${
              size === pageSize
                ? "border-paleo-accent bg-paleo-accent text-paleo-bg"
                : "border-paleo-line text-paleo-dim hover:border-paleo-dim hover:text-paleo-cream"
            }`}
          >
            {size}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-3">
        <span>
          {rangeStart}–{rangeEnd} of {total} {unit}
        </span>
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className={navButton}
          >
            ‹ Prev
          </button>
          <span className="whitespace-nowrap text-paleo-cream">
            {page} / {pageCount}
          </span>
          <button
            type="button"
            onClick={() => onPageChange(page + 1)}
            disabled={page >= pageCount}
            className={navButton}
          >
            Next ›
          </button>
        </div>
      </div>
    </nav>
  );
}
