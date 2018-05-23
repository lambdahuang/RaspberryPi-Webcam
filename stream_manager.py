import socket
import threading
import sys
import os
from stream import CameraStream


class StreamServer(threading.Thread):
    _storage_directory = './storage/'
    output_manager = list()
    _logger = None

    def __init__(
        self,
        logger,
        storage_directory
    ):
        try:
            threading.Thread.__init__(self)
            self._logger = logger
            self._logger.info('Initialize stream server')
            self._storage_directory = storage_directory
            # initialize environ ment
            self._server_socket = socket.socket()
            self._server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1)
            self._server_socket.setsockopt(
                socket.IPPROTO_TCP,
                socket.TCP_NODELAY,
                1)
            self._server_socket.bind(('0.0.0.0', 8000))
            self._server_socket.listen(0)

        except Exception as e:
            logger.info(str(e))

    def run(self):
        self._logger.info(
                'Port is open, server is waiting '
                'for the remote steam.')
        while True:
            try:
                # Accept a single connection
                # and make a file-like object out of it
                connection, addr = self._server_socket.accept()
                self._logger.info(
                        'New stream comes: {}:{}'.format(
                            addr[0],
                            addr[1])
                )

                camera_stream = CameraStream(
                    connection,
                    self._storage_directory,
                    30,
                    self._logger)
                camera_stream.start()
                self.output_manager.append(camera_stream)
            except Exception as e:
                self._logger.warn('Failed to listen on port.' + str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                continue
