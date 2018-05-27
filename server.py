from flask import Flask, render_template, Response, url_for
import logging
import atexit
from stream_manager import StreamServer
import time

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


@app.route('/huang593')
def index():
    global stream_manager
    video_content = ""
    i = 0
    for camera_stream in stream_server.output_manager:
        if camera_stream.get_status() == 'Active':
            video_content = video_content + """
            <div class="row">
                <div class="col-sm-12"></div>
                <h3>{cam_name}</h3>
                <img class="img-rounded img-responsive" style =\
            "padding-left: 80px; padding-right: 80px;" src="{video_index}">
            </div>
            """.format(
                cam_name=camera_stream.get_camera_name(),
                video_index=url_for('video_feed', video_index=i))
        i = i + 1

    return render_template('index.html', video_content=video_content)


def gen(video_index):
    global stream_server
    while True:
        jpeg = stream_server.output_manager[int(video_index)].image_output
        time.sleep(0.1)  # to avoid overrun the visitor.
        yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                jpeg.tobytes() + b'\r\n')


@app.route('/video_feed<video_index>')
def video_feed(video_index):
    return Response(gen(video_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def shutdown_hook():
    """
    a shutdown hook to be called before the shutdown
    """
    logger.info('Shutdown')


if __name__ == '__main__':
    atexit.register(shutdown_hook)
    global stream_server
    stream_server = StreamServer(logger, './storage/')
    stream_server.start()
    app.run(host='0.0.0.0', port=80, threaded=True)
