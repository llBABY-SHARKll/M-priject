
import cv2
import numpy as np
from PIL import Image
import csv
import os

# Functions

def capture_and_save_image(filename="all.jpg"):
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
      print("Error opening camera!")
      return False
  ret, frame = cap.read()
  if not ret:
      print("Failed to capture frame!")
      cap.release()
      return False
  cv2.imwrite(filename, frame)
  cap.release()
  print(f"Image captured and saved as {filename}")

def process_image(image, hsv_filter, edge_detection=False):
  if len(image.shape) == 2:  # Grayscale image
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  elif image.shape[2] != 3:  # Non-BGR color format
      image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

  # Color filtering based on HSV values
  lower_hsv = np.array(hsv_filter[0])
  upper_hsv = np.array(hsv_filter[1])
  hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert to HSV color space
  mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)  # Create mask for the HSV range
  image = cv2.bitwise_and(image, image, mask=mask)  # Apply mask

  # Edge detection (using Sobel filter)
  if edge_detection:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
      sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=5)  # Sobel filter for horizontal edges
      sobely = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=5)  # Sobel filter for vertical edges
      edges = cv2.bitwise_or(sobelx, sobely)  # Combine horizontal and vertical edges
      image = edges  # Replace original image with edge detection result

  return image

def save_processed_image(image, filename, hsv_filter, edge_detection=False):
  processed_image = process_image(image.copy(), hsv_filter, edge_detection)  # Process a copy
  cv2.imwrite(filename, processed_image)  # Save the processed image
  print(f"Image processed and saved as: {filename}")

def convert_to_maze_binary(image):
  if len(image.shape) == 3:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
      gray_img = image
  ret, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)
  inverted_img = cv2.bitwise_not(binary_img)
  return inverted_img

def convert_to_binary(image):
  if len(image.shape) == 3:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
      gray_img = image
  ret, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)
  return binary_img

