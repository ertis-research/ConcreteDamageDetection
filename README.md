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
# install requirements. Needed if not using .devcontainer or Docker Image
make start 
# Datasets and Weights, if not using Docker Image
make download # it also unzip files
```