from __future__ import annotations
import bentoml
from pydantic import BaseModel
from bentoml.models import BentoModel

class BaseHouseInput(BaseModel):
    square_footage: float
    num_rooms: int


class V1HouseInput(BaseHouseInput):
    pass


class V2HouseInput(BaseHouseInput):
    num_bathrooms: int
    house_age: int
    distance_to_city_center: float
    has_garage: int
    has_garden: int
    crime_rate: float
    avg_school_rating: float
    country: str


class PredictionOutput(BaseModel):
    predicted_price: float


@bentoml.service(resources={"cpu": "500m"})
class HousePricePredictor:
    v1_model_ref = BentoModel("house_price_model:latest")
    v2_model_ref = BentoModel("house_price_model_v2:latest")

    def __init__(self) -> None:
        self.v1_model = bentoml.sklearn.load_model(self.v1_model_ref.tag)
        self.v2_model = bentoml.sklearn.load_model(self.v2_model_ref.tag)


    @bentoml.api
    def predict_v1(self, data: V1HouseInput) -> PredictionOutput:
        input_data = [[data.square_footage, data.num_rooms]]
        prediction = self.v1_model.predict(input_data)
        return PredictionOutput(predicted_price=prediction[0])
    
    @bentoml.api
    def predict_v2(self, data: V2HouseInput) -> PredictionOutput:
        # One-hot encode 'country' manually
        country_encoded = [0, 0, 0]  # Default for ['Canada', 'Germany', 'UK']
        if data.country == "Canada":
            country_encoded[0] = 1
        elif data.country == "Germany":
            country_encoded[1] = 1
        elif data.country == "UK":
            country_encoded[2] = 1

        # Create DataFrame with correct column names
        input_data = [[
            data.square_footage, data.num_rooms, data.num_bathrooms, data.house_age,
            data.distance_to_city_center, data.has_garage, data.has_garden,
            data.crime_rate, data.avg_school_rating
        ] + country_encoded]

        prediction = self.v2_model.predict(input_data)
        return PredictionOutput(predicted_price=prediction[0])
    

