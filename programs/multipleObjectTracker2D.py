'''
  * ************************************************************
  *      Program: Multiple Object Tracker 2D
  *      Type: Python
  *      Author: David Velasco Garcia @davidvelascogarcia
  *              Franz García Boada @Franzmgarcia
  *              Antonio Ramón Otero @antoniorotero16
  * ************************************************************
  *
  * | INPUT PORT                           | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /multipleObjectTracker2D/img:i       | Input image                                             |
  *
  *
  * | OUTPUT PORT                          | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /multipleObjectTracker2D/img:o       | Output image with tracker detection                     |
  * | /multipleObjectTracker2D/data:o      | Output result, coordinates tracker                      |
'''

# Libraries
from __future__ import print_function
import configparser
import cv2
import datetime
import os
import platform
from random import randint
import sys
import time
import numpy as np

# Variable to control yarp installed
try:
    import yarp
    yarpInstalled = 1

except:
    print("")
    print("[ERROR] Error, YARP middleware not installed, using not YARP mode.")
    print("")
    yarpInstalled = 0

# Function: objectTrackerBuilder
def objectTrackerBuilder(trackerType):

    # Build an object tracker based on his type
    if trackerType == objectTrackerTypesArray[0]:
        objectTracker = cv2.TrackerBoosting_create()

    elif trackerType == objectTrackerTypesArray[1]:
        objectTracker = cv2.TrackerMIL_create()

    elif trackerType == objectTrackerTypesArray[2]:
        objectTracker = cv2.TrackerKCF_create()

    elif trackerType == objectTrackerTypesArray[3]:
        objectTracker = cv2.TrackerTLD_create()

    elif trackerType == objectTrackerTypesArray[4]:
        objectTracker = cv2.TrackerMedianFlow_create()

    elif trackerType == objectTrackerTypesArray[5]:
        objectTracker = cv2.TrackerGOTURN_create()

    elif trackerType == objectTrackerTypesArray[6]:
        objectTracker = cv2.TrackerMOSSE_create()

    elif trackerType == objectTrackerTypesArray[7]:
        objectTracker = cv2.TrackerCSRT_create()

    else:
        objectTracker = None

        print("")
        print("[ERROR] Error Tracker Type selected not supported.")
        print("")

        print("[INFO] Supported Tracker Types:")
        print("")

        for objectTrackerTypes in objectTrackerTypesArray:
            print(objectTrackerTypes)

    return objectTracker

# Function: objetTrackerSelectTargets
def objetTrackerSelectTargets(rgbFrame, boxesArray, colorsArray):

    # Variable to control target selecction
    loopControlTargetSelection = 0

    while int(loopControlTargetSelection) == 0:

        # Call to interactive GUI selectROI  function
        boxObject = cv2.selectROI('[PROCESSED] multipleObjectTracker2D', rgbFrame)

        # Add region of interest to boxesArray
        boxesArray.append(boxObject)

        # Select random color to tracker object
        colorsArray.append((randint(0, 255), randint(0, 255), randint(0, 255)))

        print("")
        print("[INFO] Target selected and added correctly.")
        print("")

        print("")
        print("[INFO] Press q to end selection targets or press c to continue selecting targets.")
        print("")

        # If q is pressed
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):
            loopControlTargetSelection = 1

            print("")
            print("[INFO] Targets selection finished correctly, starting object tracking.")
            print("")

    return boxesArray, colorsArray

print("")
print("")
print("**************************************************************************")
print("**************************************************************************")
print("                  Program: Multiple Object Tracker 2D                     ")
print("                     Author: David Velasco Garcia                         ")
print("                             @davidvelascogarcia                          ")
print("**************************************************************************")
print("**************************************************************************")

print("")
print("Starting system ...")
print("")

print("")
print("Loading multipleObjectTracker2D module ...")
print("")

# Get system configuration
print("")
print("Detecting system and release version ...")
print("")
systemPlatform = platform.system()
systemRelease = platform.release()

print("")
print("**************************************************************************")
print("Configuration detected:")
print("**************************************************************************")
print("")
print("Platform:")
print(systemPlatform)
print("Release:")
print(systemRelease)

