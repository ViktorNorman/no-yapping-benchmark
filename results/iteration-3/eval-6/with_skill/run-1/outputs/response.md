"Slowing us down" = the per-call queries scattered through the repo layer (N+1 on every list endpoint)? Start by collapsing those into batched fetches in `db/repository.ts`? (y / point me elsewhere)