def find_object(image):
  # Find contours
  contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Check if any contours are found
  if not contours:
      return False, None, None, None

  # Assuming the largest contour corresponds to the object
  largest_contour = max(contours, key=cv2.contourArea)

  # Find bounding box, center, and radius (approximated as a circle)
  x, y, w, h = cv2.boundingRect(largest_contour)
  center = (int(x + w / 2), int(y + h / 2))
  radius = max(w // 2, h // 2)  # Approximate radius based on bounding box dimensions

  return True, (x, y, w, h), center, radius

def write_array_to_file(array, filename="loc.txt"):
  # Ensure data is a list or NumPy array
  if not isinstance(array, (list, np.ndarray)):
      raise TypeError("Input data must be a list or NumPy array.")
  # Open the file in write mode with truncation (deletes existing content)
  with open(filename, "w") as f:
    # Write each element of the array on a separate line
    for item in array:
      f.write(str(item) + "\n")  # Convert each item to string before writing
  print(f"Array successfully written to {filename}.")

def resizing(main,hpercentage):
    main = cv2.imread(main)
    height = main.shape[ 0] * hpercentage / 100
    width = main.shape[ 1] * hpercentage / 100 
    dim = dim = (int(width), int(height))
    final_im = cv2.resize(main, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("nature.jpg", final_im)
    return "yes"

def convert_to_binary01(image_path):
  img = cv2.imread(image_path)
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  threshold = 220
  binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY_INV)[1]
  # Convert the binary image to a NumPy array
  binary_array = np.asmatrix(binary_img)
  # Invert the array so white is 0 and others are 1
  binary_array = np.where(binary_array == 255, 0, 1)
  return binary_array

def modify_array(array, center, height, width, value_to_replace_with):
    x_center, y_center = center
    half_height = height // 2
    half_width = width // 2

    
    y_start = max(0, y_center - half_height)
    y_end = min(len(array), y_center + half_height + 1)  
    x_start = max(0, x_center - half_width)
    x_end = min(len(array[0]), x_center + half_width + 1)  
    print(x_start,x_end,y_start,y_end)
  
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            array[y][x] = int(value_to_replace_with)

    return array

def read_bw_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read image as grayscale

    # Apply a threshold to convert grayscale to binary (0 or 255)
    _, bw_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # Normalize to 0 or 1
    bw_array = 1 - bw_image // 255

    return bw_array

def create_colored_image(array):
    color_map = {
        0: (0, 0, 0),   # Black
        1: (255, 0, 0), # Red
        2: (0, 0, 255), # Blue
        3: (0, 255, 0)  # Green
    }

    h, w = array.shape
    image_data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            image_data[i, j] = color_map[array[i, j]]

    return Image.fromarray(image_data)

# Main

def main():

  #const 
  Robot_H = 28.1 #CM 
  Robot_W = 30.6 #CM

  #picname = "all.jpg"  #main picture name
  picname = "all2.png"
  #capture_and_save_image(picname) #input using camera
  image = cv2.imread(picname) # read the image capture
  height, width = image.shape[:2] # maze dimensions

  # colour filter values

  hsv_filter_green = ((35, 50, 50), (75, 255, 255))  # Green
  hsv_filter_red_dark = ((0, 100, 100), (10, 255, 255)) # Red (for darker shades)
  hsv_filter_red_bright = ((170, 100, 100), (180, 255, 255)) # Red (for brighter shades)
  hsv_filter_blue = ((100, 100, 100), (140, 255, 255))  # Blue

  # colour filterations

  save_processed_image(image.copy(), "goal.png", hsv_filter_green)
  save_processed_image(image.copy(), "robot.png", hsv_filter_blue)
  save_processed_image(image.copy(), "map.png", hsv_filter_red_dark)

  #convert to binary

  binary_map = cv2.imwrite("binary.jpg",convert_to_maze_binary(cv2.imread("map.png")))
  binary_robot = cv2.imwrite("robotb.jpg",convert_to_binary(cv2.imread("robot.png")))
  binary_goal = cv2.imwrite("goalb.jpg",convert_to_binary(cv2.imread("goal.png")))

  # Convert the image to a NumPy array

  robotloc = np.array(Image.open("robotb.jpg"))
  goalloc = np.array(Image.open("goalb.jpg"))

  # Robot and Goal Location and Radius

  roboty, rbounding_box, rcenter, rradius = find_object(robotloc)
  goaly, gbounding_box, gcenter, gradius = find_object(goalloc)

  # Debugging

  if roboty:
    print("robot")
    print(f"Bounding box: {rbounding_box}")
    print(f"Center: {rcenter}")
    print(f"Radius: {rradius}")
  if goaly:
    print("goal")
    print(f"Bounding box: {gbounding_box}")
    print(f"Center: {gcenter}")
    print(f"Radius: {gradius}")

  # Writing the data needed 

  image_path = 'binary.jpg' 
  bw_array = read_bw_image(image_path)
  print(bw_array)
  
  rheight = int(1.2 * rradius)
  rwidth = rheight
  gheight = int(1.2*rheight)
  gwidth = gheight

  rrelation = float(Robot_W / rheight)

  locs = [ rrelation , rheight , rcenter[0],rcenter[1], gcenter[0],gcenter[1],height,width]
  write_array_to_file(locs)
  
  print(rheight,rwidth,rcenter,gheight,gwidth,gcenter)

  bw_array= modify_array(bw_array,rcenter,rheight,rwidth,value_to_replace_with=2)
  bw_array= modify_array(bw_array,gcenter,gheight,gwidth,value_to_replace_with=3)
  
  #colored_image = create_colored_image(bw_array)
  #colored_image.show()  # Display the image

  output_file = 'site.csv'

  # Write the array to the CSV file
  with open(output_file, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(bw_array)

  print(f"Array written to {output_file}")
  
if __name__ == '__main__':
    main()
