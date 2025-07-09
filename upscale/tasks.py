from celery import Celery
from upscale import upscale_image_bytes

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def upscale_task(image_bytes):
    result_io = upscale_image_bytes(image_bytes)
    return result_io.getvalue()