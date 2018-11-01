# -*- coding: utf-8 -*-

"""
	larning_OCR.py
	~~~~~~~~~~~~~~~

	Determine the type of battery from the video by OCR.
	Use tesseract to recognize charactor.
	s
	1) Split the video into frames
	2) Label the battery  with OCR.
	3) Saving frames to the directory of their label

	Dependency::
		python : 3.6.*
		Package : Please look requirements.txt 

	Usage::
	 >>> python labeling_OCR.py --path './videos/00000.mov' --debug
"""
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import glob
import shutil, os, re, argparse

from split_video import video_2_frames


# Keyword
alk = ("ALKALINE", ["ALKALI", "ALK", "LR6", "LR03", "LR20", "1.5V", "1,5V"])
nicd = ("NICD", ["NI-CD", "NICD", "KR6", "KR03", "KR20"])
nimh = ("NIMH", ["NIMH", "MHNI", "NI-MH", "MH-NI", "HR14", "HR6", "HR03", "HR20"])
liion = ("LIION", ["LIION", "LI-ION", "LITHIUM", "3,7V", "3.7V"])
UNKNOWN = "UNKNOWN"

klst = [alk, nicd, nimh, liion]

def main(args):
	if args.debug:
		print('Now spliting the video...',flush=True)
	imgs = video_2_frames(args.path, args.frame)

	if args.debug:
		print('Recognizing charactor : ', end='')
	label = judge(imgs, args.debug)
	add_to_training_data(label, imgs, args.dest, args.path)
	print(label)


def resize(img, size=2):
	return img.resize((int(img.width * size), int(img.height * size)))

def rotate(img, deg):
	return img.rotate(deg)


# You can arrange image*******************************************************
# Please use in find_keywords()
# e.g. img = resize(sharpness(img), 2.0)

def sharpness(img, SHARPNESS=1.5):
	sharpness_converter = ImageEnhance.Sharpness(img)
	sharpness_img = sharpness_converter.enhance(SHARPNESS)
	return sharpness_img

def contrast(img, CONTRAST=1.5):
	contrast_converter = ImageEnhance.Contrast(img)
	contrast_img = contrast_converter.enhance(CONTRAST)
	return contrast_img

def brightness(img, BRIGHTNESS = 1.5):
	brightness_converter = ImageEnhance.Brightness(img)
	brightness_img = brightness_converter.enhance(BRIGHTNESS)
	return brightness_img

#*****************************************************************************


def get_text(img):
	""" Get text from image by tesseract. The returned text is all upper case.

		:param img: image :type: `Image` object
		:return candidate: Recognized text :type: str
	"""
	text = pytesseract.image_to_string(img, lang='eng')
	return text.upper()


def find_keywords(imgs, debug=False):
	""" Find keywords and return labels. e.g. ['NIMH', 'NIMH', 'UNKNOWN']

		:param imgs: images :type: [`Image` object]
		:param debug: :type: boolean
		:return candidate: Return list of lables :type: [str]
	"""
	candidate = []
	for img in imgs:
		if debug:
			print('*', end='', flush=True)

		img = resize(img)
		for deg in [0.0, 90.0, 180.0, 270.0]:
			img = rotate(img, deg)
			text = get_text(img)

			for category, lst in klst:
				for key in lst:
					if key in text:
						candidate.append(category)
						break;
	return candidate


def judge(imgs, debug=False):
	""" Return label

		:param imgs: images :type: [`Image` object]
		:param debug:  :type: boolean
		:return: Label of battery :type: str
	"""
	candidate = find_keywords(imgs, debug)
	if debug:
		print('\nEstimate : ' + str(set(candidate)))
	if len(set(candidate)) == 1:
		return candidate[0]
	
	return UNKNOWN


def add_to_training_data(label, imgs, dest, video_path):
	""" save frames as training data. Frames move to directory of their label.

		:param label: label of battery :type: str
		:param imgs: frames from a video :type: str
		:param dest: destination directory :type: str
		:param video_path: get file name from this path :type: str
	"""
	video_name = os.path.basename(video_path)
	video_name, _ = os.path.splitext(video_name)

	dir_path  = ''
	if label == UNKNOWN:
		dir_path = './' + UNKNOWN + '/' + video_name + '/'
	else:
		dir_path = dest + '/' + label + '/'

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	for i, im in enumerate(imgs):
		im.save(dir_path + video_name + '_' + str(i) + '.jpg')


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
				prog='labeling_OCR.py', 
				usage='Determine the type of battery from the video by OCR.', 
				description='description...',
				epilog='end',
				add_help=True,
				)
	parser.add_argument('-P', '--path', help="Path to the video. Default is './videos'.", required=False, default='./videos')
	parser.add_argument('-F', '--frame', help='Pick this number of frames from video. Default is 30.', required=False, type=int,
							default=30)
	parser.add_argument('-D', '--dest', help="The path to the training data. Default is './train_data'.", required=False,
							default='./train_data')
	parser.add_argument('--debug', help='Debug mode.', action='store_true', required=False, default=False)

	# parse thearguments.
	args = parser.parse_args()
	main(args)

