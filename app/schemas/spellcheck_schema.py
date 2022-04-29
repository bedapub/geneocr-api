from typing import Any, List
from pydantic import BaseModel, Field


class SpellCheckRequestModel(BaseModel):
    value: List[str] = Field(
        ...,
        description='Array of words that will be check for correct spelling'
    )
    options: Any = Field(
        None,
        description='Options for spell checking'
    )

class SpellCheckModel(BaseModel):
    initial_word: str = Field(
        ...,
        desciption='Initial word'
    )
    gene_exists: bool = Field(
        ...,
        description='Does initial word exist in gene list'
    )
    suggestions: List[str] = Field(
        [],
        description='Suggestions for correct spelling of initial word'
    )
    best_canditate: str = Field(
        None,
        description='Best candidate for correct spelling'
    )