import matplotlib.pyplot as plt

image_save_folder = './images/'

def plot(nodes, active_accidents, patients_saved, current_location):
	for i in range(time):
		plt.scatter(x=active_accidents[:, 0], y=active_accidents[:, 1], c='r')
		plt.scatter(x=patients_saved[:, 0], y=patients_saved[:, 1], c='g')
		plt.scatter(x=current_location[0], current_location[1], c='y')
		for j in range(nodes.shape[0]):
			if (not([nodes[j, 0], nodes[j, 1]] in active_accidents) and not([nodes[j, 0], nodes[j, 1]] in active_accidents)):
				plt.scatter(x=nodes[j, 0], y=nodes[j, 1], c='b')

		plt.savefig(image_save_folder + str(i) + '.png')

def plot1(nodes, hospitals, path1):
	color = ['y', 'b', 'orange', 'black', 'r']

	for a in range(len(path1)):
		for b in range (len(path1)):
			active_node, ambulance_assigned, path = path1[a]
			node_x, node_y = nodes[active_node, 0], nodes[active_node, 1]
			plt.plot(node_x, node_y, c=color[ambulance_assigned], marker='o')
			current_node_x, current_node_y = nodes[path[b], 0], nodes[path[b], 1]
			plt.plot(current_node_x, current_node_y, c=color[ambulance_assigned], marker='v')
		#for j in range()

	plt.scatter(x=hospitals[:, 0], y=hospitals[:, 1], c='g', marker='o')

	plt.savefig(image_save_folder + str(t) + '.png')


def make_video():
	import cv2
	import os

	video_name = 'video.avi'

	images = [img for img in os.listdir(image_save_folder) if img.endswith(".png")]
	images.sort()
	frame = cv2.imread(os.path.join(image_folder, images[0]))
	height, width, layers = frame.shape

	video = cv2.VideoWriter(video_name, 0, 2, (width,height))

	for image in images:
	    video.write(cv2.imread(os.path.join(image_folder, image)))

	cv2.destroyAllWindows()
	video.release()