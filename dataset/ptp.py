# ------------------------------------------------------------------------------
# Nazgul Mamasheva
# -----------------------------------------------------------------------------

import os
import cv2
import numpy as np

from dataset.base_dataset import BaseDataset

class ptp(BaseDataset):
    def __init__(self, data_path, is_train=True, crop_size=(448, 448), scale_size=None):
        super().__init__(crop_size)

        self.scale_size = scale_size

        self.is_train = is_train

        self.image_list = []
        self.depth_list = []

        if is_train:
            self.dataset_path = os.path.join(data_path, 'train')
        else:
            self.dataset_path = os.path.join(data_path, 'test')


        for file in os.listdir(self.dataset_path):
            if file.endswith(".jpg"):
                self.image_list.append(file)
                self.depth_list.append(os.path.splitext(file)[0] + '.npy')

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):

        img_path = self.dataset_path + '/' + self.image_list[idx]
        gt_path = self.dataset_path + '/' + self.depth_list[idx]

        filename = 'eval' + '_' + img_path.split('/')[-1]

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        depth = np.load(gt_path).astype('float32')

        if self.scale_size:
            image = cv2.resize(image, (self.scale_size[0], self.scale_size[1]))
            depth = cv2.resize(image, (self.scale_size[0], self.scale_size[1]))

        if self.is_train:
            image, depth = self.augment_training_data(image, depth)
        else:
            image, depth = self.augment_test_data(image, depth)

        depth = depth / 1000.0  # convert in meters

        return {'image': image, 'depth': depth, 'filename': filename}
