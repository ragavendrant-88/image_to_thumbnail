import time
import json
import pytest

from api import app_celery

import requests

@pytest.fixture
def dummyImage():
    dummyImageData = {
    }
    return dummyImageData

def test_convertToThumbnail(dummyImage):
    response = requests.post('http://localhost:5000/convertImage', data=json.dumps(dummyImage), headers={"content-type": "application/json"})
    assert response.status_code == 202
    assert response.json().get('success') == True
    assert response.json().get('token') is not None

def test_convertStatusProgress(dummyImage):
    convertResponse = requests.post('http://localhost:5000/convertImage', data=json.dumps(dummyImage), headers={"content-type": "application/json"})
    taskId = convertResponse.json().get('token')
    response = requests.get('http://localhost:5000/status/' + taskId, headers={"content-type": "application/json"})
    assert response.status_code == 200
    assert response.json().get('status') == "PENDING"
    assert response.json().get('resizedImageName') is None

def test_convertStatusFinished(dummyImage):
    convertResponse = requests.post('http://localhost:5000/convertImage', data=json.dumps(dummyImage), headers={"content-type": "application/json"})
    taskId = convertResponse.json().get('token')
    time.sleep(0.5)
    response = requests.get('http://localhost:5000/status/' + taskId, headers={"content-type": "application/json"})
    assert response.status_code == 200
    assert response.json().get('status') == "SUCCESS"
    assert response.json().get('resizedImageName') is not None