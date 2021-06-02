import os
import xml.etree.ElementTree as et
from os import listdir
from os.path import isfile, join
from numpy.core.shape_base import block
import pandas as pd
import cv2
import numpy as np
import shutil
# from sklearn import train_test_split
import albumentations as A

def prepare_codebrim_yolo(path_images, path_annotations, output):

    new_object = "{class_label} {x_center} {y_center} {width} {height}\n"
    xml_extension = "{}.xml"
    txt_extension = "{}.txt"

    # Reading codebrim images
    image_ids = [f for f in listdir(path_images) if isfile(join(path_images,f))]
    for image_id in image_ids:

        id_wo_extension = os.path.splitext(image_id)[0]
        image_annotation = join(path_annotations, xml_extension.format(id_wo_extension))

        if isfile(image_annotation):
            
            xtree = et.parse(image_annotation)
            xroot = xtree.getroot()

            image_height, image_width = cv2.imread( join(path_images, image_id ) ).shape[:2]
            for obj in xroot.iter("object"):

                with open(join(output, txt_extension.format(id_wo_extension)), "a+") as output_file:
                    bndbox = obj.find("bndbox")
                    x_center = ( int( bndbox.find( "xmin" ).text ) + int( bndbox.find( "xmax" ).text ) )/ 2 / image_width
                    y_center = ( int( bndbox.find( "ymin" ).text ) + int( bndbox.find( "ymax" ).text ) ) / 2 / image_height
                    width = ( int( bndbox.find( "xmax" ).text ) - int( bndbox.find( "xmin" ).text ) ) / image_width
                    height = ( int( bndbox.find( "ymax" ).text ) - int( bndbox.find( "ymin" ).text ) ) / image_height

                    defects = obj.find( "Defect" )
                    for defect in defects:

                        is_defect_present = defect.text == "1"
                        if is_defect_present:

                            defect_name = defect.tag
                            if defect_name == "Crack":
                                label = 0
                            elif defect_name == "Spallation":
                                label = 1
                            elif defect_name == "Efflorescence":
                                label = 2
                            elif defect_name == "ExposedBars":
                                label = 3
                            elif defect_name == "CorrosionStain":
                                label = 4
                        
                            output_file.write(
                                new_object.format(
                                    class_label = label,
                                    x_center = x_center,
                                    y_center = y_center,
                                    width = width,
                                    height = height
                                )
                            )
                output_file.close()


def split_data( path_labels, path_images, output, train = 0.6, val = 0.2, test = 0.2 ):

    jpg_extension = "{}.jpg"
    
    fractions = np.array([train, val, test])
    # Reading codebrim labels
    image_ids = [f for f in listdir(path_labels) if isfile(join(path_labels,f))]
    # print( image_ids )
    list_images = pd.Series(image_ids)
    # print(list_images)
    # Shuffle the input
    list_images = list_images.sample(frac=1)
    # Split into 3 parts
    train, val, test = np.array_split(
        list_images, (fractions[:-1].cumsum() * len(list_images)).astype(int)
    )

    print( "Creating first folders... ")
    if not os.path.exists(join(output, "images")):
        os.makedirs(join(output, "images"))
    if not os.path.exists(join(output, "labels")):  
        os.makedirs(join(output, "labels"))
    print( "Creating secondary folders... ")
    if not os.path.exists(join( join(output, "images"), "train" )):
        os.makedirs(join( join(output, "images"), "train" ))
    if not os.path.exists(join( join(output, "labels"), "train" )):
        os.makedirs(join( join(output, "labels"), "train" ))

    print( "Training files... " )
    with open(join(output, "train.txt"), "w") as f:
        for value in train:

            id_wo_extension = os.path.splitext(value)[0]
            path = join(path_images, jpg_extension.format(id_wo_extension))
            path2=join( join( join(output, "images"), "train" ), jpg_extension.format(id_wo_extension))
            f.write(path2+"\n")
            shutil.copy(path, path2)
            shutil.copy(join(path_labels, value), join( join( join(output, "labels"), "train" ), value ) )
    f.close()


    if not os.path.exists(join( join(output, "images"), "test" )): 
        os.makedirs(join( join(output, "images"), "test" ))
    if not os.path.exists(join( join(output, "labels"), "test" )):
        os.makedirs(join( join(output, "labels"), "test" ))
    print( "Test files... " )
    with open(join(output, "test.txt"), "w") as f:
        for value in test:

            id_wo_extension = os.path.splitext(value)[0]
            path = join(path_images, jpg_extension.format(id_wo_extension))
            path2=join( join( join(output, "images"), "test" ), jpg_extension.format(id_wo_extension))
            f.write(path2+"\n")
            shutil.copy(path, path2)
            shutil.copy(join(path_labels, value), join( join( join(output, "labels"), "test" ), value ) )
    f.close()

    if not os.path.exists(join( join(output, "images"), "val" )):
        os.makedirs(join( join(output, "images"), "val" ))
    if not os.path.exists(join( join(output, "labels"), "val" )):
        os.makedirs(join( join(output, "labels"), "val" ))
    print( "Val files... " )
    with open(join(output, "val.txt"), "w") as f:
        for value in val:

            id_wo_extension = os.path.splitext(value)[0]
            path = join(path_images, jpg_extension.format(id_wo_extension))
            path2=join( join( join(output, "images"), "val" ), jpg_extension.format(id_wo_extension))
            f.write(path2+"\n")
            shutil.copy(path, path2)
            shutil.copy(join(path_labels, value), join( join( join(output, "labels"), "val" ), value ) )
    f.close()


