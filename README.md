[![Build Status](https://travis-ci.org/lambdahuang/RaspberryPi-Webcam.svg?branch=master)](https://travis-ci.org/lambdahuang/RaspberryPi-Webcam)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)


# Python Raspberry Pi Web Camera

![Output Example1](https://github.com/lambdahuang/RaspberryPi-Webcam/blob/readme_update/ExampleImages/example1.jpg)

This project allows you to easily configure your Raspberry Pi into a live-stream monitor!

It supports all versions of Raspberry Pi, as long as your Pi has a camera.

The server side is written by python flask. You can put it anywhere in any operating system, even in another pi!

# Features

1. `Live` video stream.
2. Purely `python-based` applet.
3. Support `image playback`, server periodically dump images to files.
4. `Web-based` server, DOES NOT require any client.
5. Support `global deployment`, as long as you have a public IP to run the server!


# Serverside Installation

Run following script to download and install the environment.
```
git clone https://github.com/lambdahuang/RaspberryPi-Webcam.git
cd RaspberryPi-Webcam
chmod +x install.sh
./install.sh
```

# Server Execution

To run server at terminal:
```
# In the project directory
source env/bin/activate
sudo python3 server.py
```

To run server at backend:
```
# In the project directory
source env/bin/activate
sudo nohup python3 server.py &
```

# Camera-side Installation

The installation is pretty similar to the server-side.
On the camera side, you only need the directory of *camera_side*. 
Copy the camera_side to a location on camera-side Pi, and execute following commands:
```
# Install the camera-side
cd camera_side/
chmod +x install.sh
./install.sh
```

# Issues with Installation

1. Clien-side installation failure.

Solution: This is probably caused by missing necessary image library. To install python image tool, execute following commands: `sudo apt-get install python-imaging libjpeg-dev zlib1g-dev` or `yum innstall python-imaging libjpeg-dev zlib1g-dev`.

# Auto-run Camera Script When Booting

There are many ways outside to autorun a script when booting the Pi.
I'm using the `/etc/rc.local` to realize the autorun,
by simply placing this `/home/pi/camera_side/env/bin/python3 /home/pi/camera_side/camera_client.py /home/pi/camera_side/camera_setting.ini &`
at the end of the file.

