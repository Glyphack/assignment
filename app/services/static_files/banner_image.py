from app.core import config


def get_banner_image_url(image_name: str):
    return f"{config.STATIC_CONTENT_BASE_URL}/images/image_{image_name}.png"
