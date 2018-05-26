import io
import socket
import struct
import time
import picamera
from PIL import Image
import configparser
import argparse


def run_camera(config_file):
    Config = configparser.ConfigParser()
    Config.read(config_file)

    camera_name = Config.get('camera', 'name')
    resolution_width = int(Config.get('camera', 'width'))
    resolution_height = int(Config.get('camera', 'height'))
    frame_rate = int(Config.get('camera', 'frame_rate'))
    rotation = int(Config.get('camera', 'rotation'))
    quality = int(Config.get('camera', 'quality'))
    compress_enable = int(Config.get('camera', 'compress_enable'))
    server_address = Config.get('camera', 'server_address')

    if Config.get('camera', 'hflip_enable') == '1':
        hflip_enable = True
    else:
        hflip_enable = False

    while(True):
        try:
            client_socket = socket.socket()
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print('connect to remote host..')
            client_socket.connect((server_address, 8000))
            connection = client_socket.makefile('wb')
        except Exception as e:
            print("Caught exception socket.error : {0}".format(str(e)))
            continue
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (resolution_width, resolution_height)
                camera.framerate = frame_rate
                camera.rotation = rotation
                camera.hflip = hflip_enable

                time.sleep(2)
                start = time.time()
                stream = io.BytesIO()
                compressed = io.BytesIO()
                # Use the video-port for captures...
                elapsed_time = time.time()
                frame_count = 0
                print('start transmitting..')

                # regist camera
                connection.write(struct.pack('<50s', camera_name.encode('utf-8')))

                for foo in camera.capture_continuous(stream, 'jpeg',
                                                     use_video_port=True):

                    if(compress_enable == 1):
                        stream.seek(0)
                        image = Image.open(stream)
                        image.save(compressed, 'jpeg', quality=quality)

                        time_stamp = time.time()

                        connection.write(struct.pack(
                            '<1dL',
                            time_stamp,
                            compressed.tell()))
                        connection.flush()

                        compressed.seek(0)
                        connection.write(compressed.read())

                        compressed.seek(0)
                        compressed.truncate()

                        stream.seek(0)
                        stream.truncate()
                    else:

                        time_stamp = time.time()

                        connection.write(struct.pack(
                            '<1dL',
                            time_stamp,
                            stream.tell()))
                        connection.flush()

                        stream.seek(0)
                        connection.write(stream.read())

                        stream.seek(0)
                        stream.truncate()

                    frame_count = frame_count + 1
                connection.write(struct.pack('<1dL', 0, 0))

        except Exception as e:
            print("Caught exception socket.error : {0}".format(str(e)))
            continue
        finally:
            pass
            connection.close()
            client_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_file',
        metavar='CONFIG_FILE',
        type=str,
        help='The path to the camera config file.'
    )
    args = parser.parse_args()
    run_camera(args.config_file)
