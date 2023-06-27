import numpy as np
import os
import torch
import cv2
# with open("datasets/AFLW/annotations/0/image00002-7135.pts", "r") as f:
#     content = f.readlines()
# print(content)
# print(torch.ByteTensor([False]))

# a = np.zeros((3,3, 19))
# print(a.view(19, -1))
img = cv2.imread("datasets/images/image_0019.png")
print(img.shape)