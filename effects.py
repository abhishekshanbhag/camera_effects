import numpy as np
import cv2

cam = cv2.VideoCapture(0)

print "Select effect: \n1. No Effect \n2. Thermal \n3. Mirror \n4. Warp\n5. Exit"
cv2.namedWindow("Camera")
choice = -1

def thermal():	
	global choice	
	choice = -1
	while (choice == -1):	
		ret, frame_thermal = cam.read()
		final = np.zeros((frame_thermal.shape), np.float_)		
		gray1 = cv2.cvtColor(frame_thermal, cv2.COLOR_BGR2GRAY)
		gray = np.float_(cv2.equalizeHist(gray1))
	
		m = gray<50
		#masked = np.multiply(m,gray)
		final[:,:,0] += np.multiply((((gray/50.0)*195) + 60),m)
		final[:,:,2] += np.multiply((80 - (gray/5.0)*8),m)

		n = np.logical_and(gray>=50, gray<135)
		final[:,:,0] += np.multiply(n,255)
		#cv2.imshow("70T110", final)
	
		m = np.logical_and(gray>=135, gray<150)
		final[:,:,0] += np.multiply(m,((150 - gray)*(255.0/15)))
		#cv2.imshow("110T180", final)

		n = np.logical_and(gray>=90, gray<130)
		final[:,:,1] += np.multiply(n,((gray - 90)*(255.0/40)))
		#cv2.imshow("110T180", final)

		m = np.logical_and(gray>=130, gray<205)
		final[:,:,1] += np.multiply(m,255)
		#cv2.imshow("110T180", final)

		n = np.logical_and(gray>=205, gray<230)
		final[:,:,1] += np.multiply(n,((230 - gray)*(255.0/25)))
		#cv2.imshow("110T180", final)

		m = np.logical_and(gray>=160, gray<200)
		final[:,:,2] += np.multiply(m,((gray - 160)*(255.0/40)))
		#cv2.imshow("110T180", np.uint8(final))

		n = gray>200
		final[:,:,2] += np.multiply(n,255)
		cv2.imshow("Camera", np.uint8(final))
		#cv2.imshow("Stream", np.uint8(gray))
		#break
		choice = cv2.waitKey(30)


def mirror():
	global choice	
	choice = -1
	ret, frame = cam.read()
	row, col, ch = frame.shape
	mir = np.zeros((row, col, ch), np.uint8)
	while choice == -1:	
		ret, frame = cam.read()
		frame2 = cv2.flip(frame, 1)
		mir[0:row,0:col/2,:] = frame[0:row, 0:col/2, :]
		mir[0:row,col/2:col,:] = frame2[0:row, col/2:col, :]	
		#cv2.imshow("Stream", frame)
		cv2.imshow("Camera", mir)
		choice = cv2.waitKey(30)

def warp():
	global choice
	choice = -1


while(True):

	ret, frame = cam.read()
	cv2.imshow("Camera", frame)
	if choice == -1 or choice  == 1:
		choice = cv2.waitKey(30)
	elif (choice == ord('2')):
		thermal()
		#choice = -1
	elif choice == ord('3'):
		mirror()
		#choice = -1
	elif choice == ord('4'):
		warp()
		#choice = -1
	elif choice == ord('5') or (choice == 27):
		break
	else: 
		choice  = -1

cv2.destroyAllWindows()
	


