Before picking a fix, I'd want to know what's actually saturating. 5k writes/sec isn't inherently a Postgres wall — a tuned box on good hardware can do well past that. So the first question is: what's the bottleneck? CPU, disk IOPS/fsync, lock contention, connection count, or a few hot rows? The answer changes the recommendation a lot.

Quick framing on the three options:

- **Read replicas** solve read load, not write load. Since your pain is writes, replicas won't help the core problem. They're still worth adding if reads are also climbing and you can tolerate replication lag, but they don't address the 5k writes/sec ceiling.

- **Event sourcing** is an architecture change, not a scaling lever. It can make writes append-only (which is friendlier), but you take on projections, eventual consistency, replay complexity, and a big migration. Don't adopt it to fix throughput — adopt it only if you independently want the audit log / temporal model it gives you. It's the highest-risk, slowest-payoff option here.

- **Sharding** directly addresses write throughput by spreading writes across nodes. It's the right tool *if* writes are genuinely the wall — but it adds real cost: cross-shard queries, rebalancing, and picking a good shard key (for orders, usually customer_id or tenant_id, rarely order_id).

What I'd actually do, roughly in order:

1. **Squeeze the current box first.** Check `pg_stat_statements`, fsync/WAL settings, `synchronous_commit`, batching/`COPY` for bulk inserts, and connection pooling (PgBouncer — uncontrolled connections often masquerade as a write limit). Cheap wins frequently buy 2-3x and a year of runway.
2. **Scale vertically + tune** if you haven't maxed the instance — faster NVMe, more IOPS, partitioning hot tables by time.
3. **Then shard**, with a deliberate key, once you've confirmed writes are the true constraint and you've exhausted the easy gains. Citus is worth a look since it keeps you in Postgres rather than rewriting onto a new datastore.

Net: I'd default to sharding over the other two for a write problem, but I wouldn't shard yet. Tune and measure first — most "we've hit the Postgres write limit" turns out to be config, batching, or connection handling, not the engine. Can you share what the box looks like at peak (CPU %, disk wait, active connections) and whether writes are spread evenly or concentrated on a few tables?