print("")
print("**************************************************************************")
print("Object Tracker Configuration:")
print("**************************************************************************")
print("")

# Variable to loopControlFileExists
loopControlFileExists = 0

while int(loopControlFileExists) == 0:

    # If file founded
    try:
        # Get object tarcker congiguration
        print("")
        print("Getting object tracker configuration ...")
        print("")
        configurationObject = configparser.ConfigParser()
        configurationObject.read('../config/config.ini')
        configurationObject.sections()

        videoSource = configurationObject['Configuration']['video-source']
        imgWidth = configurationObject['Configuration']['image-width']
        imgHeight = configurationObject['Configuration']['image-height']
        trackerType = configurationObject['Configuration']['tracker-type']
        yarpMode = configurationObject['Configuration']['yarp-mode']
        yarpReceive = configurationObject['Configuration']['yarp-receive']

        print("")
        print("[INFO] Video Source: " + str(videoSource))
        print("[INFO] Image Width: " + str(imgWidth))
        print("[INFO] Video Height: " + str(imgHeight))
        print("[INFO] Tracker Type: " + str(trackerType))
        print("[INFO] YARP Mode: " + str(yarpMode))
        print("[INFO] YARP Receive: " + str(yarpReceive))
        print("")

        # Image size
        image_w = int(imgWidth)
        image_h = int(imgHeight)

        # Set loopControlFileExists
        loopControlFileExists = 1

    # If file not founded
    except:
        print("")
        print("[ERROR] Sorry, config.ini not founded, waiting 4 seconds to the next check ...")
        print("")
        time.sleep(4)

print("")
print("[INFO] Data obtained correctly.")
print("")


if (int(yarpInstalled) == 1) and (int(yarpMode) == 1):

    print("")
    print("**************************************************************************")
    print("YARP configuration:")
    print("**************************************************************************")
    print("")
    print("Initializing YARP network ...")
    print("")

    # Init YARP Network
    yarp.Network.init()

    print("")
    print("[INFO] Opening image input port with name /multipleObjectTracker2D/img:i ...")
    print("")

    # Open input image port
    multipleObjectTracker2D_portIn = yarp.BufferedPortImageRgb()
    multipleObjectTracker2D_portNameIn = '/multipleObjectTracker2D/img:i'
    multipleObjectTracker2D_portIn.open(multipleObjectTracker2D_portNameIn)

    print("")
    print("[INFO] Opening image output port with name /multipleObjectTracker2D/img:o ...")
    print("")

    # Open output image port
    multipleObjectTracker2D_portOut = yarp.Port()
    multipleObjectTracker2D_portNameOut = '/multipleObjectTracker2D/img:o'
    multipleObjectTracker2D_portOut.open(multipleObjectTracker2D_portNameOut)

    print("")
    print("[INFO] Opening data output port with name /multipleObjectTracker2D/data:o ...")
    print("")

    # Open output data port
    multipleObjectTracker2D_portOutDet = yarp.Port()
    multipleObjectTracker2D_portNameOutDet = '/multipleObjectTracker2D/data:o'
    multipleObjectTracker2D_portOutDet.open(multipleObjectTracker2D_portNameOutDet)

    # Create data bootle
    outputBottleMultipleObjectTracker2D = yarp.Bottle()

    # Image size
    image_w = int(imgWidth)
    image_h = int(imgHeight)

    # Prepare input image buffer
    in_buf_array = np.ones((image_h, image_w, 3), np.uint8)
    in_buf_image = yarp.ImageRgb()
    in_buf_image.resize(image_w, image_h)
    in_buf_image.setExternal(in_buf_array.data, in_buf_array.shape[1], in_buf_array.shape[0])

    # Prepare output image buffer
    out_buf_image = yarp.ImageRgb()
    out_buf_image.resize(image_w, image_h)
    out_buf_array = np.zeros((image_h, image_w, 3), np.uint8)
    out_buf_image.setExternal(out_buf_array.data, out_buf_array.shape[1], out_buf_array.shape[0])

    print("")
    print("[INFO] YARP network configured correctly.")
    print("")

