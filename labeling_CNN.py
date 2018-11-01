# -*- coding: utf-8 -*-

"""
	labeling_CNN.py
	~~~~~~~~~~~~~~~~

	Determine the label of battery from the video. Use CNN.

	Dependency::
		python : 3.6.*  
		Package : Please look requirements.txt 

	Usage::
	>>> python labeling_CNN.py --path ./videos/00000.mov -M ./models/model.h5 --debug -N 3
"""

import argparse
import os
import cv2
from PIL import Image
from keras.models import load_model
import numpy as np

import split_video

# Constant
LABEL = ["ALKALINE", "LIION", "NIMH", "NICD"]
UNKNOWN = "UNKNOWN"
IMAGE_SIZE = 224
CORRECT_PROB = 0.95


def main(args):
	""" Get label of battery by CNN.

		:return: label of battery :type: str
	"""
	if not os.path.exists(args.path):
		print("Path to the video does not exist : " + args.path)
		exit(1)
	elif not os.path.exists(args.model):
		print("The model  does not excist : " + args.model)
		exit(1)

	images = get_image_from_video(args.path, args.number)
	label = get_label_from_images(images, load_model(args.model), args.debug)
	print(label)


def  get_image_from_video(path, number):
	""" Split video into frames and return frames.

		:param path: path to the video :type: str
		:param number: the number of images to determine the label :type: int
		:return images: list of image from video :type: [`Image` object]
	"""
	images = []

	video = cv2.VideoCapture(path)
	frame_number = video.get(cv2.CAP_PROP_FRAME_COUNT)
	index = [frame_number // number * i for i in range(number)]
	
	for i in index:
		video.set(cv2.CAP_PROP_POS_FRAMES, i)
		flag, frame = video.read()
		if flag:
			images.append(split_video.crop_max_square(Image.fromarray(frame)))
		else:
			break;

	video.release()

	return images



def convert_data(imgs):
	""" Processing data from image to CNN.

		:param imgs: :type: [`Image` object]
		:return X: procesed images :type: [float]
	"""
	X = []
	for image in imgs:
		image = image.convert("RGB")
		image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
		data = np.asarray(image)
		X.append(data)
		
	X = np.array(X, dtype=np.float32)
	X = X / 255.0

	return X

def get_label(results):
	""" Return labels that have best probability.
		It should be LABEL or UNKNOWN.

		:param results: list of probabilities :type: [[float]]
		:return ans_label: procesed images :type: [str]
	"""
	ans_label = []
	for result in results:
		ans = 0
		ans_pos = 0
		for i, arg in enumerate(result):
			if arg > ans_pos:
				ans = i
				ans_pos = arg
		
			label = LABEL[ans]
			if ans_pos < CORRECT_PROB:
				label = UNKNOWN

		ans_label.append(label)
	
	return ans_label

def estimate_label(labels):
	""" Guess the label from multiple labels.

		:param labels: list of label :type: [[str]]
		:return ret_l: final label :type: str
	"""

	if UNKNOWN in labels:
		return UNKNOWN
	elif len(set(labels)) == 1:
		return labels[0]

	return UNKNOWN
	



def  get_label_from_images(images, model, debug=False):
	""" Predict the type of battery.
		Model should be '*.h5'.

		:param images: :type: [`Image` object]
		:param model: model(keras)
		:return: the label of battery :type: str
	"""
	processed = convert_data(images)

	result =  model.predict(processed, verbose=int(debug))
	labels = get_label(result)
	if debug:
		print(labels)
	
	return estimate_label(labels)



if __name__ == "__main__":
	# Make parser.
	parser = argparse.ArgumentParser(
				prog='labeling_CNN.py', 
				usage='Determine the type of battery from the video by CNN.', 
				description='description...',
				epilog='end',
				add_help=True,
				)
	parser.add_argument('-P', '--path', help='Path to the video to determine.', required=True)
	parser.add_argument('-M', '--model', help='Choose model. Default is "./models/model.h5".', required=False,
							default='./models/model.h5')
	parser.add_argument('-N', '--number', help='The number of images to determine the label. Get this number of frames from the video. Default is 3.', 
							required=False, type=int, default=3)
	parser.add_argument('--debug', help='Debug mode.', action='store_true', required=False, default=False)

	# parse thearguments.
	args = parser.parse_args()
	main(args)

