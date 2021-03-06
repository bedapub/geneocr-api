
from typing import List

from PIL.ExifTags import TAGS
from fastapi.routing import APIRouter
from fastapi import status
from PIL import Image
import pytesseract
from pytesseract import Output
from fastapi import File
import io
import os
import cv2
import numpy as np
from starlette.responses import StreamingResponse


from config.api_configs import COMMON_API_RESPONSE_MODELS
from schemas.image_analyzation_schema import ImageAnalyzationResponseModel
from helpers.text_area_detecting import detect_text_areas
from helpers.rotate import rotate_image

analyzation_namespace = APIRouter(prefix='/analyze')

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

@analyzation_namespace.post(
    '/image',
    description='Analyze text inside of image',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_analyzation_endpoint(file: bytes = File(...), response_format: str = 'string'):
    try:
        img = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
        h, w, c = img.shape
        if min((h, w)) < 300:
            scale_factor = float(350 / min((h, w))) * 1.5
            img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        else:
            img = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
        try:
            img = rotate_image(img)
        except Exception as e:
            pass
        img = cv2.resize(img, None, fx=3, fy=3, interpolation= cv2.INTER_AREA)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        text = pytesseract.image_to_string(img, lang='eng')
        if response_format == 'string':
            return ImageAnalyzationResponseModel(text=text, status="success", format="string")
        if response_format == 'array':
            split_text = text.split("\n")
            split_text = list(filter(lambda line: line.strip(), split_text))
            return ImageAnalyzationResponseModel(text=split_text, status="success", format="array")
        return ImageAnalyzationResponseModel(text=text, status="success", format="string")
    except Exception as e:
        print(e)
        return ImageAnalyzationResponseModel(status="failed", text=e, format=response_format)

    
@analyzation_namespace.post(
    '/text-area',
    description='Recognize text areas in image',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },

)
def image_analyzation_endpoint(file: bytes = File(...)):
    img = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
    img = detect_text_areas(img)
    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")




