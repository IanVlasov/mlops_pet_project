# MLOps Pet Project

## Checklist for the reviewer

- [x] Problem description can be found below.
- [x] Project infrastructure is deployed using IaC (CloudFormation)
- [x] Experiment tracking and model registry are used (MLFlow)
- [ ] Workflow deployment (Prefect)
- [x] Containerize model deployment code (Docker)
- [ ] The model deployment code is containerized and could be deployed on cloud
- [ ] No model monitoring.
- [ ] Instructions can be found below.
- [x] Unit tests
- [x] Integration tests
- [x] Linters
- [x] Makefile
- [x] pre-commit hooks
- [ ] CI/CD pipeline

## Project description

This is the demonstration project to show how to apply MLOps practices on data science project.
The solution is based on [mlops-zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) lectures.
For demonstration purposes [NYC Yellow Taxi Trip Records](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
are used. The model showed here is designed to make fare predictions for each taxi trip using
several simple features. This project does not cover extensive and advanced techniques of EDA, feature engineering
and model design.

### This project covers
* Demonstrates practical aspects of production ML services.
* ML model lifecycle:
  * Training and tracking experiments.
  * Deployment of the scheduled jobs with the model in Production.
  * Model deployment as a stream service that runs on cloud
* Preparing the whole infrastructure for AWS using Infrastructure as Code (IaC) service (CloudFormation).
* Best practices of software engineering:
  * Unit tests
  * Integration tests
  * Linters
  * Makefiles
  * Pre-commit hooks
  * CI/CD pipeline


