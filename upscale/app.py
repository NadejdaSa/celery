from flask import Flask, request, jsonify, send_file
from tasks import upscale_task
import io

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image = request.files['image']
    task = upscale_task.delay(image.read())
    return jsonify({'task_id': task.id}), 202

@app.route('/tasks/<task_id>', methods=['GET'])
def task_status(task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    response = {'tas_id': task_id, 'status': result.status}
    if result.status == 'SUCCESS':
        response['file_url'] = f'/processed/{task_id}.png'
    return jsonify(response)


@app.route('/processed/{file}', methods=['GET'])
def get_processed(file)
    from celery.result import AsyncResult
    task_id = file.replace('.png', '')
    result = AsyncResult(task_id)
    if result.status != 'SUCCESS':
        return  jsonify({'error': 'Not ready'}), 404
    return send_file(io.BytesIO(result.result), mimetype='image/png', as_attachment=True, download_name=file)