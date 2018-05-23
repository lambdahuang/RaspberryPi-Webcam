import time
import os
from PIL import Image
import io
import struct
import pytz
import numpy as np
import cv2
from datetime import datetime
import threading
import sys


class CameraStream(threading.Thread):
    # initialize some statistical variables
    _bandwidth_calc_time = 0
    _bandwidth_calc_count = 0
    _bandwidth = 0
    _frame_count = 0
    _frame_per_second = 0

    # sender
    _sender_time_stamp = 0
    _last_shotcut_time = 0
    _shotcut_interval = 0

    # initialize shotcut functions
    _shotcut_directory = ''

    _camera_name = ''
    _connection = None
    _last_update = 0

    status = 'Inactive'

    def __init__(self, connection, storage_directory, shotcut_interval, logger):
        try:
            threading.Thread.__init__(self)
            self._connection = connection
            self._data_pipeline = connection.makefile('rb')
            self._camera_name = str(struct.unpack(
                '<50s',
                self._data_pipeline.read(struct.calcsize('<50s')))[0], 'utf-8').replace('\x00', '')
            self._shotcut_directory = os.path.join(storage_directory, self._camera_name)
            if not os.path.isdir(self._shotcut_directory):
                os.makedirs(self._shotcut_directory)
            self._last_update = time.time()
            self._shotcut_interval = shotcut_interval
            self.status = 'Active'
            self._logger = logger
        except Exception as e:
            self._logger.warn('Failed to listen on port.' + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        self._logger.info('The stream from {} is initialized.'.format(self._camera_name))

    def run(self):
        self._logger.info('Thread is running.')
        try:
            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                (sender_time_stamp, image_len) = struct.unpack(
                    '<1dL',
                    self._data_pipeline.read(struct.calcsize('<1dL'))
                )
                if not image_len:
                    break
                else:
                    self._bandwidth_calc_count = self._bandwidth_calc_count + image_len
                    self._frame_count = self._frame_count + 1

                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self._data_pipeline.read(image_len))

                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                self._image = Image.open(image_stream)
                self._cv_image = np.array(self._image)

                # calculate bandwidth
                if (time.time() - self._bandwidth_calc_time) >= 2:
                    bandwidth = self._bandwidth_calc_count / float(time.time() - self._bandwidth_calc_time) / 1000  # KB/S
                    frame_per_second = self._frame_count / float(time.time() - self._bandwidth_calc_time)

                    self._bandwidth_calc_time = time.time()
                    self._bandwidth_calc_count = 0
                    self._frame_count = 0

                self._put_text_on_image("{:.2f}KPS    {:.2f}FPS    {}".format(
                    bandwidth,
                    frame_per_second,
                    datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
                ))

                ret, self.image_output = cv2.imencode('.jpeg', self._cv_image, [cv2.IMWRITE_JPEG_QUALITY, 80])
                self._last_update = time.time()
                self._take_shotcut()

        finally:
            self._data_pipeline.close()
            self.status = 'Inactive'

    def _put_text_on_image(self, target_text):
        # turn the image into opencv compatible format
        cv2.putText(
            self._cv_image,
            target_text,
            (10, len(self._cv_image) - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.3,
            (255, 255, 255),
            1
        )

    def _take_shotcut(self):
        if time.time() - self._last_shotcut_time >= self._shotcut_interval:
            label = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern')).strftime('%y_%m_%d_%H_%M_%S')
            output_path = self._shotcut_directory + '/' + label + '.jpg'
            cv2.imwrite(output_path, self._cv_image)
            self._logger.info('Output image to file: {}'.format(output_path))
            self._last_shotcut_time = time.time()

    def get_status(self):
        if time.time() - self._last_update > 60:
            self.status = 'Inactive'
        else:
            return self.status

    def get_camera_name(self):
        return self._camera_name












