import { apiGet } from "@/lib/apiClient";
import type { Fossil } from "@/types/paleo";

/**
 * FOSSILS — API LAYER.  Maps to api/v1/routers/fossils.py.
 *
 * The router accepts mutually-exclusive `?species=` and `?genus=` filters. We
 * model that as an optional, narrowly-typed argument so callers can't pass both
 * by accident, and the function stays a thin, faithful wrapper of the endpoint.
 */
export type FossilFilter =
  | { by: "genus"; value: string }
  | { by: "species"; value: string }
  | undefined;

export function fetchFossils(filter: FossilFilter, signal?: AbortSignal): Promise<Fossil[]> {
  const params = filter ? { [filter.by]: filter.value } : undefined;
  return apiGet<Fossil[]>("/fossils", { params, signal });
}
