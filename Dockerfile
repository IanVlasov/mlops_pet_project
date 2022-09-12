FROM public.ecr.aws/lambda/python:3.9

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.0 \
  LAMBDA_TASK_ROOT="/"

RUN pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
RUN yum install -y gcc python3-devel

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml README.md /code/

## Creating folders, and files for a project:
COPY ./mlops_pet /code/mlops_pet

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install -E tests --no-interaction --no-ansi --no-dev


COPY [ "./mlops_pet/deployment/lambda_function.py", "/" ]

WORKDIR /
CMD [ "lambda_function.lambda_handler" ]
