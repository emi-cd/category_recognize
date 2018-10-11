# -*- coding: utf-8 -*-

"""
	split_video.py
	~~~~~~~~~~~~~~~

	Dependency::
		python : 3.6.*

	Usage::
	>>> import split_video
	>>> split_video.video_2_frames(./movie.mov, 30)
	Now you can get 30 frames from a moview.mov.
"""
import os
import cv2
from PIL import Image

def crop_center(pil_img, crop_width, crop_height):
	""" Crop the image of the center.

		:param pil_img: :type: `Image` object
		:param crop_width: give the cropping width :type: int
		:param crop_width: give the cropping height :type: int
		:return: cropped image :type: `Image` object
	"""
	img_width, img_height = pil_img.size
	return pil_img.crop(((img_width - crop_width) // 2,
						(img_height - crop_height) // 2,
						(img_width + crop_width) // 2,
						(img_height + crop_height) // 2))

def crop_max_square(pil_img):
	""" Crop to the largest square of the image.

		:param pil_img: :type: `Image` object
		:return: cropped image :type: `Image` object
	"""
	return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def video_2_frames(video_path, num_frame = 30):
	""" Split video into frames and return Image object list.

		:param video_path: path to the video :type: str
		:param num_frame: Pick this number of frames. :type: int
		:return images: list of image from video :type: [`Image` object]
	"""
	# make the image dirctory if it doesn't exsist.
	if not os.path.exists(video_path):
		print("Path to the video does not exist : " + video_path)
		exit(1)
		
	images = []
	# Video to frame.
	video = cv2.VideoCapture(video_path)
	frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	num_frame = num_frame if num_frame < frame_number else frame_number
	index = [frame_number // num_frame * i for i in range(num_frame)]
	
	for i in index:
		video.set(cv2.CAP_PROP_POS_FRAMES, i)
		flag, frame = video.read()
		if flag:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			images.append(crop_max_square(Image.fromarray(frame)))
		else:
			break;

	# When everything done, release the capture.
	video.release()

	return images