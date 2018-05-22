from flask import Flask, render_template, Response, url_for

import socket

import threading
import sys
import os
import logging
from stream import CameraStream
import atexit

app = Flask(__name__)

# initialize the log system
logger_format = '%(asctime)-30s %(levelname)-10s %(message)s'
formatter = logging.Formatter(logger_format)
hdlr = logging.FileHandler('./monitoring.log')
hdlr.setFormatter(formatter)

logging.basicConfig(format=logger_format)
logger = logging.getLogger('monitoring')
logger.setLevel(logging.INFO)
logger.addHandler(hdlr)

storage_directory = './storage/'


def get_stream_from_remote(server_socket):
    global output_manager
    logger.info('Port is open, server is waiting for the remote steam.')
    while True:
        try:
            # Accept a single connection and make a file-like object out of it
            connection, addr = server_socket.accept()
            logger.info('New stream comes: {}:{}'.format(addr[0], addr[1]))
            # thread.start_new_thread(stream_receiver, (connection.makefile('rb'),))
            camera_stream = CameraStream(
                connection,
                storage_directory,
                30,
                logger)
            output_manager.append(camera_stream)
        except Exception as e:
            logger.warn('Failed to listen on port.' + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            continue


@app.route('/huang593')
def index():
    global output_manager
    video_content = ""
    i = 0
    for camera_stream in output_manager:
        if camera_stream.get_status() == 'Active':
            video_content = video_content + """
            <div class="row">
                <div class="col-sm-12"></div>
                <h3>{cam_name}</h3>
                <img class="img-rounded img-responsive" style = "padding-left: 80px; padding-right: 80px;" src="{video_index}">
            </div>
            """.format(
                cam_name=camera_stream.get_camera_name(),
                video_index=url_for('video_feed', video_index=i))
        i = i + 1

    return render_template('index.html', video_content=video_content)


def gen(video_index):
    global output_manager
    while True:
        jpeg = output_manager[int(video_index)].image_output
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


@app.route('/video_feed<video_index>')
def video_feed(video_index):
    return Response(gen(video_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def global_initialization():
    global output_manager
    output_manager = list()


def shutdown_hook():
    """
    a shutdown hook to be called before the shutdown
    """
    global server_socket
    global thread_hdl
    try:
        server_socket.close()
        if 'thread_hdl' in globals():
            thread_hdl.stop()
    finally:
        logger.info('Shutdown')


if __name__ == '__main__':
    atexit.register(shutdown_hook)

    # initialize environ ment
    global_initialization()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    global thread_hdl
    thread_hdl = threading.Thread(target=get_stream_from_remote, args=(server_socket,))
    thread_hdl.start()
    # thread.start_new_thread(get_stream_from_remote, (server_socket,))
    app.run(host='0.0.0.0', port=80, threaded=True)
