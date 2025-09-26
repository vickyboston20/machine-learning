from __future__ import annotations
import bentoml
from pydantic import BaseModel
from bentoml.models import BentoModel

class HouseInput(BaseModel):
    square_footage: float
    num_rooms: int

class PredictionOutput(BaseModel):
    predicted_price: float

@bentoml.service(resources={"cpu": "500m"})
class HousePricePredictor:
    model_ref = BentoModel("house_price_model:latest")

    def __init__(self) -> None:
        # Load the model using BentoML's built-in loader
        self.model = bentoml.sklearn.load_model(self.model_ref.tag)

    @bentoml.api
    def predict(self, data: HouseInput) -> PredictionOutput:
        input_data = [[data.square_footage, data.num_rooms]]
        prediction = self.model.predict(input_data)
        return PredictionOutput(predicted_price=prediction[0])
