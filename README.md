# MLOps Pet Project

## Checklist for the reviewer

- [x] Problem description can be found below.
- [x] Project infrastructure is deployed using IaC (CloudFormation)
- [x] Experiment tracking and model registry are used (MLFlow)
- [x] Basic workflow orchestration (Prefect)
- [x] The model deployment code is containerized and can be deployed on cloud
- [ ] No model monitoring.
- [x] Instructions can be found below.
- [x] Unit tests
- [x] Integration tests
- [x] Linters
- [x] Makefile
- [x] pre-commit hooks
- [x] CI/CD pipeline

## Project description

This is the demonstration project to show how to apply MLOps practices on data science project.
The solution is based on [mlops-zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) lectures.
For demonstration purposes [NYC Yellow Taxi Trip Records](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
are used. The model showed here is designed to make fare predictions for each taxi trip using
several simple features. This project does not cover extensive and advanced techniques of EDA, feature engineering
and model design.

### This project covers

- Demonstrates practical aspects of production ML services.
- ML model lifecycle:
  - Training and tracking experiments.
  - Deployment of the scheduled jobs with the model in Production.
  - Model deployment as a stream service that runs on cloud
- Preparing the whole infrastructure for AWS using Infrastructure as Code (IaC) service (CloudFormation).
- Best practices of software engineering:
  - Unit tests
  - Integration tests
  - Linters
  - Makefiles
  - Pre-commit hooks
  - CI/CD pipeline

## Instructions

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Poetry](https://python-poetry.org/docs/)
- [AWS CLI](https://aws.amazon.com/cli/)

### Data and model description

As it has already been mentioned, here NYC Yellow Taxi dataset is used. The model will predict fare amount based on several
features: `passengers_count`, `trip_distance`, `pickup_hour`, `pickup_minutes`, `day of week`.
In the `mlops_pet/pipelines` folder the training and deployment code can be found. They are organized in prefect flows and split on tasks.

### First steps

To install the project with all extras simply run

```
poetry install -E tests -E deployment -E eda
```

This command will install simple CLI commands which you can execute using `mlops_pet` package.
First of all you need to setup your environment variables. Please, run

```
mlops_pet setup
```

in your terminal and fill the values. At startup default values are configured to successfully run
integration tests.

You can run `mlops_pet --help` command to see other available commands

### Tests

To run tests which are defined in the Makefile type

```
make integration_test
```

This command will start the full test pipeline including unit tests which are required for
the integration test.

The integration test repeats production infrastructure locally using docker to start MLFlow and Prefect
servers with the necessary storages and databases. It trains model, registers it, pulls it from the registry and uses it to make
predictions using Kinesis stream.

### Production infrastructure

The whole infrastructure is defined in cloudformation folder. It consists of:

- MLFlow server with Postgres DB and S3 bucket for tracking and storage servers.
- Prefect server

To deploy this infrastructure using your AWS account run

```
bash ./cloudformation/deploy-stack.sh
```

> **NB!**
> Running this command you may be charged for using some resources on AWS.

> **NB!**
> Current infrastructure is configured to be open for everyone in demonstration purpposes.
> Be sure you have prepared additional security steps before deploying this code into your
> organization workflow.

As outputs you will get several links for MLFlow server, Prefect server and S3 bucket.
You can use them to setup production infrastructure by running `mlops_pet setup`.

### Best practices

- Simple unit tests and integration tests can be found in `tests` folder
- Pre-commit hooks setup several checks including linters. The setup can be found in `.pre-commit-config.yaml`
- `Makefile` is available in the root directory
- Simple CI/CD pipeline job can be found in the following demonstration [Merge request](https://github.com/IanVlasov/mlops_pet_project/pull/2). The definition of github actions is available in `.github` folder.
