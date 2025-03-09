#importing the required libraries
from picamera2 import Picamera2, Preview
import time
import cv2
import pandas as pd
import pyttsx3

#defining image path
img_path = "/home/rapi/Desktop/colour_img/testcolour2.jpg"

#intitializing the camera 
picam2 = Picamera2()

#setting up the camera and taking the photo
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()
time.sleep(2)
picam2.capture_file(img_path)

# Initialize the text-to-speech engine and setting the settings
engine = pyttsx3. 1nit()
engine.setProperty( 'rate',150)
engine. setProperty ('voice', "english-us")

#reading the image with opencv
img = cv2.imread(img_path)

# declaring and formating global variables aka the r g and b values and the colour name and the base colour (are used later on)
R_value = G_value = B_value = 0
Colour = ""
base = ""

# Reading the csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Get the center coordinates of the image
height, width, _ = img.shape
center_x = width // 2
center_y = height // 2


# Get the color at the center pixel
B_value, G_value, R_value = img[center_y, center_x]

# Get the color name based on the RGB values by calculating the colour values closest to the the detect values 
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            Colour = csv.loc[i, "color_name"]
    return Colour

#getting the base shades using predefined colour shades 
def get_color_base(R, G, B):
  """
  This function identifies the color based on predefined ranges.
  """
  # Define color ranges based on RGB values
  colors = {
    "red": (B < 100 and G < 100 and R > 180),
    "orange": (B < 100 and G > 100 and R > 180),
    "yellow": (B < 100 and G > R and R > 100),
    "green": (B > G and G > R),
    "blue": (B > R and G > R),
    "purple": (R < G and B > G),
    "brown": (abs(R - G - B) < 100 and R > 100 and G > 100 and B > 100),
    "black": (R < 50 and G < 50 and B < 50),
    "white": (R > 200 and G > 200 and B > 200),
    "grey": (abs(R - G - B) < 100)
  }
  
  # Check for matching color based on ranges
  for color, condition in colors.items():
    if condition:
      return color
  
  # If no match found, return "unknown"
  return "unknown"

# Save the color name and RGB values in variables
Colour = get_color_name(R_value, G_value, B_value)

# Save the base colour in a variable
base = get_color_base(R_value, G_value, B_value)


#Display the color information
print("Color:", Colour)
print("base:", base)
print("R:", R_value)
print("G:", G_value)
print("B:", B_value)

# Convert color information to audio using text-to-speech
text_to_speak = f"The detected color is {Colour}.Its shade {base} R value is {R_value}, G value is {G_value}, and B value is {B_value}."
engine.say(text_to_speak)
engine.runAndWait()
