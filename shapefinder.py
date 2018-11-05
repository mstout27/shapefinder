# import the necessary packages
import numpy as np
import cv2
import argparse

# create argument parser and flags
parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("-c","--color", help = "specify shape color", default = "0x00ff00")
parser.add_argument("-s","--shape", help = "choose shape", default = "rectangle")
parser.add_argument("-o", help = "save to file")
args = parser.parse_args()

red = 0
green = 255
blue = 0
# determine correct output based on flags
if args.color[0:2] == "0x":
    red = args.color[2:4]
    red = int(red,16)
    green = args.color[4:6]
    green = int(green,16)
    blue = args.color[6:8]
    blue = int(blue,16)
if args.color:
    if args.color == "red":
        red = 255
        green = 0
        blue = 0
    if args.color == "blue":
        red = 0
        green = 0
        blue = 255
    if args.color == "green":
        red = 0
        green = 255
        blue = 0
    if args.color == "black":
        red = 0
        green = 0
        blue = 0

sides = 0
if args.shape:
    if args.shape == "triangle":
        sides = 3
    elif args.shape == "rectangle":
        sides = 4
    elif args.shape == "pentagon":
        sides = 5
    elif args.shape == "hexagon":
        sides = 6 
    print("Shape will be: {}".format(args.shape))

# load the image, convert it to grayscale, and blur it
image = cv2.imread("lee.PPM")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)

cv2.imshow("Gray",gray)
cv2.waitKey(0)

# detect edges in the image
edged = cv2.Canny(gray, 10, 75)

cv2.imshow("Edged", edged)
cv2.waitKey(0)

# construct and apply a closing kernel to 'close' gaps between 'white'
# pixels
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Closed", closed)
cv2.waitKey(0)

# find contours (i.e. the 'outlines') in the image and initialize the
# total number of books found
_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

# loop over the contours
for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if the approximated contour has four points, then rectangle
        if len(approx) == 3 and sides == 3:
            cv2.drawContours(image, [approx], -1, (red, green, blue), 4)
            total +=1
        elif len(approx) == 4 and sides == 4:
            cv2.drawContours(image, [approx], -1, (red, green, blue), 4)
            total += 1
        elif len(approx) == 5 and sides == 5:
            cv2.drawContours(image, [approx], -1, (red, green, blue), 4)
            total += 1
        elif len(approx) == 6 and sides == 6:        
            cv2.drawContours(image, [approx], -1, (red, green, blue), 4)
            total += 1



       

# display the output
print ("I found {0} books in that image".format(total))
cv2.imshow("Output", image)

# if -o flag, save output to file
if args.o:
    print("Saving to output file: {}".format(args.o))
    imwrite(args.o,image)  

cv2.waitKey(0)
