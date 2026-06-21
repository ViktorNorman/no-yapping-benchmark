Read replicas don't help you here. Your problem is writes (5k/sec), and replicas only offload reads. They're worth adding anyway if reads are also hot, but they won't touch the write ceiling.

So the real choice is shard vs. event sourcing. They solve different problems, and event sourcing is not a scaling fix — it's a data-model change that happens to enable some scaling patterns. Don't reach for it to buy headroom.

What I'd do, in order:

1. First confirm you've actually hit Postgres's limit, not a config/hardware limit. 5k writes/sec is not inherently a lot for one well-tuned box. Before sharding, check:
   - Are you on a write-bound instance? Bump IOPS / move to faster disks first — cheapest possible win.
   - `synchronous_commit`, `wal_writer_delay`, `max_wal_size`, checkpoint tuning. Misconfigured WAL is the usual culprit at this scale.
   - Are writes fighting indexes? Every index multiplies write cost. Drop unused ones.
   - Batch where you can — group commits, multi-row inserts.
   A tuned single Postgres can often clear 10–20k writes/sec on decent hardware. If you haven't exhausted this, you're about to take on sharding complexity to dodge a config change.

2. If you're genuinely at the box's limit, shard. For an orders service the shard key is usually obvious — customer_id or order_id (hash). Orders are naturally partitionable: most queries scope to one customer, and cross-customer transactions are rare. That's close to the ideal sharding case. Use Citus (Postgres extension, keeps you in the Postgres world) before hand-rolling app-level sharding. The cost you take on: cross-shard queries, rebalancing, and any global invariant (uniqueness, aggregate reporting) gets harder.

3. Event sourcing — only if you have a separate, real need for it: full audit trail, temporal queries ("what did this order look like on date X"), or you want to derive multiple read models from one write log. It changes how you reason about every read and write, demands tooling for replay/versioning/snapshots, and your team pays that tax forever. It does not by itself raise your write throughput — your event store still has to absorb 5k/sec. If "we need to scale writes" is the only driver, this is the wrong tool.

My actual recommendation: tune and verify the single instance first (days of work, possibly solves it outright). If you're truly at the limit, shard by customer_id via Citus. Add read replicas in parallel if reads are also straining. Leave event sourcing out of the scaling decision — adopt it later, deliberately, only if the audit/temporal/read-model needs show up on their own.

One caveat worth flagging: if writes are climbing fast and you're already at the ceiling, don't burn weeks tuning — set a threshold (e.g. "if tuning doesn't get us to 2x headroom in a week, we shard") so you don't optimize a box you're about to outgrow anyway.

This is a real design call with org and ops implications — if you want to go deep on shard-key choice or a Citus migration plan, probably worth a dedicated chat.
