from mlops_pet.deployment.model import kinesis, service, utils


def init(
    prediction_stream_name: str,
    model_name: str,
    test_run: bool = False,
) -> service.ModelService:
    model = utils.load_model(model_name)

    callbacks = []

    # if not test_run:
    #     kinesis_client = utils.create_kinesis_client()
    #     kinesis_callback = kinesis.KinesisCallback(kinesis_client, prediction_stream_name)
    #     callbacks.append(kinesis_callback.put_record)

    model_service = service.ModelService(model=model, model_version=model_name, callbacks=callbacks)

    return model_service
