from airflow.models import DagBag


def test_no_import_errors():
    bag = DagBag(dag_folder="airflow/dags", include_examples=False)
    assert not bag.import_errors
