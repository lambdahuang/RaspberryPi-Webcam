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
