cd /workspace
# copy kernal
cp -f /output/boot/dts/broadcom/*.dtb ./device/brcm/rpi4-kernel/
cp -f /output/boot/Image ./device/brcm/rpi4-kernel/
cp -f /output/boot/dts/overlays/* ./device/brcm/rpi4-kernel/overlays/


. build/envsetup.sh

# lunch aosp_rpi4-ap2a-userdebug
lunch aosp_rpi4_tv-ap2a-userdebug

make bootimage systemimage vendorimage -j$(nproc)


bash /workspace/rpi4-mkimg.sh

cp /workspace/out/target/product/rpi4/RaspberryVanillaAOSP14-20241123-rpi4.img /output/