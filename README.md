# Reinforced Concrete Bridge Defect Detection with Convolutional Neural Networks

> Thesis for the Master's degree in Computer Science - University of Malaga.
>
> **This work and its related code can be used for educational purposes only.**

The industrial sector has focused on monitoring structural health in order to anticipate and avoid high costs.
There are different ways of monitoring, such as monitoring based on computer vision.
Deep Learning concepts have been introduced to facilitates the comprehension of the work conducted throughout this project.
In this Master's Thesis, the Convolutional Neural Network in the current state-of-the-art, YOLOv5, has been proposed to detect and classify reinforced concrete bridge defects in real-time.
The dataset that has been used during the training and evaluation of this model is the CODEBRIM [[1]][[2]] dataset.
Different evaluations have been performed so as to find the best possible performance based on CODEBRIM annotations by optimizing the parameters and using ensemble modeling techniques and data augmentation.
After an exhaustive analysis of the results and the dataset used, poorly annotated images have been verified and have negatively affected the model training, and thus, the final YOLOv5 performance using CODEBRIM. However, considering this statement, the results are promising, requiring new datasets in this context to improve the performance shown.

### Test results with CODEBRIM

|Model |mAP@.5  | R@.5 | P@.5 | mAP@.05 | R@.05 | P@.05 | msec/image |
--- | --- | --- | --- | --- | --- | --- | --- 
|YOLOv3| 0.233 | 0.316 | 0.369 | 0.365 | 0.397 | 0.489 | 43.8 |
|YOLOv5s| 0.248 | 0.35 | 0.341 | 0.371 | 0.406 | 0.469 | 20.2 |
|YOLOv5s6| 0.247 | 0.323 | 0.369 | 0.379 | 0.379 | 0.494 | **17.7** |
| **YOLOv5x** | **0.255** | **0.357** | **0.376** | **0.387** | **0.4**  | **0.527** | 66.3 |
|YOLOv5-p2| 0.212 | 0.309 | 0.31 | 0.335 | 0.371 | 0.431 | 41.10 |

### Test results with CODEBRIM after Data Augmentation

|Model |mAP@.5  | R@.5 | P@.5 | mAP@.05 | R@.05 | P@.05 |
--- | --- | --- | --- | --- | --- | --- 
|YOLOv5s| 0.32 | 0.433 | 0.409 | 0.517 | 0.563 | 0.536 |
|YOLOv5s6| 0.314 | 0.391 | 0.461 | 0.534 | 0.551 | 0.584 |
| **YOLOv5x** | **0.357** | **0.443** | **0.486** | **0.561** | **0.574**  | **0.614** |

## Requirements

### To use containerized version

Need to have a GPU, Docker, Windows installed. 

### To just test without containers

Install `make`, `python`, `pip`. And `gdown` and `unrar` if you wanna use the datasets we use here.

```bash
python pascalvoc.py -gt ../datasets/CODEBRIM/labels/test -det ../yolov3/runs/detect/exp6/labels -sp ../data/results -gtcoords rel -imgsize 640,640 # object_detection
```

```bash
# install requirements. Needed if not using .devcontainer or Docker Image
make start 
# Datasets and Weights, if not using Docker Image
make download # it also unzip files
make develop
concrete prepare # creates groundtruth files
```

## Commands

### Training
```
python train.py --data ../data/codebrim.yaml --cfg models/yolov3.yaml --weights '' --batch-size 10 --log-artifacts --log-imgs 10 --epochs 10 --cache-images --multi-scale
```

#### Test
```
python detect.py --save-txt --source ../datasets/CODEBRIM/images/test/ --weights runs/train/exp5/weights/best.pt --conf 0.25 --save-conf
```

### Another test
```
python test.py --weights .\runs\train\exp46\weights\best.pt --data ..\data\3-fold-codebrim-10-1.yaml --img 640 --task test --batch-size 8 --iou-thres 0.01
```

### Other chunks

Adding images to the dataset using PowerShell:
```
# Declare array
$array = @( )

# move images
for ($i = 0; $i -lt $array.Length; $i++){ Move-Item -Path $array[$i] -Destination "datasets\CODEBRIM-20\images\train\" }

# Obtain filenames
$filenames = $array | Split-Path -Leaf 

# Obtain filenames without extensions
$filenamesnoext = @(); for ($i = 0; $i -lt $filenames.Length; $i++){ $filenamesnoext += $filenames[$i].Split(".")[0] }

# Move annotations
for ($i = 0; $i -lt $filenames.Length; $i++){ $temp = $filenamesnoext[$i]; Move-Item -Path "$temp.txt" -Destination "..\train" }
```


[1]: https://github.com/MrtnMndt/meta-learning-CODEBRIM
[2]: https://arxiv.org/abs/1904.08486
