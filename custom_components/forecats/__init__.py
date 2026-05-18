import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall

from .forecats import generate_pet_pic
from .models import GenerateRequest

DOMAIN = "forecats"
_LOGGER = logging.getLogger(__name__)

PET_SCHEMA = vol.Schema(
    {
        vol.Required("name"): cv.string,
        vol.Required("description"): cv.string,
        vol.Required("type", default="cat"): cv.string,
    }
)

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("gemini_api_key"): cv.string,
        vol.Required("location"): cv.string,
        vol.Required("forecast"): dict,
        vol.Required("temperature_unit"): cv.string,  
        vol.Required("pets"): list[PET_SCHEMA],
        vol.Required("input_image_paths"): [cv.string],
        vol.Required("art_styles"): [cv.string],
        vol.Required("image_gen_aspect_ratio"): cv.string,
        vol.Required("image_gen_resolution"): cv.string,
        vol.Required("final_image_size"): cv.string,
        vol.Optional("display_profile"): cv.string,
    },
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the pet generator integration."""

    async def handle_generate(call: ServiceCall) -> None:
        data = GenerateRequest(
            **call.data,
        )  # look I know I validate twice but I cant be effed to refactor
        _LOGGER.info(f"Received generate_pet_picture service call with data: {data}")
        try:
            # Run in executor thread, pass HA config directory
            original_path, optimized_path = await hass.async_add_executor_job(
                generate_pet_pic,
                data,
                hass.config.path(),
            )

            _LOGGER.info(f"Generated pet pictures: {original_path}, {optimized_path}")

        except Exception:
            _LOGGER.exception("Failed to generate pet picture")

    hass.services.async_register(DOMAIN, "generate_pet_picture", handle_generate, SERVICE_SCHEMA)

    return True
