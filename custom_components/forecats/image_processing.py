"""Image processing utilities for forecats."""

import logging

from PIL import Image, ImageOps

logger = logging.getLogger("forecats")


def resize_image(image: Image.Image, final_size: str) -> Image.Image:
    """Crop then resize image to specified width and height.

    Returns the original image if final size is not in the correct format.

    Args:
        image: PIL Image to be resized
        final_size: String in format "WIDTHxHEIGHT", e.g. "512x512"

    """
    if "x" not in final_size:
        logger.warning(f"Could not parse image size {final_size}, returning original image")
        return image

    width, height = map(int, final_size.split("x"))
    image = ImageOps.fit(
        image,
        size=(width, height),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    return image


def recolor_image(image: Image.Image, profile: str | None) -> Image.Image:
    """Recolor image based on display profile.

    Args:
        image: PIL Image to be recolored.
        display_profile: Display profile string

    """
    if not profile or profile not in DISPLAY_PROFILES:
        logger.warning(f"Display profile {profile} not found, returning original image")
        return image

    if image.mode != "RGB":
        image = image.convert("RGB")

    # Build palettes
    color_map = DISPLAY_PROFILES[profile]["color_map"]

    device_palette = []  # This is the palette in the device specs
    true_palette = []  # This is the palette that the device actually displays irl
    for c in color_map:
        true_color = color_map[c]
        true_palette.extend(_hex_to_rgb(true_color))
        device_palette.extend(_hex_to_rgb(c))
    true_palette.extend([0] * (256 * 3 - len(true_palette)))
    device_palette.extend([0] * (256 * 3 - len(device_palette)))

    # Dither based on palette
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette(true_palette)
    quantized = image.quantize(palette=palette_image, dither=Image.Dither.FLOYDSTEINBERG)

    # Convert to device palette
    quantized.putpalette(device_palette)
    image = quantized.convert("RGB")

    return image


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    lv = len(hex_color)
    return tuple(int(hex_color[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


DISPLAY_PROFILES = {
    "spectra6": {
        "color_map": {
            "#000000": "#191E21",  # Black
            "#FFFFFF": "#E8E8E8",  # White
            "#0000FF": "#2157BA",  # Blue
            "#00FF00": "#125F20",  # Green
            "#FF0000": "#B21318",  # Red
            "#FFFF00": "#EFDE44",  # Yellow
        },
    },
}
