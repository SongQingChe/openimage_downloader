import os
import xml.dom.minidom as xmldom
def parse_xml(xml_path):
    """
    get the information in the xml file
        args:
            xml_path: the path to single .xml file
        returns:
            output_dict: {'size':(H,W,C), 
                            'objects':[(label_name,x1,y1,x2,y2),(label_name,x1,y1,x2,y2)]}
    """
    output_dict = {}
    DOMTree = xmldom.parse(xml_path)
    annotation = DOMTree.documentElement
    #img_name = annotation.getElementsByTagName('filename')[0].firstChild.data
    img_size = annotation.getElementsByTagName('size')
    img_height = img_size[0].getElementsByTagName('height')[0].childNodes[0].data
    img_width = img_size[0].getElementsByTagName('width')[0].childNodes[0].data
    img_depth = img_size[0].getElementsByTagName('depth')[0].childNodes[0].data
    output_dict['size'] = (img_height, img_width, img_depth)
    #print(output_dict)

    _objects = annotation.getElementsByTagName('object')
    output_dict['objects'] = list()
    for _object in _objects:
        label_name = _object.getElementsByTagName('name')[0].childNodes[0].data
        #print(label_name)
        bbox = _object.getElementsByTagName('bndbox')[0]
        left = bbox.getElementsByTagName('xmin')[0].childNodes[0].data
        top = bbox.getElementsByTagName('ymin')[0].childNodes[0].data
        right = bbox.getElementsByTagName('xmax')[0].childNodes[0].data
        bottom = bbox.getElementsByTagName('ymax')[0].childNodes[0].data
        res_tuple = (label_name, int(left), int(top), int(right), int(bottom))
        output_dict['objects'].append(res_tuple)
    #print(output_dict) 
    return output_dict # {'size':tuple, 'objects':list}

data_dir = 'OID/dogandcat_trun/train/Cat_clean_/'
xml_dir = data_dir + 'xmls'
img_dir = data_dir + 'imgs'
for xml_path in [os.path.join(xml_dir, xml_name) for xml_name in os.listdir(xml_dir)]:
    #print(parse_xml(xml_path)['objects'])
    if len(parse_xml(xml_path)['objects']) == 0:
        print('empty')
        os.remove(xml_path)
        img_path = os.path.join(img_dir, os.path.splitext(os.path.split(xml_path)[-1])[-2]+'.jpg')
        os.remove(img_path)