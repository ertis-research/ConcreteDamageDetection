# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.155.1/containers/python-3/.devcontainer/base.Dockerfile
FROM python:3.9.1-buster

RUN apt update
RUN apt install ffmpeg libsm6 libxext6 fastjar -y

RUN cd /tmp && wget https://www.rarlab.com/rar/rarlinux-x64-5.6.0.tar.gz \
    && tar -zxvf rarlinux-x64-5.6.0.tar.gz && cd rar \
    &&  cp -v rar unrar /usr/local/bin/

RUN pip install gdown
# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1