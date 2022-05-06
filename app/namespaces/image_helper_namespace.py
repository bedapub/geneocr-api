
from fastapi.routing import APIRouter
from fastapi import status
from fastapi import File
import cv2
import numpy as np
import io
from config.api_configs import COMMON_API_RESPONSE_MODELS

from helpers.rotate import rotate_image

from helpers.image_super_resolution import preprocess_image, model_image, save_image

image_helper_namespace = APIRouter(prefix='/image-helper')
from starlette.responses import StreamingResponse

@image_helper_namespace.post(
    '/rotate',
    description='Rotates image, so the text is horizontal aligned',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_analyzation_endpoint(file: bytes = File(...)):
    img = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
    rotated = rotate_image(img)
    res, im_png = cv2.imencode(".png", rotated)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@image_helper_namespace.post(
    '/sharpen',
    description='Sharpen image with tenserflow model',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_analyzation_endpoint(file: bytes = File(...)):
    image = preprocess_image(file)
    image = model_image(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    res, im_png = cv2.imencode(".png", image)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

