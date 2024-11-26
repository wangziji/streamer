## Build
docker build -t a14-4-kernal:1.0 .  
## RUN
#### enter the image
docker run -it --privileged --name a14-4-kernal -v /mnt/aosp/a14-4-kernal:/output a14-4-kernal:1.0 /bin/bash
docker run -it --privileged --name a14-4-kernal --mount type=bind,source=/mnt/aosp/test,target=/workspace,bind-propagation=shared a14-4-kernal:1.0 /bin/bash
#### excute
cd /workspace
./build.sh