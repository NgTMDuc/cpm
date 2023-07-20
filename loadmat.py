from scipy.io import loadmat
import numpy as np
import os.path as osp
import os

this_dir = osp.dirname(os.path.abspath(__file__))
mat_path = osp.join(this_dir,'datasets','AFLW','AFLWinfo_release.mat')
mat = loadmat(mat_path)
save_info_path = "datasets/AFLW/aflwInfo.txt"
save_name_path = "datasets/AFLW/aflwName.txt"


def openSaveNameFile(save_name_path):
    results = []
    with open(save_name_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            name = line.strip()
            results.append(name)
    return results

def openSaveInfoFile(save_info_path):
    results = []
    with open(save_info_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            info = line.strip()
            results.append(eval(info))
    return results

def find_info(name, face_info):
    for face in face_info:
        if name == face["image_name"]:
            return face
    
def scale_bbox(bbox, w_increase, h_increase):
    old_x = bbox[0]
    old_y = bbox[2]
    old_w = bbox[1]
    old_h = bbox[3]

    new_x = old_x - w_increase * old_w
    if new_x < 0:
        new_x = 0
    
    new_y = old_y
    new_w = (1 + 2 * w_increase) * old_w
    new_h = (1 + h_increase) * old_h

    new_bbox = (new_x, new_w, new_y, new_h)
    
    return new_bbox

name_list = openSaveNameFile(save_name_path)
face_info = openSaveInfoFile(save_info_path)

def loadMatFile(mat_path, name_list = name_list, face_info = face_info):
    total_image = 24386
    aflwinfo = dict()
    # results = []
    mat = loadmat(mat_path)
    aflwinfo['name-list'] = []
    aflwinfo["mask"] = []
    aflwinfo["landmark"] = []
    aflwinfo['box'] = []
    tmp_name = mat["nameList"][:, 0]
    tmp_mask = mat['mask_new'].copy()
    
    tmp_landmark = mat['data'].reshape((total_image, 2, 19))
    tmp_landmark = np.transpose(tmp_landmark, (0,2,1))
    tmp_bbox = mat['bbox'].copy()
    for i in range(total_image):
        # print(str(tmp_name[i][0]).split("/")[1])
        # break
        if str(tmp_name[i][0]).split("/")[1] in name_list:
            # print(1)
            aflwinfo["name-list"].append(str(tmp_name[i][0]))
            aflwinfo["mask"].append(np.append(tmp_mask[i], [1,1]))
            # tmp = tmp_landmark[i]
            tmp = find_info(str(tmp_name[i][0]).split("/")[1], face_info)
            keypoints = tmp['keypoints']
            landmark = tmp_landmark[i]
            for key, value in keypoints.items():
                landmark = np.append(landmark, [list(value)], axis = 0)
            aflwinfo['landmark'].append(landmark)
            aflwinfo['box'].append(scale_bbox(tmp_bbox[i], 1/3, 1/4))

            # results.append(aflwinfo)
    return aflwinfo

if __name__ == "__main__":
    # print(name_list)
    results = loadMatFile(mat_path)
    # print(len(results))
    # print(len(results["name-list"]))
    print(results['name-list'][0])
    # for face in face_info:
        # print(type(face))
        # print(face["image_name"])
        # break