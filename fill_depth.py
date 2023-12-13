# ------------------------------------------------------------------------------
# Nazgul Mamasheva
# -----------------------------------------------------------------------------

import os
import cv2
import numpy as np

from utils.colorization import fill_depth_colorization as fill_depth_colorization


raw_data_path = "./dataset/inputs/raw_ptp/"
colorized_data_path = "./dataset/inputs/colorized_ptp/"

for file in os.listdir(raw_data_path):
	if file.endswith(".jpg"):

		image_path = os.path.join(raw_data_path, file)
		depth_path = os.path.join(raw_data_path, os.path.splitext(file)[0] + ".npy")

		raw_image = cv2.imread(image_path)

		# cutting raw image into image and mask
		width = raw_image.shape[1]

		width_cutoff = width // 2
		orig_image = raw_image[:, :width_cutoff]
		mask = raw_image[:, width_cutoff:]


		image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
		image = image/255 # convert to range 0 to 1


		depth = np.load(depth_path)
		depth = depth / 1000.0  # convert in meters


		res = fill_depth_colorization(image, depth)


		image_name = os.path.basename(image_path)
		depth_name = os.path.basename(depth_path)

		cv2.imwrite(colorized_data_path + image_name, orig_image)
		cv2.imwrite(colorized_data_path + image_name.split(".")[0] + "_mask.jpg", mask)
		np.save(colorized_data_path + depth_name, res)
