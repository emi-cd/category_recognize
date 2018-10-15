# -*- coding: utf-8 -*-

"""
	retraining.py
	~~~~~~~~~~~~~~~

	Retraining the model. Train data should be .jpg.

	Dependency::
		python : 3.6.*
		Package : Please look requirements.txt 

	Usage::
	>>> python retraining.py --model ./models/model.h5 --debug
"""

import argparse
import os
import glob
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

import split_video

# Constant
LABEL = ["ALKALINE", "LIION", "NIMH", "NICD"]
IMAGE_SIZE = 150


def main(args):
	""" Make new model.
		Origin model become old_model.h5 and new one become model.h5.
	"""
	if not os.path.exists(args.model):
		print('The model does not exist : ' + args.model)
		exit(1)
	elif not os.path.exists(args.train):
		print('Train data does not exist : ' + args.train)
		exit(1)


	model = load_model(args.model)
	path, file = os.path.split(args.model)
	model.save(path + '/old_' + file)

	if args.debug:
		print('Processing data...')

	X, Y = process_train_data(args.train)
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state = 24)

	if args.debug:
		print('Training with new batteries...')
	es_cb = EarlyStopping(monitor='val_loss', patience=2, mode='auto', restore_best_weights=True)
	history = model.fit(X_train, y_train, batch_size=32, epochs=50, callbacks=[es_cb], validation_data=(X_test, y_test), verbose=int(args.debug))

	model.save(args.model)

	maintain(args.train, args.number)

def process_train_data(path):
	""" Process data from directory for CNN training.


		:param path: path to the training data. There should be data for each LABEL. :type: str
		:return X: image data for CNN :type: [[[float]]] (data of image)
		:return Y: label data for CNN :type: [[int]] (label of battery)
	"""
	X = []
	Y = []
	for index, name in enumerate(LABEL):
		if not os.path.exists(path + '/' + name):
			print('Does not exist : ' + path + '/' + name)
			exit(1)

		files = glob.glob(path + '/' + name + '/*.jpg')
		for file in files:
			image = Image.open(file)
			image = image.convert("RGB")
			image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
			data = np.asarray(image)
			X.append(data)
			Y.append(index)
	
	X = np.array(X, dtype=np.float32)
	X = X / 255.0

	Y = np_utils.to_categorical(Y, len(LABEL))

	return X, Y

def maintain(train, number):
	for folder in glob.glob(train + '/*'):
		files = glob.glob(folder + '/*.jpg')
		if len(files) > number:
			for i in range(len(files) - number):
				os.remove(files[i])


if __name__ == "__main__":
	# Make parser.
	parser = argparse.ArgumentParser(
				prog='retraining.py', 
				usage='Retraining the model.', 
				description='description...',
				epilog='end',
				add_help=True,
				)
	parser.add_argument('-M', '--model', help='Choose model. Default is "./models/model.h5".', required=False,
							default='./Models/model.h5')
	parser.add_argument('-T', '--train', help='Path to the train data. Default is ./train_data', required=False, default='./train_data')
	parser.add_argument('-N', '--number', help='The number os training data. Default is 1000.', required=False, default=1000, type=int)
	parser.add_argument('--debug', help='Debug mode.', action='store_true', required=False, default=False)

	# parse thearguments.
	args = parser.parse_args()
	main(args)

