from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.protobuf.json_format import MessageToDict
import pandas as pd
import numpy as np
import io
import sys
from . import kyc_config as cfg

client = vision_v1.ImageAnnotatorClient.from_service_account_file(cfg.gcv_api_key_path)

def get_text_response_from_path(path):

    output = None

    try:
        if path.startswith('http') or path.startswith('gs:'):
            image = vision_v1.types.Image()
            image.source.image_uri = path
        else:
            with io.open(path, 'rb') as image_file:
                content = image_file.read()
            image = vision_v1.types.Image(content=content)

    except ValueError:
        output = "Cannot Read Input File"
        return output

    response = client.text_detection(image=image)
    text_response = MessageToDict(response._pb)
    return text_response

def process_ocr(img_path):
    text_response = get_text_response_from_path(img_path)

    img_name = img_path.split('/')[-1].split('.')[0]
    json_name = cfg.json_loc+'ocr_'+img_name+'.npy'
    np.save(json_name, text_response)

# if __name__ == '__main__':
#     if(len(sys.argv) > 1):
#         img_path = sys.argv[1]
#         print('OCR processing '+img_path)
#         process_ocr(img_path)
#     else:
#         print('argument is missing: image path')
