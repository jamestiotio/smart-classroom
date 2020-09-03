import pygame
import cv2 as cv
import numpy as np

pygame.init()
screen = pygame.display.set_mode([800,600])
font = pygame.font.SysFont('ubuntumono', 32) 

labels_e = ('neutral', 'happy', 'sad', 'surprise', 'anger')
net_e = cv.dnn.readNet('./emotions-recognition-retail-0003.bin','./emotions-recognition-retail-0003.xml')
net_f = cv.dnn.readNet('./face-detection-adas-0001.bin','./face-detection-adas-0001.xml')

def test_net_e():
	# https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/intel/emotions-recognition-retail-0003/description/emotions-recognition-retail-0003.md
	img = cv.imread('./emotions-recognition-retail-0003.jpg', cv.IMREAD_COLOR)
	blob = cv.dnn.blobFromImage(img, size=(64,64))
	net_e.setInput(blob)
	out = net_e.forward()
	out = out.flatten()
	labels = ('neutral', 'happy', 'sad', 'surprise', 'anger')
	print(list(zip(out, labels)))
test_net_e()

cap = cv.VideoCapture(1)

while True:
	ret, frame = cap.read()

	blob = cv.dnn.blobFromImage(frame, size=(672, 384))
	net_f.setInput(blob)
	out_f = net_f.forward()

	#pgframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
	#pgframe = np.rot90(pgframe)
	#pgframe = cv.flip(pgframe, 0)
	#pgframes = pygame.surfarray.make_surface(pgframe)
	#screen.blit(pgframes, (0,0))

	for detection in out_f.reshape(-1, 7):
		confidence = float(detection[2])
		if(confidence < 0.5): continue
		xmin = int(detection[3] * frame.shape[1])
		ymin = int(detection[4] * frame.shape[0])
		xmax = int(detection[5] * frame.shape[1])
		ymax = int(detection[6] * frame.shape[0])
		#print(confidence, xmin, ymin, xmax, ymax)
		#pygame.draw.rect(screen, (255,0,0), (xmin,ymin,xmax-xmin,ymax-ymin), 2)

		#crop_face = pgframe[xmin:xmax,ymin:ymax] # color version
		
		crop_face = frame[ymin:ymax,xmin:xmax] # real np version
		face_blob = cv.dnn.blobFromImage(crop_face, size=(64, 64))
		net_e.setInput(face_blob)
		out_e = net_e.forward()
		out_e = out_e.flatten()
		emotion = labels_e[np.argmax(out_e)]
		img_text_emotion = font.render(emotion, True, (0,255,0))
		
		screen.blit(pygame.surfarray.make_surface(np.rot90(crop_face)), (0,0))
		screen.blit(img_text_emotion, (10, 10))

	pygame.display.update()
