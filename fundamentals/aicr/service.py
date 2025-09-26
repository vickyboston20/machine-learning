from __future__ import annotations
import bentoml
from typing import List
from pydantic import BaseModel
import pandas as pd
from bentoml.models import BentoModel


# Input schema for each row
class HealthClaimInput(BaseModel):
    claim_amount: float
    num_services: int
    patient_age: int
    provider_id: int
    days_since_last_claim: int

# Output schema
class PredictionOutput(BaseModel):
    predictions: List[int]

@bentoml.service(resources={"cpu": "500m"})
class HealthInsuranceAnomalyDetectionService:
    model_ref = BentoModel("health_insurance_anomaly_detector:latest")

    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(self.model_ref.tag)

    @bentoml.api
    def predict(self, data: pd.DataFrame) -> PredictionOutput:
        """
        API endpoint to detect anomalies in health insurance claims.
        It accepts a Pandas DataFrame and returns a list of predictions.
        """
        predictions = self.model.predict(data)
        return PredictionOutput(predictions=predictions.tolist())