"""
    TODO
"""
import os
import xml.etree.ElementTree as et
from os import listdir
from os.path import isfile, join
import pandas as pd

def prepare_codebrim_yolo(path_images, path_annotations, output):
    """
        TODO

        groundtruth
    """
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

            for obj in xroot.iter("object"):

                with open(join(output, txt_extension.format(id_wo_extension)), "a+") as output_file:
                    bndbox = obj.find("bndbox")
                    x_center = int( bndbox.find( "xmin" ).text )
                    y_center = int( bndbox.find( "ymin" ).text )
                    width = int( bndbox.find( "xmax" ).text ) - int( bndbox.find( "xmin" ).text )
                    height = int( bndbox.find( "ymax" ).text ) - int( bndbox.find( "ymin" ).text )

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
