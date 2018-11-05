# import the necessary packages
import numpy as np
import cv2
import argparse

# create argument parser and flags
parser = argparse.ArgumentParser()
parser.add_argument("image", help = "image to detect shapes")
parser.add_argument("-c","--color", help = "specify shape color", default = "0x00ff00")
parser.add_argument("-s","--shape", help = "choose shape", default = "rectangle")
parser.add_argument("-o", help = "save to file")
args = parser.parse_args()

red = 0
green = 255
blue = 0

# if -c flag, read hex color input
if args.color[0:2] == "0x":
    red = args.color[2:4]
    red = int(red,16)
    green = args.color[4:6]
    green = int(green,16)
    blue = args.color[6:8]
    blue = int(blue,16)
# if -s flag, read word color input
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
    if args.color == "yellow":
        red = 255
        green = 255
        blue = 0
    if args.color == "purple":
        red == 255
        green == 0
        blue == 255
    if args.color == "cyan":
        red == 0
        green == 255
        blue == 255
    if args.color == "white":
        red == 255
        green == 255
        blue == 255

# read shape input
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
gray = cv2.GaussianBlur(gray, (5, 5), 0)

#display blurred and grayed image
cv2.imshow("Gray",gray)
cv2.waitKey(0)

# detect edges in image
edges = cv2.Canny(gray, 10, 75)

#show edges image
cv2.imshow("Edges", edges)
cv2.waitKey(0)

# kernal for closing edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# show closed image
cv2.imshow("Closed", closed)
cv2.waitKey(0)

# retrieve contours from fixed image
_, cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

# loop over contours
for c in cnts:

    # approximate contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Use contour & user input to determine shape to detect
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

# Output
print ("Found {} {}s in image".format(total, args.shape))
cv2.imshow("Output", image)

# if -o flag, save output to file
if args.o:
    print("Saving to output file: {}".format(args.o))
    cv2.imwrite(args.o,image)  

cv2.waitKey(0)
