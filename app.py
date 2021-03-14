from api import app_celery, tasks
from flask import Flask, jsonify, request
import uuid


def runApp():
    app = app_celery.createApp()
    print('create app loaded')
    @app.route('/convertImage', methods=['POST'])
    def convertToThumnail():
        imgString = request.json['imageData']
        newFileID = str(uuid.uuid4())
        task = tasks.asyncConverterThumbnail.delay(newFileID, imgString)

        return jsonify({
            'success': True,
            'token': task.id,
        }), 202


    @app.route('/status/<token>', methods=['GET'])
    def getStatus(token):
        state = tasks.getStatus(token)
        return jsonify({
            'status': state.get('status'),
            'resizedImageName': state.get('info'),
        }), 200

    # start app
    app.run(host="0.0.0.0", port=5000, use_reloader=True)


if __name__ == "__main__":
    runApp()
