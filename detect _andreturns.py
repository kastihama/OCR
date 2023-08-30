import argparse
import math, keras_ocr
import pandas as pd

generateFileName="identifiedText.txt"
generateFileLocation = "generatedFile/"+generateFileName

parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, 
					help='path to image')
parser.add_argument('--thresh', type=int, default=15, 
					help='threshold to distinguish new rows')
parser.add_argument('--order', type=str, default='yes', 
					help='enter y or yes to order detections in a human readable way')
args = parser.parse_args()

def detect_w_kerasFromImage(image_path):
	"""Function returns detected text from image"""

	# keras_ocr.pipeline.Pipeline() is a class in the keras-ocr library that allows you
	# to create an OCR pipeline using Keras. OCR stands for Optical Character Recognition,
	# and it refers to the technology used to recognize text from images.
	# Initialize pipeline
	pipeline = keras_ocr.pipeline.Pipeline()

	# Read in image path
	read_image = keras_ocr.tools.read(image_path)

	# prediction_groups is a list of (word, box) tuples
	prediction_groups = pipeline.recognize([read_image]) 

	return prediction_groups[0]


def get_distance(predictions):
	"""
	Function returns list of dictionaries with (key,value):
		* text : detected text in image
		* center_x : center of bounding box (x)
		* center_y : center of bounding box (y)
		* distance_from_origin : hypotenuse
		* distance_y : distance between y and origin (0,0)
	...for each bounding box (detections). 
	"""

	# Point of origin
	x0, y0 = 0, 0

	# Generate dictionary
	detections = []
	for group in predictions:
		
		# Get center point of bounding box
		top_left_x, top_left_y = group[1][0]
		bottom_right_x, bottom_right_y = group[1][1]
		center_x, center_y = (top_left_x + bottom_right_x)/2, (top_left_y + bottom_right_y)/2
	
		# Use the Pythagorean Theorem to solve for distance from origin
		distance_from_origin = math.dist([x0,y0], [center_x, center_y])

		# Calculate difference between y and origin to get unique rows
		distance_y = center_y - y0
		
		# Append all results
		detections.append({
							'text': group[0],
							'center_x': center_x,
							'center_y': center_y,
							'distance_from_origin': distance_from_origin,
							'distance_y': distance_y
						})
	
	return detections


def distinguish_rows(lst, thresh=15):
	"""Function to help distinguish unique rows"""
	sublists = []
	for i in range(0, len(lst)-1):
		if (lst[i+1]['distance_y'] - lst[i]['distance_y'] <= thresh):
			if lst[i] not in sublists:
				sublists.append(lst[i])
			sublists.append(lst[i+1])
		else:
			yield sublists
			sublists = [lst[i+1]]
	yield sublists

def generateFile( text ):
  with open (generateFileLocation, 'w') as text_file:
    text_file.write(str(text))

def main(image_path, thresh, order='yes'):
	"""Function returns predictions from left to right & top to bottom"""
	predictions = detect_w_kerasFromImage(image_path)
	predictions = get_distance(predictions)
	predictions = list(distinguish_rows(predictions, thresh))
	
	# Remove all empty rows
	predictions = list(filter(lambda x:x!=[], predictions))

	# Order text detections in human readable format
	ordered_preds = []
	sub_ordered_preds=[]
	order_in_Array = []
	ylst = ['yes', 'y']
	string_Data =""
	for h,row in enumerate(predictions):
		if order in ylst: row = sorted(row, key=lambda x:x['distance_from_origin'])
		inner_array=[]
		for i, each in enumerate(row):
			inner_array.append(each['text'])
			ordered_preds.append(row)
		    
		if i == len(predictions) - 1:
			string_Data = string_Data + " ".join(inner_array)+'\n'
			sub_ordered_preds.append(" ".join(inner_array))
			order_in_Array.append(inner_array)
		else:
			string_Data = string_Data + " ".join(inner_array)+'\n'
			sub_ordered_preds.append(" ".join(inner_array))
			order_in_Array.append(inner_array)
	generateFile(string_Data)
	# print(string_Data)

	return ordered_preds
	# return ordered_preds

if __name__=='__main__':
	
	image = args.image
	thresh = args.thresh
	order = args.order
	
	print(f'Generating predictions for {image}...')
	predictions = main(image, thresh, order)
	print(predictions)
	generateFile(predictions)
	# print(predictions)



	
