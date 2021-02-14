'''
  * ************************************************************
  *      Program: Multiple Object Tracker 2D
  *      Type: Python
  *      Author: David Velasco Garcia @davidvelascogarcia
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
from halo import Halo
import numpy as np
import platform
from random import randint
import time
import yarp


class MultipleObjectTracker2D:

    # Function: Constructor
    def __init__(self):

        # Build Halo spinner
        self.systemResponse = Halo(spinner='dots')

        # Build object tracker types
        self.objectTrackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

    # Function: getSystemPlatform
    def getSystemPlatform(self):

        # Get system configuration
        print("\nDetecting system and release version ...\n")
        systemPlatform = platform.system()
        systemRelease = platform.release()

        print("**************************************************************************")
        print("Configuration detected:")
        print("**************************************************************************")
        print("\nPlatform:")
        print(systemPlatform)
        print("Release:")
        print(systemRelease)

        return systemPlatform, systemRelease

    # Function: getAuthenticationData
    def getAuthenticationData(self):

        print("\n**************************************************************************")
        print("Authentication:")
        print("**************************************************************************\n")

        loopControlFileExists = 0

        while int(loopControlFileExists) == 0:
            try:
                # Get authentication data
                print("\nGetting authentication data ...\n")

                authenticationData = configparser.ConfigParser()
                authenticationData.read('../config/config.ini')
                authenticationData.sections()

                videoSource = authenticationData['Configuration']['video-source']
                imageWidth = authenticationData['Configuration']['image-width']
                imageHeight = authenticationData['Configuration']['image-height']
                trackerType = authenticationData['Configuration']['tracker-type']

                yarpSend = authenticationData['YARP']['yarp-send']
                yarpReceive = authenticationData['YARP']['yarp-receive']

                print("Video Source: " + str(videoSource))
                print("Image width: " + str(imageWidth))
                print("Image height: " + str(imageHeight))
                print("Tracker Type: " + str(trackerType))

                print("YARP Send: " + str(yarpSend))
                print("YARP Receive: " + str(yarpReceive))

                # Convert image from string to int
                imageWidth = int(imageWidth)
                imageHeight = int(imageHeight)

                # Exit loop
                loopControlFileExists = 1

            except:

                systemResponseMessage = "\n[ERROR] Sorry, config.ini not founded, waiting 4 seconds to the next check ...\n"
                self.systemResponse.text_color = "red"
                self.systemResponse.fail(systemResponseMessage)
                time.sleep(4)

        systemResponseMessage = "\n[INFO] Data obtained correctly.\n"
        self.systemResponse.text_color = "green"
        self.systemResponse.succeed(systemResponseMessage)

        return videoSource, imageWidth, imageHeight, trackerType, yarpSend, yarpReceive

    # Function: checkYARPInstalled
    def checkYARPInstalled(self):

        try:
            import yarp
            yarpInstalled = 1

        except:
            systemResponseMessage = "\n[ERROR] Sorry, YARP middleware not installed. Using not YARP mode.\n"
            self.systemResponse.text_color = "red"
            self.systemResponse.fail(systemResponseMessage)

            yarpInstalled = 0

        return yarpInstalled

    # Function: getObjectTracker
    def getObjectTracker(self):

        objectTracker = cv2.MultiTracker_create()

        return objectTracker

    # Function: getTracker
    def getTracker(self, trackerType):

        if trackerType == self.objectTrackerTypes[0]:
            tracker = cv2.TrackerBoosting_create()

        elif trackerType == self.objectTrackerTypes[1]:
            tracker = cv2.TrackerMIL_create()

        elif trackerType == self.objectTrackerTypes[2]:
            tracker = cv2.TrackerKCF_create()

        elif trackerType == self.objectTrackerTypes[3]:
            tracker = cv2.TrackerTLD_create()

        elif trackerType == self.objectTrackerTypes[4]:
            tracker = cv2.TrackerMedianFlow_create()

        elif trackerType == self.objectTrackerTypes[5]:
            tracker = cv2.TrackerGOTURN_create()

        elif trackerType == self.objectTrackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()

        elif trackerType == self.objectTrackerTypes[7]:
            tracker = cv2.TrackerCSRT_create()

        else:
            tracker = cv2.TrackerCSRT_create()

        return tracker

    # Function: systemInfo
    def systemInfo(self):

        print("\n**************************************************************************")
        print("User controller:")
        print("**************************************************************************\n")
        print("1. Select region of interest with mouse.")
        print("2. Press enter to save region of interest to be tracked.")
        print("3. Press q to ends region selection or press c to continue selecting more regions.")
        print("4. Press u with program is working to update or re-select region of interest.")

    # Function: initializeCaptureDevices
    def initializaCaptureDevices(self, videoSource):

        self.systemResponse.text = "Initializing capture device ..."
        self.systemResponse.text_color = "blue"
        self.systemResponse.start()

        # If read from local webcam
        if str(videoSource) == "0":
            captureDevice = cv2.VideoCapture(0)

        # If video file or IP camera
        else:
            captureDevice = cv2.VideoCapture(str(videoSource))

        # Variable to to prevent dark frame at staring webcam
        loopControlGetFirstFrame = 0

        while int(loopControlGetFirstFrame) < 5:
            success, dataToSolve = captureDevice.read()

            # Increase loopControlGetFirstFrame
            loopControlGetFirstFrame = loopControlGetFirstFrame + 1

        self.systemResponse.stop()

        return captureDevice

    # Function: getDataToSolve
    def getDataToSolve(self, yarpReceive, inputImagePort, imageWidth, imageHeight):

        # Receive from selected source
        if int(yarpReceive) == 1:
            dataToSolve = inputImagePort.receive()

        # If not YARP mode
        else:
            success, dataToSolve = inputImagePort.read()

        # Resize data to solved
        dataToSolve = cv2.resize(dataToSolve, (imageWidth, imageHeight))

        return dataToSolve

    # Function: getTargets
    def getTargets(self, dataToSolve):

        # Build boxes and colors arrays
        boxes = []
        colors = []

        loopControlTargetSelection = 0

        while int(loopControlTargetSelection) == 0:

            # Call to interactive GUI selectROI to select the target box
            box = cv2.selectROI('[PROCESSED] multipleObjectTracker2D', dataToSolve)

            # Add region of interest to boxes
            boxes.append(box)

            # Select random color to tracker object
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))

            systemResponseMessage = "\n[INFO] Target selected correctly.\n"
            self.systemResponse.text_color = "blue"
            self.systemResponse.info(systemResponseMessage)

            systemResponseMessage = "\n[INFO] Enter q to ends selection. Enter c to select an additional target.\n"
            self.systemResponse.text_color = "red"
            self.systemResponse.fail(systemResponseMessage)

            # If q is pressed exit selection
            k = cv2.waitKey(0) & 0xFF

            if (k == 113):
                loopControlTargetSelection = 1

                systemResponseMessage = "\n[INFO] Target selection done correctly.\n"
                self.systemResponse.text_color = "green"
                self.systemResponse.succeed(systemResponseMessage)

        return boxes, colors

    # Function: addTargets
    def addTargets(self, objectTracker, trackerType, dataToSolve, boxes):

        for box in boxes:
            objectTracker.add(self.getTracker(trackerType), dataToSolve, box)

        return objectTracker

    # Function: drawBoxes
    def drawBoxes(self, boxes, colors, dataToSolve, yarpSend, outputDataPort):

        # Draw box and name in data to solve frame for each target
        for colorIndex, box in enumerate(boxes):

            # Prepare point P1: Up-Left box point
            p1 = (int(box[0]), int(box[1]))

            # Prepare point P2: Down-Right box point, P1 + horizontal distance and P1 + vertical distance
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))

            # Draw rectangle in target with random color
            cv2.rectangle(dataToSolve, p1, p2, colors[colorIndex], 2, 1)

            # Prepare target ID
            targetID = "TARGET: " + str(int(colorIndex + 1))

            # Draw ID on target box
            cv2.putText(dataToSolve, targetID, (int(box[0]), int(box[1] + box[3]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[colorIndex], 2)

            # Get coordinates
            dataSolvedResults = str(targetID) + self.getCoordinates(box)

            systemResponseMessage = "\n[INFO] Results: " + str(dataSolvedResults) + ".\n"
            self.systemResponse.text_color = "green"
            self.systemResponse.succeed(systemResponseMessage)

            if int(yarpSend) == 1 and str(outputDataPort) != "null":

                # Send output
                outputDataPort.send(dataSolvedResults)

        return dataToSolve

    # Function: getCoordinates
    def getCoordinates(self, box):

        # Get centroid coordinates X and Y
        x = int(box[0]) + int(box[2] / 2)
        y = int(box[1]) + int(box[3] / 2)

        coordinatesXY = " X: " + str(x) + ", Y: " + str(y)

        return coordinatesXY

    # Function: processRequest
    def processRequests(self, trackerType, imageWidth, imageHeight, yarpSend, yarpReceive, outputImagePort, outputDataPort, inputImagePort):

        # Variable to control check targets
        checkTargets = 0

        # Variable to control loopProcessRequests
        loopProcessRequests = 0

        while int(loopProcessRequests) == 0:

            # Waiting to input data request
            print("**************************************************************************")
            print("Waiting for input data request:")
            print("**************************************************************************")

            systemResponseMessage = "\n[INFO] Waiting for input data request at " + str(datetime.datetime.now()) + " ...\n"
            self.systemResponse.text_color = "yellow"
            self.systemResponse.warn(systemResponseMessage)

            print("\n**************************************************************************")
            print("Processing:")
            print("**************************************************************************\n")

            try:
                dataToSolve = self.getDataToSolve(yarpReceive, inputImagePort, imageWidth, imageHeight)

                if int(checkTargets) == 0:

                    # Set targets and add to tracking system
                    boxes, colors = self.getTargets(dataToSolve)
                    trackerEngine = self.addTargets(self.getObjectTracker(), trackerType, dataToSolve, boxes)
                    checkTargets = 1

                    # First frame send base to solve frame
                    dataSolved = dataToSolve

                else:
                    # Update tracker engine with new boxes position
                    success, boxes = trackerEngine.update(dataToSolve)

                    # Draw boxes
                    dataSolved = self.drawBoxes(boxes, colors, dataToSolve, yarpSend, outputDataPort)

                # Display data solved tracking
                cv2.imshow('[PROCESSED] multipleObjectTracker2D', dataSolved)

                # If key u is pressed re-select targets
                if cv2.waitKey(33) == ord('u'):
                    checkTargets = 0

                if int(yarpSend) == 1 and str(outputImagePort) != "null":

                    # Send output
                    outputImagePort.send(dataSolved)

            except:
                systemResponseMessage = "\n[ERROR] Sorry, i couldn´t resolve your request.\n"
                self.systemResponse.text_color = "red"
                self.systemResponse.fail(systemResponseMessage)


class YarpDataPort:

    # Function: Constructor
    def __init__(self, portName):

        # Build Halo spinner
        self.systemResponse = Halo(spinner='dots')

        # Build port and bottle
        self.yarpPort = yarp.Port()
        self.yarpBottle = yarp.Bottle()

        systemResponseMessage = "\n[INFO] Opening Yarp data port " + str(portName) + " ...\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        # Open Yarp port
        self.portName = portName
        self.yarpPort.open(self.portName)

    # Function: receive
    def receive(self):

        self.yarpPort.read(self.yarpBottle)
        dataReceived = self.yarpBottle.toString()
        dataReceived = dataReceived.replace('"', '')

        systemResponseMessage = "\n[RECEIVED] Data received: " + str(dataReceived) + " at " + str(datetime.datetime.now()) + ".\n"
        self.systemResponse.text_color = "blue"
        self.systemResponse.info(systemResponseMessage)

        return dataReceived

    # Function: send
    def send(self, dataToSend):

        self.yarpBottle.clear()
        self.yarpBottle.addString(str(dataToSend))
        self.yarpPort.write(self.yarpBottle)

    # Function: close
    def close(self):

        systemResponseMessage = "\n[INFO] " + str(self.portName) + " port closed correctly.\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        self.yarpPort.close()


class YarpImagePort:

    # Function: Constructor
    def __init__(self, portName, imageWidth, imageHeight):

        # Build Halo spinner
        self.systemResponse = Halo(spinner='dots')

        # If input image port required
        if "/img:i" in str(portName):
            self.yarpPort = yarp.BufferedPortImageRgb()

        # If output image port required
        else:
            self.yarpPort = yarp.Port()

        systemResponseMessage = "\n[INFO] Opening Yarp image port " + str(portName) + " ...\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        # Open Yarp port
        self.portName = portName
        self.yarpPort.open(self.portName)

        # Build image buffer
        self.imageWidth = int(imageWidth)
        self.imageHeight = int(imageHeight)
        self.bufferImage = yarp.ImageRgb()
        self.bufferImage.resize(self.imageWidth, self.imageHeight)
        self.bufferArray = np.ones((self.imageHeight, self.imageWidth, 3), np.uint8)
        self.bufferImage.setExternal(self.bufferArray.data, self.bufferArray.shape[1], self.bufferArray.shape[0])

    # Function: receive
    def receive(self):

        image = self.yarpPort.read()
        self.bufferImage.copy(image)
        assert self.bufferArray.__array_interface__['data'][0] == self.bufferImage.getRawImage().__int__()
        image = self.bufferArray[:, :, ::-1]

        return self.bufferArray

    # Function: send
    def send(self, dataToSend):

        self.bufferArray[:,:] = dataToSend
        self.yarpPort.write(self.bufferImage)

    # Function: close
    def close(self):

        systemResponseMessage = "\n[INFO] " + str(self.portName) + " port closed correctly.\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        self.yarpPort.close()


# Function: main
def main():

    print("**************************************************************************")
    print("**************************************************************************")
    print("                 Program: Multiple Object Tracker 2D                      ")
    print("                     Author: David Velasco Garcia                         ")
    print("                             @davidvelascogarcia                          ")
    print("**************************************************************************")
    print("**************************************************************************")

    print("\nLoading Multiple Object Tracker 2D engine ...\n")

    # Build multipleObjectTracker2D object
    multipleObjectTracker2D = MultipleObjectTracker2D()

    # Get system platform
    systemPlatform, systemRelease = multipleObjectTracker2D.getSystemPlatform()

    # Get authentication data
    videoSource, imageWidth, imageHeight, trackerType, yarpSend, yarpReceive = multipleObjectTracker2D.getAuthenticationData()

    # Check YARP installed if YARP is required
    if int(yarpSend) == 1 or int(yarpReceive) == 1:

        yarpInstalled = multipleObjectTracker2D.checkYARPInstalled()

        if int(yarpInstalled) == 1:

            # Init Yarp network
            yarp.Network.init()

            # Create Yarp ports
            if int(yarpSend) == 1:
                outputImagePort = YarpImagePort("/multipleObjectTracker2D/img:o", imageWidth, imageHeight)
                outputDataPort = YarpDataPort("/multipleObjectTracker2D/data:o")

            else:
                outputImagePort = "null"
                outputDataPort = "null"

            if int(yarpReceive) == 1:
                inputImagePort = YarpImagePort("/multipleObjectTracker2D/img:i", imageWidth, imageHeight)

            else:
                inputImagePort = multipleObjectTracker2D.initializaCaptureDevices(videoSource)

        else:
            outputImagePort = "null"
            outputDataPort = "null"
            inputImagePort = multipleObjectTracker2D.initializaCaptureDevices(videoSource)

    else:
        outputImagePort = "null"
        outputDataPort = "null"
        inputImagePort = multipleObjectTracker2D.initializaCaptureDevices(videoSource)

    # Show system info
    multipleObjectTracker2D.systemInfo()

    # Process input requests
    multipleObjectTracker2D.processRequests(trackerType, imageWidth, imageHeight, yarpSend, yarpReceive, outputImagePort, outputDataPort, inputImagePort)

    # Close Yarp ports
    if int(yarpSend) == 1 and int(yarpInstalled) == 1:
        outputImagePort.close()
        outputDataPort.close()

    if int(yarpReceive) == 1 and int(yarpInstalled) == 1:
        inputImagePort.close()

    print("**************************************************************************")
    print("Program finished")
    print("**************************************************************************")
    print("\nmultipleObjectTracker2D program finished correctly.\n")


if __name__ == "__main__":

    # Call main function
    main()