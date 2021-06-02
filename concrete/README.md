# ConcreteDamageDetection

- [`numpydoc` docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Making a Python Package](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)
- [Upload to PyPi](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56)
- [Example of setup.py from Neptune alpha](https://github.com/neptune-ai/neptune-client/blob/alpha/setup.py)

# Requirements

## To use containerized version

Need to have a GPU, Docker, Windows installed. 

## To just test without containers

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
concrete prepare # creates groundtruth files (for codebrim at the moment)
```


# Training
```
python train.py --data ../data/codebrim.yaml --cfg models/yolov3.yaml --weights '' --batch-size 10 --log-artifacts --log-imgs 10 --epochs 10 --cache-images --multi-scale
```

# Test
```
python detect.py --save-txt --source ../datasets/CODEBRIM/images/test/ --weights runs/train/exp5/weights/best.pt --conf 0.25 --save-conf
```

# Another test
```
python test.py --weights .\runs\train\exp46\weights\best.pt --data ..\data\3-fold-codebrim-10-1.yaml --img 640 --task test --batch-size 8 --iou-thres 0.01
```

# Other chunks

Adding images to the used dataset:
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