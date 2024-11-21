export OUT_DIR=/output
echo "output dir is: $OUT_DIR"
. build/envsetup.sh

# lunch aosp_rpi4-ap2a-userdebug
lunch aosp_rpi4_tv-ap2a-userdebug

make bootimage systemimage vendorimage -j$(nproc)

cd $OUT_DIR

bash /workspace/rpi4-mkimg.sh