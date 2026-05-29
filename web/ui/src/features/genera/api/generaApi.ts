import { apiGet } from "@/lib/apiClient";
import type { Genus, GenusDetail } from "@/types/paleo";

/**
 * ============================================================================
 *  GENERA — API LAYER
 * ============================================================================
 *
 *  This is the frontend mirror of your backend's `genus_service` + router. It
 *  knows the endpoints, the query params, and the response types — and NOTHING
 *  about React. That separation matters: these are plain async functions you
 *  could unit-test or call from a script. React Query (in the hooks layer) is
 *  what turns them into cached, reactive component data.
 *
 *  Maps to:  api/v1/routers/genera.py
 */

/** GET /genera  → list of lightweight GenusRead records. */
export function fetchGenera(signal?: AbortSignal): Promise<Genus[]> {
  return apiGet<Genus[]>("/genera", { signal });
}

/**
 * GET /genera?name=...  → the backend returns a single match, but its
 * response_model is `list[GenusRead]`-shaped for the unfiltered case and a
 * single object for the `name` case. We normalize to "one Genus" here so the
 * hook layer doesn't have to care.
 */
export function fetchGenusByName(name: string, signal?: AbortSignal): Promise<Genus> {
  return apiGet<Genus>("/genera", { params: { name, detail: "basic" }, signal });
}

/** GET /genera/{id}?detail=full  → the full GenusDetail record. */
export function fetchGenusById(id: number, signal?: AbortSignal): Promise<GenusDetail> {
  return apiGet<GenusDetail>(`/genera/${id}`, { params: { detail: "full" }, signal });
}
