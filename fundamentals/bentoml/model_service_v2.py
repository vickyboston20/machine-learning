from __future__ import annotations
import bentoml
from pydantic import BaseModel
from bentoml.models import BentoModel


class HouseInput(BaseModel):
    square_footage: float
    num_rooms: int
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
    model_ref = BentoModel("house_price_model_v2:latest")

    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(self.model_ref.tag)

    @bentoml.api
    def predict(self, data: HouseInput) -> PredictionOutput:
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

        prediction = self.model.predict(input_data)
        return PredictionOutput(predicted_price=prediction[0])
