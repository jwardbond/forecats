from pydantic import BaseModel, model_validator


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
    input_image_paths: list[str] | None = None
    input_image_dir: str | None = None
    art_styles: list[str]

    image_gen_aspect_ratio: str
    image_gen_resolution: str
    final_image_size: str

    display_profile: str | None

    @model_validator(mode="after")
    def check_images_provided(self):
        if not self.input_image_paths and not self.input_image_dir:
            raise ValueError("Either input_image_paths or input_image_dir must be provided.")
        return self
