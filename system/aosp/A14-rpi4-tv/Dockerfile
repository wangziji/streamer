# Define base image.
FROM ubuntu:22.04

# AOSP enviroment: https://source.android.com/docs/setup/start/requirements?hl=zh-cn
# raspberry-vanilla:https://github.com/raspberry-vanilla/android_local_manifest/tree/android-14.0?tab=readme-ov-file
RUN apt update && \
    apt-get install -y git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 \
    x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig \
    bc coreutils dosfstools e2fsprogs fdisk kpartx mtools ninja-build pkg-config python3.10 && \
    ln -s /usr/bin/python3.10 /bin/python3 && \
    apt-get install -y python3-pip && \
    pip3 install meson mako jinja2 ply pyyaml dataclasses && \
    export REPO=$(mktemp /tmp/repo.XXXXXXXXX) && \
    curl -o ${REPO} https://storage.googleapis.com/git-repo-downloads/repo && \
    gpg --recv-keys 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65 && \
    curl -s https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ${REPO} && install -m 755 ${REPO} /bin/repo && \
    mkdir /workspace && cd /workspace && \
    curl -o .repo/local_manifests/manifest_brcm_rpi.xml -L https://raw.githubusercontent.com/raspberry-vanilla/android_local_manifest/android-14.0/manifest_brcm_rpi.xml --create-dirs && \
    repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r67 && \
    repo sync -j$(nproc)

COPY ./build.sh /workspace

RUN chmod +x /workspace/build.sh