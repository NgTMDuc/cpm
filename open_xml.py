import xml.etree.ElementTree as ET
import os
import os.path as osp

this_dir = osp.dirname(os.path.abspath(__file__))
XML_PATH = "20230113_aflw_part_0_neck_annotation_sangdv.xml"
image_dir = osp.join(this_dir, 'datasets',  'AFLW', 'flickr')
save_info_path = "datasets/AFLW/aflwInfo.txt"
save_name_path = "datasets/AFLW/aflwName.txt"


def get_all_images(XML_PATH, img_path, tag_label = "all_neck_visible"):
    results = []
    image_name_results = []
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    for image in root.findall("./image"):
        tag  = image.find("tag")

        #If the tag's label is all_neck_visible
        if tag.attrib["label"] == tag_label:
            item = dict()

            image_name = image.attrib['name']
            image_name_results.append(image_name)
            image_path = os.path.join(img_path, image_name)

            points = image.find("points")
            str_point1, str_point2 = points.attrib['points'].split(';')
            x1, y1 = [float(s) for s in str_point1.split(',')]
            x2, y2 = [float(s) for s in str_point2.split(',')]
            item['image_name'] = image_name
            item['image_path'] = image_path
            d = dict()   
            d['22'] = (x1, y1)
            d['23'] = (x2, y2)
            item['keypoints'] = d

            results.append(item)
        
    return image_name_results, results


if __name__ == "__main__":
    image_name_results, img_results = get_all_images(XML_PATH, image_dir)
    # print(image_name_results)
    with open(save_info_path, "w") as f:
        f.writelines([f"{x}\n" for x in img_results])
    
    with open(save_name_path, "w") as f:
        f.writelines([f"{x}\n" for x in image_name_results])