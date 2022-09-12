from mlops_pet import definitions
from mlops_pet.deployment import model

PREDICTIONS_STREAM_NAME = definitions.PREDICTIONS_STREAM_NAME
MODEL_NAME = definitions.MODEL_NAME
TEST_RUN = definitions.TEST_RUN


model_service: model.service.ModelService = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    model_name=MODEL_NAME,
    test_run=TEST_RUN,
)


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    return model_service.lambda_handler(event)
