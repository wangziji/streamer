# Define base image.
FROM ubuntu22.04

# AOSP enviroment: https://source.android.com/docs/setup/start/requirements?hl=zh-cn
RUN apt update 
RUN apt-get install -y git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig

RUN apt-get install -y python3.10
RUN ln -s /usr/bin/python3.10 /bin/python3

RUN export REPO=$(mktemp /tmp/repo.XXXXXXXXX)
RUN curl -o ${REPO} https://storage.googleapis.com/git-repo-downloads/repo
RUN gpg --recv-keys 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
RUN curl -s https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ${REPO} && install -m 755 ${REPO} ~/bin/repo

# raspberry-vanilla:https://github.com/raspberry-vanilla/android_local_manifest/tree/android-14.0?tab=readme-ov-file
RUN apt-get install -y bc coreutils dosfstools e2fsprogs fdisk kpartx mtools ninja-build pkg-config python3-pip
RUN pip3 install meson mako jinja2 ply pyyaml dataclasses

RUN repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r67
RUN curl -o .repo/local_manifests/manifest_brcm_rpi.xml -L https://raw.githubusercontent.com/raspberry-vanilla/android_local_manifest/android-14.0/manifest_brcm_rpi.xml --create-dirs

RUN repo sync -j$(nproc)
RUN . build/envsetup.sh
RUN lunch aosp_rpi4_tv-ap2a-userdebug