from mlops_pet.pipelines import register, training
from mlops_pet.pipelines.register.register_flow import main as register_flow
from mlops_pet.pipelines.training.training_flow import main as training_flow

__all__ = ["training", "training_flow", "register_flow", "register"]
