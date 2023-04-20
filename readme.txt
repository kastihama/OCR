#How to use Project
apt install python3-venv
python3 -m venv venv
source venv/bin/activate
===  INstalling from requirnment.txt
pip install -r requirements.txt


# Purpose:
Improve Keras-OCR to read detected texts in a more 'human' way, 
meaning from left to right and top to bottom. 


# Install all necessary libraries (Note: I used a conda environment.)
pip install -r requirements.txt

Reference From
Full Explanation: 
extract-text-from-image-left-to-right-and-top-to-bottom-with-keras-ocr-b56f098a6efe


Sample Runs:
# Raw detection (order does not matter)
python detect.py --image images/wanderer.png --thresh 10 --order no

# Tighten threshold
python detect.py --image images/wanderer.png --thresh 10 --order yes
	
# Average threshold
python detect.py --image images/wanderer.png --thresh 15 --order yes 

# Loosen threshold
python detect.py --image images/wanderer.png --thresh 20 --order yes

get_distance: Description of it's function
This Python code defines a function named get_distance that takes in one parameter predictions. This function is intended to receive a list of lists, where each list contains a detected text in an image and its corresponding bounding box coordinates.

The function then loops through each of the bounding boxes, calculates the center point of each bounding box, and uses the Pythagorean Theorem to calculate the distance from the center point to the origin point (0, 0).

It also calculates the distance between the center point and the y-axis, or the distance between the center point and the origin point on the y-axis.

Finally, the function stores all the calculated results for each bounding box in a list of dictionaries and returns the list.

The output of the function get_distance will be a list of dictionaries, where each dictionary contains the following keys:

'text': The detected text in the image
'center_x': The center of the bounding box on the x-axis
'center_y': The center of the bounding box on the y-axis
'distance_from_origin': The distance from the center point to the origin point (0,0)
'distance_y': The distance between the center point and the y-axis

