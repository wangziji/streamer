## Build
docker build -t a14-4-tv:1.0 .  
## RUN
#### enter the image
docker run -it --privileged --name a14-4-tv -v /mnt/aosp/a14-4-kernal/kernal/boot:/output /mnt/aosp/a14-4-tv:/workspace a14-4-tv:1.0 /bin/bash
#### excute
cd /workspace
./build.sh
## ENABLE ADB
#### Clone ADB source code
```
git clone https://android.googlesource.com/platform/system/adb system/core/ad
```

#### Modify **BoardConfig.mk**
```
vim device/brcm/rpi4/BoardConfig.mk
```

add
```
# 启用adbd服务
BOARD_VENDOR_KERNEL_CMDLINE += ro.secure=0 ro.debuggable=1 persist.service.adb.enable=1 service.adb.tcp.port=5555
```

#### Modify **rpi4.mk**
```
vim device/brcm/rpi4/aosp_rpi4_tv.mk
```
add
```
PRODUCT_HOST_PACKAGES += adbd \
                        adb
```

#### Create **system.prop**
```
vim device/brcm/rpi4/system.prop 
```
add 
```
persist.service.adb.enable=1
service.adb.tcp.port=5555
ro.adb.secure=0
ro.debuggable=1
```