def data_augmentation(path_images, path_annotations, output_images, output_labels, number_of_copies=1):

    new_object = "{class_label} {x_center} {y_center} {width} {height}\n"
    xml_extension = "{}.xml"
    txt_extension = "{}.txt"

    transform = A.Compose([ 
            # A.CenterCrop(width=850,height=850, p=0.3),
            A.RandomSizedBBoxSafeCrop(width=650, height=650, erosion_rate=0.2), # EXPLANATION: https://albumentations.ai/docs/examples/example_bboxes2/#using-randomsizedbboxsafecrop-to-keep-all-bounding-boxes-from-the-original-image
            A.HorizontalFlip(p=0.6),
            A.RandomBrightnessContrast(p=0.8),
            A.ShiftScaleRotate(p=0.5),
            A.RGBShift(r_shift_limit=30, g_shift_limit=30, b_shift_limit=30, p=0.5),
            A.MedianBlur (blur_limit=7, always_apply=False, p=0.5),
            A.GaussNoise (var_limit=(10.0, 50.0), mean=0, always_apply=False, p=0.5)
        ], bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.5))

    # Reading codebrim images
    image_ids = [f for f in listdir(path_images) if isfile(join(path_images,f))]
    print( "TOTAL IMAGES: ", len( image_ids ) )
    for image_id in image_ids:

        id_wo_extension = os.path.splitext(image_id)[0]
        image_annotation = join(path_annotations, xml_extension.format(id_wo_extension))
        if isfile(image_annotation):
            xtree = et.parse(image_annotation)
            xroot = xtree.getroot()

            image =  cv2.imread( join(path_images, image_id ) )
            image_height, image_width = image.shape[:2]
            bboxes = []
            Efflorescence = False
            Spallation = False
            Crack = False
            ExposedBars = False
            CorrosionStain = False
            for obj in xroot.iter("object"):

                # with open(join(output, txt_extension.format(id_wo_extension)), "a+") as output_file:
                bndbox = obj.find("bndbox")
                ## YOLO FORMAT
                # x_center = ( int( bndbox.find( "xmin" ).text ) + int( bndbox.find( "xmax" ).text ) )/ 2 / image_width
                # y_center = ( int( bndbox.find( "ymin" ).text ) + int( bndbox.find( "ymax" ).text ) ) / 2 / image_height
                # width = ( int( bndbox.find( "xmax" ).text ) - int( bndbox.find( "xmin" ).text )  ) / image_width
                # height = ( int( bndbox.find( "ymax" ).text ) - int( bndbox.find( "ymin" ).text )  ) / image_height
                ## COCO FORMAT
                # x_min = int( bndbox.find( "xmin" ).text )
                # y_min = int( bndbox.find( "ymin" ).text )
                # width = ( int( bndbox.find( "xmax" ).text ) - int( bndbox.find( "xmin" ).text ) )
                # height = ( int( bndbox.find( "ymax" ).text ) - int( bndbox.find( "ymin" ).text ) )
                ## Albumentations format
                # x_min = int( bndbox.find( "xmin" ).text ) / image_width
                # y_min = int( bndbox.find( "ymin" ).text ) / image_height
                # x_max = int( bndbox.find( "xmax" ).text ) / image_width
                # y_max = int( bndbox.find( "ymax" ).text ) / image_height
                ## Pascal_voc format
                x_min = int( bndbox.find( "xmin" ).text ) 
                y_min = int( bndbox.find( "ymin" ).text ) 
                x_max = int( bndbox.find( "xmax" ).text ) 
                y_max = int( bndbox.find( "ymax" ).text )

                defects = obj.find( "Defect" )
                for defect in defects:

                    is_defect_present = defect.text == "1"
                    if is_defect_present:

                        defect_name = defect.tag
                        if defect_name == "Crack":
                            label = 0
                        elif defect_name == "Spallation":
                            label = 1
                        elif defect_name == "Efflorescence":
                            label = 2
                        elif defect_name == "ExposedBars":
                            label = 3
                        elif defect_name == "CorrosionStain":
                            label = 4
                    
                        # x_center = x_center if x_center > 0 and x_center < 1 else 0 if x_center < 0 else 1
                        # y_center = y_center if y_center > 0 and y_center < 1 else 0 if  y_center < 0 else 1 
                        # width = width if width > 0 and width < 1 else 0 if width < 0 else 1 
                        # height = height if height > 0 and height < 1 else 0 if  height < 0 else 1
                        # print ( x_center, y_center, width, height )
                        ## YOLO FORMAT
                        # bboxes.append([x_center, y_center, width, height, str(label)])
                        ## COCO FORMAT
                        # bboxes.append([x_min, y_min, width, height, str(label)])
                        ## ALBUMENTATIONS FORMAT
                        bboxes.append([x_min, y_min, x_max, y_max, str(label)])
                        if label == 2:
                            Efflorescence = True
                        elif label == 1:
                            Spallation = True
                        elif label == 3:
                            ExposedBars = True
                        elif label == 4:
                            CorrosionStain = True
                        elif label == 0:
                            Crack = True
                            # output_file.write(
                                # new_object.format(
                                #     class_label = label,
                                #     x_center = x_center,
                                #     y_center = y_center,
                                #     width = width,
                                #     height = height
                                # )
                            # )
                # output_file.close()
            # TRANSFORM
            # print( "TOTAL BBOXES: ", len(bboxes), bboxes )
            repeat = 1
            if Efflorescence:
                repeat = 8
                if Crack:
                    repeat = 4
            elif Spallation or ExposedBars or CorrosionStain:
                repeat = 3
                if (ExposedBars or CorrosionStain) and not Spallation:
                    repeat = 6
                    if ExposedBars and not CorrosionStain:
                        repeat = 10
                if Crack:
                    repeat = 2
            
            for i in range(repeat * number_of_copies):
                try:
                    
                    transformed = transform(image=image, bboxes=bboxes)
                    transformed_image = transformed['image']
                    transformed_image_height, transformed_image_width = transformed_image.shape[:2]
                    transformed_bboxes = transformed['bboxes']

                    # AND SAVE
                    transformed_image_name = "transformed_" + str(i) + "_" + image_id
                    transformed_image_name_wo_extension = "transformed_" + str(i) + "_" + id_wo_extension
                    path_new_image = os.path.join(output_images, transformed_image_name)
                    
                    cv2.imwrite( path_new_image, transformed_image )
                    
                    with open(join(output_labels, txt_extension.format(transformed_image_name_wo_extension)), "a+") as output_file:
                        
                        for defect in transformed_bboxes:
                            ## PASS TO YOLO FOMRAT:
                            # x_center = ( 2 * defect[0] + defect[2] ) / 2 / transformed_image_width
                            # y_center = ( 2 * defect[1] + defect[3] ) / 2 / transformed_image_height
                            # width = defect[2] / transformed_image_width
                            # height = defect[3] / transformed_image_height
                            x_center = ( defect[0] + defect[2] ) / 2 / transformed_image_width
                            y_center = ( defect[1] + defect[3] ) / 2 / transformed_image_height
                            width = ( defect[2]- defect[0] ) / transformed_image_width
                            height = ( defect[3] - defect[1]  ) / transformed_image_height

                            # RANGE LIMIT
                            output_file.write(
                                new_object.format(
                                    class_label = defect[4],#label,
                                    x_center = x_center,
                                    y_center = y_center,
                                    width = width,
                                    height = height
                                )
                            )
                        output_file.close()
                    np_transformed_bboxes = np.array( transformed_bboxes )
                    category_id_to_name = ["Crack", "Spallation", "Efflorescence", "ExposedBars", "CorrosionStain" ]
                    visualize(transformed_image, np.array( np_transformed_bboxes[:, :4], dtype=float), np.array( np_transformed_bboxes[:, 4], dtype='int') , category_id_to_name)
                except:
                    continue

BOX_COLOR = (255, 0, 0) # Red
TEXT_COLOR = (255, 255, 255) # White

def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    # x_min, y_min, w, h = bbox
    # x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    x_min, y_min, x_max, y_max = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=TEXT_COLOR, 
        lineType=cv2.LINE_AA,
    )
    return img


def visualize(image, bboxes, category_ids, category_id_to_name):
    import matplotlib.pyplot as plt
    img = image.copy()
    for bbox, category_id in zip(bboxes, category_ids):
        # print( category_id )
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name)
    plt.figure(figsize=(12, 12))
    plt.axis('off')
    plt.imshow(img)
    plt.show(block=True)