# Build objectTrackerTypesArray
objectTrackerTypesArray = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

print("")
print("**************************************************************************")
print("Initialize video source:")
print("**************************************************************************")
print("")
print("[INFO] Initializing video source ...")
print("")

# If YARP full receive mode is available
if (int(yarpInstalled) == 1) and (int(yarpMode) == 1) and (int(yarpReceive) == 1):

    # Receive image source
    frame = multipleObjectTracker2D_portIn.read()

    # Buffer processed image
    in_buf_image.copy(frame)
    assert in_buf_array.__array_interface__['data'][0] == in_buf_image.getRawImage().__int__()

    # YARP -> OpenCV
    rgbFrame = in_buf_array[:, :, ::-1]

    # Set success as True because wait until receive
    success = True

else:
    # Create VideoCapture object if webcam selected
    if str(videoSource) == "0":

        videoCaptureObject = cv2.VideoCapture(0)

    # If video file selected
    else:
        videoCaptureObject = cv2.VideoCapture(str(videoSource))

    # Get first frame
    # Variable to control get first frame
    loopControlGetFirstFrame = 0

    # Get 5 frame to prevent dark frame at staring webcam
    while int(loopControlGetFirstFrame) < 5:
        # Get Video Source frame
        success, rgbFrame = videoCaptureObject.read()

        # Count loopControlGetFirstFrame + 1
        loopControlGetFirstFrame = loopControlGetFirstFrame + 1

# If there is an error getting video source
if not success:
    print("")
    print("[ERROR] Error getting video source.")
    print("[INFO] Closing multipleObjectTracker2D program ...")
    print("")

    # Exit program
    sys.exit(1)

else:

    try:
        # Resize video source to selected resolution
        rgbFrame = cv2.resize(rgbFrame, (image_w, image_h))

        # Print commands
        print("")
        print("**************************************************************************")
        print("User controller:")
        print("**************************************************************************")
        print("")
        print("1. Select region of interest with mouse controller.")
        print("2. Press enter to save region of interest to be tracked.")
        print("3. Press q to end region selection and start to track, or press c to continue selecting more regions.")
        print("4. Press u with program is working to update or re-select region of interest.")
        print("")

        if (int(yarpInstalled) == 1) and (int(yarpMode) == 1):

            print("")
            print("**************************************************************************")
            print("YARP Ports:")
            print("**************************************************************************")
            print("")
            print("Processed image will be send by /multipleObjectTracker2D/img:o YARP port.")
            print("Processed target centroid coordinates will be send by /multipleObjectTracker2D/data:o YARP port.")
            print("")

    except:
        print("")
        print("[ERROR] Error resizing rgbFrame.")
        print("")

# Build boxesArray and colorsArray
boxesArray = []
colorsArray = []

print("")
print("[INFO] Initializing selection object tracking ...")
print("")

# Call objetTrackerSelectTargets function
boxesArray, colorsArray = objetTrackerSelectTargets(rgbFrame, boxesArray, colorsArray)

print("")
print("[INFO] Initializing multiple object tracker ...")
print("")

# Create multiTracker object
multipleObjectTracker = cv2.MultiTracker_create()

# Initialize multiTracker object with region of interest selected in each box of rgbFrame
for box in boxesArray:
    multipleObjectTracker.add(objectTrackerBuilder(trackerType), rgbFrame, box)

print("")
print("[INFO] Multiple object tracker Initialized correctly.")
print("")

# Variable to control loopControlReadImage
loopControlReadImage = 0

