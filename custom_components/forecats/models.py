from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    type: str
    description: str


class GenerateRequest(BaseModel):
    """Request model for generating pet pictures."""

    gemini_api_key: str

    location: str
    forecast: dict
    temperature_unit: str
    pets: list[Pet]
    input_image_paths: list[str]
    art_styles: list[str]

    image_gen_aspect_ratio: str
    image_gen_resolution: str
    final_image_size: str

    display_profile: str | None
