# Android 主控与 USB 音频可行性调查

调查日期：2026-10-22。范围仅为公开一手资料核实；未安装镜像、连接硬件或验证 App。本文件为架构建议，不代表已批准平台选型。

## 结论

建议以树莓派 5 + 平板式 Android + 异步 USB 音频接收板作为首选验证路线。先通过现成 USB DAC 验证播放链路，再冻结自研接口。ROCK 5B 作为备选，但其厂商 Android 镜像不能自动消除重采样、App 兼容及音频 HAL 风险。

## 平台比较

| 候选 | 有文档支持的事实 | 尚未证明的能力 |
| --- | --- | --- |
| Raspberry Pi 5 | KonstaKANG 提供 2026-05-20 LineageOS 23.2/Android 16；维护者列音频、GPIO DAC、网络及触屏功能。镜像非 LineageOS 团队官方支持，部分组件限非商业使用 | 自研 UAC2 DAC 的兼容性、全部目标采样率、逐 App 输出采样率、bit-perfect、商业部署条件 |
| Raspberry Pi 4 | 同维护者提供 Android 16；可作为已有硬件复用候选 | 不能从 Pi5 结果推定 Pi4 音频/触屏/USB 稳定性相同，需单独测试 |
| Radxa ROCK 5B | 厂商下载页提供 Android 12 镜像及安装资料 | 未取得该镜像支持 Android 14 USB mixer API、bit-perfect 或全部目标音乐 App 的证据；需要检查实际 HAL、音频策略及 USB DAC |

来源：[Pi5 镜像维护者](https://konstakang.com/devices/rpi5/LineageOS23/)、[Pi4 镜像维护者](https://konstakang.com/devices/rpi4/LineageOS23/)、[ROCK 5B 官方下载](https://docs.radxa.com/en/rock5/rock5b/download)、[Radxa 软件支持矩阵](https://docs.radxa.com/en/software-support-matrix/rockchip)。

对本项目的推论：选择较新、文档完整且能实测通过的镜像，比仅比较 SoC 性能更重要。触摸操作优先验证平板式 Android；Android TV 仅作为另一路 UI 方案，不默认等价。

## Android 音频边界

Android 14 引入 USB preferred mixer attributes，App 可请求格式、采样率及 mixer 行为。普通路径默认可混音、调音量及应用效果；USB `BIT_PERFECT` 是可选能力，需要 AIDL 音频 HAL 和音频策略配合，并非安装 Android 14 以上即可获得。启用后要求链路不做重采样、缩放或混音，音量由硬件负责。[AOSP 官方说明](https://source.android.com/docs/core/audio/preferred-mixer-attr)

因此，App 可安装、歌曲可播放、DAC 显示高采样率和逐比特无修改是不同验收项。即使 DAC 显示 192kHz，也不能排除软件已先重采样。允许 DSD 转 PCM 不意味着要求该转换路径逐比特保真；必须显示实际转换和输出状态。

## USB 与外部电脑输入

Android 播放时主控为 USB host，DAC 接收板为 peripheral。外部电脑作为音源时同样为 host；不能把两个 host 直接接在一起。建议研究“单 USB 接收板 + host 选择器”和“双接收通道 + 数字音频选择”两种拓扑，切换时先静音、停止流并重新建立稳定时钟，再释放输出。具体器件、VBUS 隔离及切换时序尚未选定。

USB 异步音频允许接收端决定采样节奏，由 host 配合反馈；它是时钟架构依据，不是整体低噪声或低失真的保证。[AOSP USB 音频说明](https://source.android.com/docs/core/audio/usb)

## 冻结主控前的实机检查

1. 固定主板、镜像版本及摘要、显示与触控型号、USB DAC 固件；记录电源和散热条件。
2. 逐 App 验证安装、登录、音乐访问、连续播放和退出后的音频路由；逐项报告 DRM、认证及地区限制。
3. 用本地已知 PCM 测试文件覆盖 44.1/48/88.2/96/176.4/192kHz，记录源格式、HAL 输出及 DAC 接收状态；更高采样率作为独立能力验证。
4. 查询 USB mixer 能力和 HAL/策略配置；逐 App 检查是否实际请求并取得目标模式。必要时用数字捕获比较样本，不能仅凭界面图标断言 bit-perfect。
5. 测试通知声、另一个 App 抢占、插拔、格式切换、断网恢复和至少 24 小时播放。
6. 验证触屏、旋钮、手机辅助控制和安全关机；所有控制入口须使用统一的受限音量状态，Android 崩溃不能解除独立静音保护。
7. 验证外部 PC 输入、主控/PC 切换及主控关机后的 DAC 可用性；确认是否要求脱离 Android 独立工作。

只有完成上述检查，才能判定具体平台适合本项目；本次调查没有确认任何候选已达到音源全覆盖、768kHz/DSD512 或最终模拟验收指标。
