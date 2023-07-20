# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import sys
import os, math
import os.path as osp
import numpy as np
assert sys.version_info.major == 3, 'Please upgrade from {:} to Python 3.x'.format(sys.version_info)
from scipy.io import loadmat
from data import PTSconvert2box,PTSconvert2str
from loadmat import loadMatFile

#Change this paths according to your directories
# this_dir = osp.dirname(os.path.abspath(__file__))
this_dir = "/content/cpm"
SAVE_DIR = osp.join(this_dir, 'datasets','AFLW_lists')
if not osp.isdir(SAVE_DIR): os.makedirs(SAVE_DIR)
image_dir = osp.join(this_dir, 'datasets',  'AFLW', 'flickr')
annot_dir = osp.join(this_dir, 'datasets',  'AFLW', 'annotations')
from open_xml import *

XML_PATH = "20230113_aflw_part_0_neck_annotation_sangdv.xml"
print ('AFLW image dir : {}'.format(image_dir))
print ('AFLW annotation dir : {}'.format(annot_dir))
assert osp.isdir(image_dir), 'The image dir : {} does not exist'.format(image_dir)

image_name_results, img_results = get_all_images(XML_PATH, image_dir)
TRAIN_TEST_SPLIT = 0.8

class AFLWFace():
  def __init__(self, index, name, mask, landmark, box):
    self.image_path = name
    self.face_id = index
    self.face_box = [float(box[0]), float(box[2]), float(box[1]), float(box[3])]
    mask = np.expand_dims(mask, axis=1)
    landmark = landmark.copy()
    self.landmarks = np.concatenate((landmark, mask), axis=1)

  def get_face_size(self, use_box):
    box = []
    if use_box == 'GTL':
      box = PTSconvert2box(self.landmarks.copy().T)
    elif use_box == 'GTB':
      box = [self.face_box[0], self.face_box[1], self.face_box[2], self.face_box[3]]
    else:
      assert False, 'The box indicator not find : {}'.format(use_box)
    assert box[2] > box[0], 'The size of box is not right [{}] : {}'.format(self.face_id, box)
    assert box[3] > box[1], 'The size of box is not right [{}] : {}'.format(self.face_id, box)
    face_size = math.sqrt( float(box[3]-box[1]) * float(box[2]-box[0]) )
    box_str = '{:.2f} {:.2f} {:.2f} {:.2f}'.format(box[0], box[1], box[2], box[3])
    return box_str, face_size

  def check_front(self):
    oks = 0
    box = self.face_box
    for idx in range(self.landmarks.shape[0]):
      if bool(self.landmarks[idx,2]):
        x, y = self.landmarks[idx,0], self.landmarks[idx,1]
        if x > self.face_box[0] and x < self.face_box[2]:
          if y > self.face_box[1] and y < self.face_box[3]:
            oks = oks + 1
    return oks == 5
    
  def __repr__(self):
    return ('{name}(path={image_path}, face-id={face_id})'.format(name=self.__class__.__name__, **self.__dict__))

def save_to_list_file(all_faces, 
                      lst_file, 
                      image_style_dir,
                      annotation_dir, 
                      use_front, 
                      use_box):
  save_faces = []
  for face in all_faces:
    if use_front == False or face.check_font():
      save_faces.append(face)
  print ('Prepare to save {} face images into {}'.format(len(save_faces), lst_file))

  lst_file = open(lst_file, 'w')
  all_face_sizes = []
  for face in save_faces:
    image_path = face.image_path
    sub_dir, base_name = image_path.split('/')
    cannot_dir = osp.join(annotation_dir, sub_dir)
    cannot_path = osp.join(cannot_dir, base_name.split('.')[0] + '-{}.pts'.format(face.face_id))
    if not osp.isdir(cannot_dir): os.makedirs(cannot_dir)
    image_path = osp.join(image_style_dir, image_path)
    # assert osp.isfile(image_path), 'The image [{}/{}] {} does not exsit'.format(index, len(save_faces), image_path)

    if not osp.isfile(cannot_path):
      pts_str = PTSconvert2str( face.landmarks.T )
      pts_file = open(cannot_path, 'w')
      pts_file.write('{}'.format(pts_str))
      pts_file.close()
    else: pts_str = None

    box_str, face_size = face.get_face_size(use_box)

    lst_file.write('{} {} {} {}\n'.format(image_path, cannot_path, box_str, face_size))
    all_face_sizes.append( face_size )
  lst_file.close()

  all_faces = np.array( all_face_sizes )
  print ('all faces : mean={}, std={}'.format(all_faces.mean(), all_faces.std()))

if __name__ == "__main__":
  mat_path = osp.join(this_dir,'datasets','AFLW','AFLWinfo_release.mat')
  aflwinfo = dict()
  aflwinfo = loadMatFile(mat_path)
  train_faces = []
  total_image = len(aflwinfo['name-list'])
  train_index = int(total_image * TRAIN_TEST_SPLIT)
  for i in range(train_index):
    face = AFLWFace(i, aflwinfo['name-list'][i], aflwinfo['mask'][i], aflwinfo['landmark'][i], aflwinfo['box'][i])
    train_faces.append( face )
  
  test_faces = []
  for i in range(train_index,total_image):
    face = AFLWFace(i, aflwinfo['name-list'][i], aflwinfo['mask'][i], aflwinfo['landmark'][i], aflwinfo['box'][i])
    test_faces.append(face)
  
  allfaces = test_faces + train_faces
  USE_BOXES = ['GTL', 'GTB']
  
  for USE_BOX in USE_BOXES:
    save_to_list_file(train_faces, osp.join(SAVE_DIR, 'train.{}'.format(USE_BOX)),      image_dir, annot_dir, False, USE_BOX) 
    print("done")
    save_to_list_file(test_faces, osp.join(SAVE_DIR, 'test.{}'.format(USE_BOX)),       image_dir, annot_dir,  False, USE_BOX)
    print("done")
    # save_to_list_file(allfaces, osp.join(SAVE_DIR, 'test.front.{}'.format(USE_BOX)), image_dir, annot_dir, True,  USE_BOX)
    save_to_list_file(allfaces, osp.join(SAVE_DIR, 'all.{}'.format(USE_BOX)),        image_dir, annot_dir, False, USE_BOX)
