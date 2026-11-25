# ADR 0001: Watermark-based incremental replication
Status: Accepted
Context: Full reloads are slow and costly on Snowflake.
Decision: Replicate by `updated_at` watermark with upsert on primary key.
Consequences: Hard deletes are not propagated; revisit with CDC/streams if needed.
