import os
import shutil
import gen_xml
current_dir = os.path.dirname(os.path.abspath(__file__))

img_dir = './OID/test/test/Human hair_Human head' # modify here
save_dir = img_dir + '_clean' # modify here
img_savedir = os.path.join(save_dir, 'imgs')
xml_savedir = os.path.join(save_dir, 'xmls')
labeltxt_dir = os.path.join(img_dir, 'Label')
label_paths = [os.path.join(labeltxt_dir, labeltxt_name) \
                    for labeltxt_name in os.listdir(labeltxt_dir)]
img_paths = [os.path.join(img_dir, img_name) \
                for img_name in os.listdir(img_dir) \
                    if os.path.splitext(img_name)[-1]=='.jpg']

if os.path.exists(save_dir):
    shutil.rmtree(save_dir)
os.makedirs(img_savedir)
os.makedirs(xml_savedir)

for img_path in img_paths:
    img_savepath = os.path.join(img_savedir, os.path.split(img_path)[-1])
    shutil.copy(img_path, img_savepath)
    xml_savepath = os.path.join(xml_savedir, os.path.splitext(os.path.split(img_path)[-1])[-2]+'.xml')
    labeltxt_name = os.path.splitext(os.path.split(img_path)[-1])[-2]
    label_path = os.path.join(labeltxt_dir, labeltxt_name+'.txt')
    if label_path in label_paths:
        bboxes = []
        labels = []
        with open(label_path, 'r') as f:
            for content in f.readlines():
                label_names = os.path.split(img_dir)[-1].split('_')
                label_name = ' '.join(content.strip().split(' ')[:-4])
                if label_name not in label_names: print('error') # 'Cat'
                bboxes.append([int(float(ele)) for ele in content.strip().split(' ')[-4:]])
                labels.append(label_name.lower()) # 'cat'
        #print(bboxes)
        if len(bboxes):
            if not gen_xml.write_xml(img_savepath, bboxes, labels, xml_savepath):
                os.remove(img_savepath)
                continue

