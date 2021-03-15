# image_to_thumbnail

## To Start the application

```
docker-compose up -d --build
```

## API ENDPOINTS

### For converting the image to thumbnail

* URL

  /convertImage

* Method

  `POST`

* Data Params

  request.json <sample image in base64>

* Response

  * Code: 202
    Content: {"success": true, "token": "<uuid>"}

* Sample Call

  curl -H "Content-Type: application/json" -d @request.json http://localhost:5000/convertImage

### For getting the status

* URL

  /status

* Method

  `GET`

* URL Params

  <token>

* Response

  * Code: 200
    Content: {"resizedImageName": <converted/image/jpg>, "status": "success"}

* Sample Call

  curl http://localhost:5000/status/<token>

### To run test

Create and activate virtual environment then run the following command.

```
python -m pytest
```

## Architecture

![Architecture](./Architecture.png)