import mlflow
from typer.testing import CliRunner

from mlops_pet import cli, definitions

runner = CliRunner()


def test_infrastructure():
    result = runner.invoke(cli.app, ["train", "--test", "--date", "2022-01-01", "--num-trials", 2])
    assert result.exit_code == 0
    client = mlflow.MlflowClient()
    exp = client.get_experiment_by_name(definitions.EXPERIMENT_NAME)
    assert exp is not None

    runs = client.search_runs(experiment_ids=exp.experiment_id)
    # assert len(runs) == 2
    result = runner.invoke(cli.app, ["register-best-model", "--test"])
    print("Infrastructure was successfully tested.")


if __name__ == "__main__":
    test_infrastructure()
