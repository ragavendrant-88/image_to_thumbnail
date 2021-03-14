from celery import Celery
from PIL import Image
import logging
import base64
import os
import time

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

# Task to convert thumbnail
@celery.task(bind=True)
def asyncConverterThumbnail(self, fileId, imgString):
    logger.info("Started resizing...")
    self.update_state(state='IN_PROGRESS', meta=None)

    tempFilename = fileId + "_temp.jpg"

    with open(tempFilename, "wb") as fh:
        fh.write(base64.decodebytes(imgString.encode()))
    img = Image.open(tempFilename) 

    # For .png images where there is no alpha
    rgbImg = img.convert('RGB')
    newFilename = fileId + ".jpg"
    newImg = rgbImg.resize((100,100), Image.ANTIALIAS)
    newImg.save(newFilename,'JPEG',optimize=True, quality=100)

    # Sleep to test task status
    logger.info("Completed resizing...")

    # Remove the temporary file
    try:
        os.remove(tempFilename)
    except OSError:
        pass
    return newFilename


def getStatus(taskId):
    task = celery.AsyncResult(taskId)
    state = {'status': task.status, 'info': task.info}
    return state
