
import cv2
from cv2 import dnn_superres
from io import BytesIO
from PIL import Image
import numpy as np

scaler = None

def load_model(path="EDSR_x2.pb"):
    global scaler
    if scaler is None:
        scaler = dnn_superres.DnnSuperResImpl_create()
        scaler.readModel(path)
        scaler.setModel("edsr", 2)
    return scaler

def upscale_image_bytes(image_bytes: bytes) -> BytesIO:
    model = load_model()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result_cv = model.upsample(img_cv)
    result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)
    result_pil = Image.fromarray(result_rgb)
    output_io = BytesIO()
    result_pil.save(output_io, format='PNG')
    output_io.seek(0)
    return output_io

def example():
    with open('lama_300px.png', 'rb') as f:
        input_bytes = f.read()
    result_io = upscale_image_bytes(input_bytes)
    with open('lama_600px.png', 'wb') as out_f:
        out_f.write(result_io.getbuffer())
            
if __name__ == '__main__':
    example()
