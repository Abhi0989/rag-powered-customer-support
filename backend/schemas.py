
from pydantic import BaseModel, Field
from typing import List


class EmailAnalysis(BaseModel):

    category: str = Field(
        description="Technical issue category"
    )

    priority: str = Field(
        description="Low, Normal, High or Critical"
    )

    summary: str

    machine_model: str | None = None

    error_codes: List[str] = Field(
        default_factory=list
    )

    issue_description: str

    order_numbers: List[str] = Field(
        default_factory=list
    )

    missing_information: List[str] = Field(
        default_factory=list
    )

    recommended_department: str

    evidence_summary: str = ""


class DraftResponse(BaseModel):

    response: str
