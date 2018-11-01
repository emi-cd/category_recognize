# -*- coding: utf-8 -*-

"""
	take_video.py
	~~~~~~~~~~~~~~~

	Take video.

	Dependency::
		python : 3.6.*
		Package : Please look requirements.txt 

	Usage::
	>>> python take_video.py
	if you want to stop this program, please enter 'q'.

"""
import cv2
import time
import argparse
import os, shutil

parser = argparse.ArgumentParser(
			prog='take_video.py', 
			usage='Take video', 
			description='description...',
			epilog='end',
			add_help=True,
			)
parser.add_argument('-T', '--time', help="Length of video. Default is 20 seconds.", required=False, type=int, default=20)

# parse thearguments.
args = parser.parse_args()

def main():
	index = 0
	PATH = './videos'
	TMP_PATH = PATH + '/.tmp'
	LOG_PATH = TMP_PATH + '/log.txt'

	if not os.path.exists(TMP_PATH):
		os.makedirs(TMP_PATH)
	if os.path.exists(LOG_PATH):
		with open(LOG_PATH, mode='r') as f:
			index = int(f.read())

	cap = cv2.VideoCapture(1)

	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
	cap.set(3, 1280) # set the Horizontal resolution
	cap.set(4, 720) # Set the Vertical resolution

	# Define the codec and create VideoWriter object
	fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	fps = 20.0
	size = (720, 580)
	video = cv2.VideoWriter(TMP_PATH + '/{:05}.mov'.format(index), fmt, fps, size)


	start_time = time.time()
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret==True:
			t = time.time() - start_time
			x = frame.shape[1] // 2 
			y = frame.shape[0] // 2
			frame = frame[y - size[1]//2:y + size[1]//2, x - size[0]//2:x + size[0]//2]
			frame = cv2.resize(frame, size)
			if t < args.time:
				# write the flipped frame
				video.write(frame)
				cv2.circle(frame, (15, 15), 5, (0, 0, 255), thickness=-1)
			elif t > args.time + 5:
				shutil.move(TMP_PATH + '/{:05}.mov'.format(index), PATH)
				index  = index + 1 if index < 100000 else 0
				video = cv2.VideoWriter(TMP_PATH + '/{:05}.mov'.format(index), fmt, fps, size)
				start_time = time.time()

			cv2.imshow('frame',frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				os.remove(TMP_PATH + '/{:05}.mov'.format(index))
				break
		else:
			break


	with open(LOG_PATH, mode='w') as f:
		f.write(str(index))


	# Release everything if job is finished
	cap.release()
	video.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
