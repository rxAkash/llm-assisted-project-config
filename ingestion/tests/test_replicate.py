from ingestion.replicate import build_extract_sql, upsert_sql


def test_upsert_sql_updates_non_key_columns():
    sql = upsert_sql("orders", ["id", "amount"], "id")
    assert "ON CONFLICT (id) DO UPDATE SET amount=EXCLUDED.amount" in sql


def test_extract_sql_uses_watermark():
    assert "WHERE updated_at > %s" in build_extract_sql("orders", "updated_at")
