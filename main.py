# -*- coding: utf-8 -*-

"""
	main.py
	~~~~~~~~~~~~~~~~

	Main flow. Video format should be .mov.
	LABEL : Label the battery
	RETRAIN : Retrain the model and maintain the number of training data. 

	Dependency::
		python : 3.6.*  
		Package : Please look requirements.txt 

	Usage::
	>>> python main.py --mode LABEl 
	or
	>>> python main.py --mode RETRAIN
"""
import argparse
import glob
import os
from time import sleep
from keras.models import load_model
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

from split_video import video_2_frames
from labeling_CNN import get_image_from_video, get_label_from_images
from labeling_OCR import judge, add_to_training_data
from retraining import process_train_data, maintain

UNKNOWN = 'UNKNOWN'
LABEL = 'LABEL'
RETRAIN = 'RETRAIN'

# Make parser.
parser = argparse.ArgumentParser(
			prog='roop.py', 
			usage='Main flow.', 
			description='description...',
			epilog='end',
			add_help=True,
			)
parser.add_argument('--mode', help="Choose 'LABEL' or 'RETRAIN'." , required=True, choices=[LABEL, RETRAIN])
parser.add_argument('-I', '--input', help="Path to the input video directory. Default is './videos'.", required=False, default='./videos')
parser.add_argument('-T', '--train', help="Path to the train data directory. Default is './train_data'.", required=False, default='./train_data')
parser.add_argument('--model', help='Choose model. Default is "./models/model.h5".', required=False,
						default='./models/model.h5')
parser.add_argument('--debug', help='Debug mode.', action='store_true', required=False, default=False)

# parse thearguments.
args = parser.parse_args()

def main():
	""" Roop. ** WARNING ** It is infinite loop!!
		If there are no videos, it become stopping for 10 seconds.
	"""
	if args.mode == LABEL:
		while True:
			videos = glob.glob(args.input + '/*.mov')
			if len(videos) > 0:
				label(videos)
			else:
				sleep(10)
	elif args.mode == RETRAIN:
			model = load_model(args.model)
			path, file = os.path.split(args.model)
			model.save(path + '/old_' + file)

			X, Y = process_train_data(args.train)
			X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state = 24)

			es_cb = EarlyStopping(monitor='val_loss', patience=2, mode='auto', restore_best_weights=True)
			history = model.fit(X_train, y_train, batch_size=32, epochs=50, callbacks=[es_cb], validation_data=(X_test, y_test), verbose=int(args.debug))
			model.save(args.model)

			maintain(args.train, 600)


def label(videos):
	""" Take video. It keeps moving, as long as the video exists.
		Output to stdout is battery's ID and label.

		:param videos: Path to the video directory :type: str
	"""
	while len(videos) > 0:
		ID, _ = os.path.splitext(os.path.basename(videos[0]))

		# CNN
		images = get_image_from_video(videos[0], 3)
		label = get_label_from_images(images, args.model)

		# OCR
		if label == UNKNOWN:
			if args.debug:
				print('OCR : ', end='')
			imgs = video_2_frames(videos[0], 60)
			label = judge(imgs[::2], args.debug)
			add_to_training_data(label, imgs, args.train, videos[0])

		print(ID + ',' + label)


		os.remove(videos[0])
		videos = glob.glob(args.input + '/*.mov')


if __name__ == "__main__":
	main()
