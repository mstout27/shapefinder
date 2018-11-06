#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

int main( int argc, char** argv ){

  //Check if too many command line args
  if(argc > 7){
    cout << "Too many arguments have been entered. Please try again." << endl;
    cout << "Arguments should be in form: input.PPM -c color -s shape -o output" << endl;
    cout << "Flags default to color = white, shape = rectangle, output = output.PPM" << endl;
    return -1;
  }

  //Check if not enough command line args
  if(argc < 2){
    cout << "Too few arguments have been entered. Please try again." << endl;
    cout << "Arguments should be in form: input.PPM -c color -s shape -o output" << endl;
    cout << "At minimum the input file must be specified." << endl;
    return -1;
  }

  // First input should be the input name
  // Set up defaults
  String imageName = argv[1];
  String colorIn = "white";
  String shape = "rectangle";
  String output = "output.PNG";

  // Loop through entered args to find flags and choices
  for(int j = 1; j < argc; j++){
    if (j+1 != argc){
      if (String(argv[j]) == "-c" || (String(argv[j]) == "--color") {
        colorIn = argv[j+1];
      }
      else if (String(argv[j]) == "-s" || (String(argv[j]) == "--shape") {
        shape = argv[j+1];
      }
      else if (String(argv[j]) == "-o") {
        output = argv[j+1];
      }
    }
  }

  // Check color input and set up choices
  Scalar color = Scalar(0, 0, 0);
  if(colorIn == "white"){
    color = Scalar(255, 255, 255);
  }
  else if(colorIn == "black"){
    color = Scalar(0, 0, 0);
  }
  else if(colorIn == "red"){
    color = Scalar(255, 0, 0);
    cout << "red" << endl;
  }
  else if(colorIn == "blue"){
    color = scalar(0, 0, 255)
  }
  else if(colorIn == "green"){
    color = scalar(0, 255, 0)
  }
  else if(colorIn == "magenta"){
    color = scalar(255, 0, 255)
  }
  else if(colorIn == "yellow"){
    color = scalar(255, 255, 0)
  }
  else if(colorIn == "cyan"){
    color = scalar(0, 255, 255)
  }
  else{
    cout << "Color flag not entered correctly. Setting to default of white." << endl;
  }

  // Check sides input and set up choices
  int sides;
  if(shape == "triangle"){
    sides = 3;
  }
  else if(shape == "rectangle"){
    sides = 4;
  }
  else if(shape == "pentagon"){
    sides = 5;
  }
  else if(shape == "hexagon"){
    sides = 6;
  }
  else{
    sides = 4;
    cout << "Shape flag not entered correctly. Setting to default of rectangle." << endl;
  }

  Mat image = imread( imageName, IMREAD_COLOR ); // Read the file

  // Check for invalid input
  if( image.empty() ){
      cout << "Could not open or find the image" << endl ;
      cout << "Please make sure the first argument is the filename." << endl;
      return -1;
  }

  Mat gray;
  Mat blur;
  cvtColor(image, gray, CV_BGR2GRAY); // Convert to grayscale for detection
  GaussianBlur(gray, blur, Size(3,3), 0, 0); // Blur the image to reduce noise

  // Detect edges in image
  Mat edges;
  Canny(gray, edges, 10, 75);

  // Kernal for closing edges
  Mat closed;
  Mat kernel = getStructuringElement(MORPH_RECT, Size(4, 4));
  morphologyEx(edges, closed, MORPH_CLOSE, kernel);

  // Retrieve contours from fixed image
  vector<vector<Point> > contours;
  vector<Vec4i> hierarchy;

  findContours(closed, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);

  // Total shapes found
  int total = 0;

  // Loop over contours
  for(int i = 0; i < contours.size(); i ++){

    // Approximate contour
    double peri = arcLength(contours[i], true);
    vector<Point> approx;
    approxPolyDP(contours[i], approx, 0.02 * peri, true);

    // Use contour & user input to determine shape to detect
    if(approx.size() == 3 & sides == 3){
      drawContours(image, contours, i, color, 4);
      total += 1;
    }
    else if(approx.size() == 4 & sides == 4){
      drawContours(image, contours, i, color, 4);
      total += 1;
    }
    else if(approx.size() == 5 & sides == 5){
      drawContours(image, contours, i, color, 4);
      total += 1;
    }
    else if(approx.size() == 6 & sides == 6){
      drawContours(image, contours, i, color, 4);
      total += 1;
    }
  }

  cout << "Found " << total << " " << shape << endl;
  namedWindow("Output", WINDOW_AUTOSIZE); // Create a window for display.
  imshow("Output", image);                // Show our image inside it.
  waitKey(0); // Wait for a keystroke in the window
  imwrite(output, image);
  return 0;
}
