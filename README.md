[![multipleObjectTracker2D Homepage](https://img.shields.io/badge/multipleObjectTracker2D-develop-orange.svg)](https://github.com/davidvelascogarcia/multipleObjectTracker2D/tree/develop/programs) [![Latest Release](https://img.shields.io/github/tag/davidvelascogarcia/multipleObjectTracker2D.svg?label=Latest%20Release)](https://github.com/davidvelascogarcia/tensorflowLiteDetection2D/tags) [![Build Status](https://travis-ci.org/davidvelascogarcia/multipleObjectTracker2D.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/multipleObjectTracker2D)

# Multiple Object: Tracker 2D (Python API)

- [Introduction](#introduction)
- [Authors](#authors)
- [Running Software](#running-software)
- [Requirements](#requirements)
- [Status](#status)
- [Related projects](#related-projects)

## Authors

- David Velasco García: [@davidvelascogarcia](https://github.com/davidvelascogarcia)
- Franz García Boada: [@Franzmgarcia](https://github.com/Franzmgarcia)
- Antonio Ramón Otero: [@antoniorotero16](https://github.com/antoniorotero16)

## Introduction

`multipleObjectTracker2D` module use `OpenCV` Python API. This module tracks objects, people, animals or something that the user needs in a image source. `multipleObjectTracker2D` use `OpenCV` region of interest to select the region or different regions that the user need to track selecting with a rectangle with user mouse input.

`multipleObjectTracker2D` is a multipurpose tracker, that support different `OpenCV` trackers like `CSRT`, `GOTURN`, `KCF` ...

The module can be configured in [config.ini](./config) file, selecting the track you want to use, also image source size to be resize and improve speed.
By default use user webcam, but can be configured to use IP video source, local file or `OpenCV` supported sources.

Also this module has support to use `YARP` middleware, and can receive video source from `YARP` port, the module receive in `/multipleObjectTracker2D/img:i` port. Also publish in `YARP` network in `/multipleObjectTracker2D/img:o` processed image source. 

Centroid tracked object coordinates is published in `/multipleObjectTracker2D/data:o YARP` port.

The module can be used with or without `YARP` dependences and configured in [config.ini](./config) file.

## Running Software

- **Running without YARP support**
1. Execute [programs/multipleObjectTracker2D.py](./programs) the detector.
2. Select region to track and **q** to end selection or **c** to continue selecting multiple object to track.


- **Running with YARP support**

1. Configure [config.ini](./config) to select `yarp-mode` and `yarp-receive` if you want to use `YARP` input.
2. Create or configure YARP Server.
3. Connect `YARP` input port if needed.
```bash
yarp connect /videoSource /multipleObjectTracker2D/img:i
```
4. Execute [programs/multipleObjectTracker2D.py](./programs) the detector.
5. Select region to track and **q** to end selection or **c** to continue selecting multiple object to track.

NOTE:

- Video results are published on `/multipleObjectTracker2D/img:o`
- Coordinate results are published on `/multipleObjectTracker2D/data:o`


## Requirements

`multipleObjectTracker2D` requires:

* [Install pip3](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-pip.md)
* Install OpenCV and OpenCV Contrib
```bash
pip3 install opencv-python==3.4.6.27
pip3 install opencv-python-contrib==3.4.6.27
```
* [Install YARP 2.3.XX+](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-yarp.md) with Python 3 bindings


Tested on: `windows 10`, `ubuntu 16.04`, `ubuntu 18.04`, `lubuntu 18.04` and `kubuntu 20.04`.


## Status

[![Build Status](https://travis-ci.org/davidvelascogarcia/multipleObjectTracker2D.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/multipleObjectTracker2D)

[![Issues](https://img.shields.io/github/issues/davidvelascogarcia/multipleObjectTracker2D.svg?label=Issues)](https://github.com/davidvelascogarcia/multipleObjectTracker2D/issues)

## Related projects

* [OpenCV: Tracking API](https://docs.opencv.org/3.4/d9/df8/group__tracking.html)
* [OpenCV: Introducction to Tracking](https://docs.opencv.org/3.4/d2/d0a/tutorial_introduction_to_tracker.html)
* [davidvelascogarcia: Tensorflow: Detector 2D (PYTHON API)](https://github.com/davidvelascogarcia/tensorflowLiteDetection2D)
