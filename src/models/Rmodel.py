from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class PricePredictionRequest(BaseModel):
    property_type: str
    property_subtype: str
    area: str
    actual_area: float = Field(..., gt=0)
    rooms: int = Field(..., ge=0)
    parking: int = Field(..., ge=0)
    is_offplan: bool
    is_freehold: bool
    usage: str
    nearest_metro: Optional[str] = None
    nearest_mall: Optional[str] = None
    master_project: Optional[str] = None
    project: str

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal


class PricePredictionRequest(BaseModel):
    property_type: Literal["Unit", "Building", "Land"]
    property_subtype: str = Field(..., min_length=2)

    area: str = Field(..., min_length=2)

    actual_area: float = Field(..., gt=0, description="Area must be positive")
    rooms: int = Field(..., ge=0, le=10)
    parking: int = Field(..., ge=0, le=10)

    is_offplan: bool
    is_freehold: bool

    usage: Literal["Residential", "Commercial"]

    nearest_metro: Optional[str]
    nearest_mall: Optional[str]
    master_project: Optional[str]
    project: str = Field(..., min_length=2)

    # ---------- Custom Validators ----------

    @field_validator("actual_area")
    def area_reasonable(cls, v):
        if v > 20000:
            raise ValueError("actual_area cannot be bigger than 2000")
        return v

    @field_validator("project")
    def project_not_blank(cls, v):
        if not v.strip():
            raise ValueError("project cannot be empty")
        return v

class ConfidenceInterval(BaseModel):
    lower: float
    upper: float


class PricePredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: ConfidenceInterval
    price_per_sqft: float
    model_confidence: str
    key_factors: List[str]