# Process image source to track object with source is active
while int(loopControlReadImage) == 0:

    # If YARP full receive mode is available
    if (int(yarpInstalled) == 1) and (int(yarpMode) == 1) and (int(yarpReceive) == 1):

        # Receive image source
        frame = multipleObjectTracker2D_portIn.read()

        # Buffer processed image
        in_buf_image.copy(frame)
        assert in_buf_array.__array_interface__['data'][0] == in_buf_image.getRawImage().__int__()

        # YARP -> OpenCV
        rgbFrame = in_buf_array[:, :, ::-1]

        # Set success as True because wait until receive
        success = True

    else:

        success, rgbFrame = videoCaptureObject.read()

    # If there is and error
    if not success:
        loopControlReadImage = 1
        break

    # If not error happened
    else:
        # Resize video source to selected resolution
        rgbFrame = cv2.resize(rgbFrame, (image_w, image_h))

        # Update multipleObjectTracker with new frame and update target box location to boxesArray
        success, boxesArray = multipleObjectTracker.update(rgbFrame)

        # Draw target detected box and name in rgbFrame for each target
        for color, newBox in enumerate(boxesArray):

            # Prepare point P1: Up-Left box point
            p1 = (int(newBox[0]), int(newBox[1]))

            # Prepare point P2: Down-Right box point, P1 + horizontal distance and P1 + vertical distance
            p2 = (int(newBox[0] + newBox[2]), int(newBox[1] + newBox[3]))

            # Draw rectangle in coordinates with prealculated random color
            cv2.rectangle(rgbFrame, p1, p2, colorsArray[color], 2, 1)

            # Add target ID down image
            cv2.putText(rgbFrame, "TARGET: " + str(int(color + 1)), (int(newBox[0]), int(newBox[1] + newBox[3]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorsArray[color], 2)

            # Get centroid coordinatesXY
            coordinateX = int(newBox[0]) + int(newBox[2]/2)
            coordinateY = int(newBox[1]) + int(newBox[3]/2)
            coordinatesXY = "X: " + str(coordinateX) + ", Y: " + str(coordinateY)

            # Print coordinatesXY local terminal
            print("")
            print("[INFO] TARGET: " + str(int(color + 1)) + ", COORDINATES: " + str(coordinatesXY))
            print("")

            # Send processed centroid coordinates by YARP Network
            if (int(yarpInstalled) == 1) and (int(yarpMode) == 1):

                # Sending processed centroid coordinates
                outputBottleMultipleObjectTracker2D.clear()
                outputBottleMultipleObjectTracker2D.addString("TARGET:")
                outputBottleMultipleObjectTracker2D.addInt(int(color + 1))
                outputBottleMultipleObjectTracker2D.addString("COORDINATES:")
                outputBottleMultipleObjectTracker2D.addString(coordinatesXY)
                outputBottleMultipleObjectTracker2D.addString("DATE:")
                outputBottleMultipleObjectTracker2D.addString(str(datetime.datetime.now()))
                multipleObjectTracker2D_portOutDet.write(outputBottleMultipleObjectTracker2D)

        # Dispay multipleObjectTracker processed rgbFrame
        cv2.imshow('[PROCESSED] multipleObjectTracker2D', rgbFrame)

        # If key u is pressed re-select targets
        if cv2.waitKey(33) == ord('u'):

            # Build boxesArray and colorsArray
            boxesArray = []
            colorsArray = []

            # Call objetTrackerSelectTargets function
            boxesArray, colorsArray = objetTrackerSelectTargets(rgbFrame, boxesArray, colorsArray)

            # Create multiTracker object to overwrite old
            multipleObjectTracker = cv2.MultiTracker_create()

            # Initialize multiTracker object with region of interest selected in each box of rgbFrame
            for box in boxesArray:
                multipleObjectTracker.add(objectTrackerBuilder(trackerType), rgbFrame, box)

            print("")
            print("[INFO] Multiple object tracker updated correctly.")
            print("")

    # Send processed image by YARP Network
    if (int(yarpInstalled) == 1) and (int(yarpMode) == 1):

        out_buf_array[:,:] = rgbFrame
        multipleObjectTracker2D_portOut.write(out_buf_image)


    # If key q is pressed exit programm
    if cv2.waitKey(33) == ord('q'):

        print("")
        print("[INFO] Key q pressed, finishing program ...")
        print("")
        break

if (int(yarpInstalled) == 1) and (int(yarpMode) == 1):

    # Close YARP ports
    print("[INFO] Closing ports ...")
    multipleObjectTracker2D_portIn.close()
    multipleObjectTracker2D_portOut.close()
    multipleObjectTracker2D_portOutDet.close()

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")
print("")
print("multipleObjectTracker2D program finished correctly.")
print("")
