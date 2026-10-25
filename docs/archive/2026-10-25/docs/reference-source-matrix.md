# DMP-A6 Gen 2 音源对标与验证矩阵

核查日期：2026-10-22。对标对象为普通版 DMP-A6 Gen 2，不使用 Master 版或其他型号的独有功能补齐。

## 已确认的项目边界

- 音源支持以“可访问、可播放”为基本目标，允许通过 Android App 实现；不因此承诺与 Eversolo 相同的原生整合、跨服务音乐库或遥控体验。
- Roon Ready、各类 Connect 等认证/合作服务逐项报告实现路径和验证结果；安装同名 App 不等于实现该服务的设备级接收功能。
- 不做机内 SSD；保留 USB DAC 输入；排除光纤、同轴及 HDMI ARC 输入。
- USB 光驱播放/抓轨和蓝牙尚待用户显式确认，当前不是必选项。
- 下表全部是参考设备证据与本项目待验证项，**本项目尚无已验证实现**。

## 证据等级

- **确认**：官方手册、官方商店正文、型号对应固件日志或官方公告直接支持。
- **搜索索引**：官方旧产品页的搜索结果保留规格，但当前页面动态加载，尚未重获完整正文；待复核，不作为完成验收的唯一证据。
- **未核实**：本轮未取得普通版可靠官方型号证据；不代表设备一定不支持。

## 音源与接入方式

| 对标项 | 参考设备证据 | 本项目边界 / 后续验证 | 实现状态 |
|---|---|---|---|
| TIDAL、Qobuz、HIGHRESAUDIO、Presto Music、Radio Paradise | 确认：官方商店描述定制集成 [S1] | 允许 App 路径；分别验证登录、浏览、播放和切歌，记录实际音频格式 | 未验证 |
| Amazon Music、IDAGIO、Calm Radio、Internet Radio、TuneIn、Deezer、SoundCloud、Apple Music* | 搜索索引：普通版规格 [S2]；手册列 Amazon Music [S4] | 逐项复核参考范围；App 可播放与原生整合分开记录；Apple Music 星号含义未核清 | 未验证 |
| QQ音乐、网易云音乐、汽水音乐 | 确认：普通版固件日志包含播放相关修复 [S3] | 验证实际可用版本、账号区域、播放及输出；不推定所有区域均可用 | 未验证 |
| SMB、NFS、WebDAV、UPnP | 确认：官方商店 [S1] | 验证发现/手动连接、鉴权、文件浏览、播放、断线恢复及库扫描 | 未验证 |
| OneDrive、Dropbox、Emby、Plex | 搜索索引：普通版规格 [S2] | 先复核参考设备支持方式，再验证本项目客户端登录与实际播放 | 未验证 |
| USB 外置存储与本地音乐库 | 确认：手册及商店支持本地/外部存储与音乐库 [S1][S4] | 验证选定文件系统、扫描、标签、封面及曲目播放；机内 SSD 排除 | 未验证 |
| DLNA | 确认：手册及固件日志 [S3][S4] | 明确接收/浏览角色，验证发现、播放队列和连续播放 | 未验证 |
| Roon Ready | 确认：手册列该服务 [S4] | 单列认证/授权可行性；一般网络播放或 App 不能替代 Roon Ready 声明 | 未验证 |
| Spotify Connect、TIDAL Connect | 确认：普通版固件日志 [S3] | 单列设备接收路径、合作/认证依赖；验证手机发现、接管与持续播放 | 未验证 |
| Qobuz Connect | 确认：官方公告覆盖 DMP 系列且提及通过认证 [S5] | 单列接收方案与认证依赖；普通 Qobuz App 播放不代表 Connect 已实现 | 未验证 |
| HUAWEI HiPlay | 确认：普通版固件日志 [S3] | 单列平台依赖、设备发现与投播验证；不据此扩展本项目多声道输出范围 | 未验证 |
| LMS | 确认：普通版固件日志提及修复 [S3] | 尚需核清参考设备角色及协议；不能直接推定等同 Squeeze Connect | 未验证 |
| USB DAC 输入 | 确认：官方手册 [S4]；新旧资料 USB-C/USB-B 标注有差异 | 保留需求；确定物理连接器、USB 设备角色与目标主机后做实机输入验证 | 未验证 |
| 外接 USB 光驱播放/抓轨 | 确认：官方商店与固件日志 [S1][S3] | 待用户确认范围；尚未列为必选 | 未验证，范围待确认 |
| 蓝牙音频输入 | 确认：官方商店 [S1] | 待用户确认范围；商店 SBC/AAC 与旧手册更广编码列表有差异，编码能力需另核 | 未验证，范围待确认 |
| 光纤、同轴、HDMI ARC 输入 | 确认：官方手册/商店 [S1][S4] | 已排除，不增加接收电路 | 未实现，范围外 |
| 机内 SSD | 确认：官方手册/商店 [S1][S4] | 已排除 | 未实现，范围外 |

## 未核实项

AirPlay 的具体版本、Jellyfin、JPLAY、NAA、Squeeze Connect：本轮未获得普通版充分的官方型号证据。其他 Eversolo 型号或品牌级页面的能力不自动加入本项目必选清单。

## 后续验证记录要求

每个纳入项记录：硬件/Android 镜像版本、App 或接收软件版本、服务区域与订阅前提、接入方式、测试曲目格式、实测输出格式、通过步骤及限制。记录结论使用“未验证 / 已通过 / 失败 / 依赖外部条件”，失败不得以另一种接入方式静默替代。避免保存账号、令牌和原始认证日志。

## 官方来源

- **[S1]** [DMP-A6 Gen 2 官方商店页](https://shop.eversolo.com/collections/eversolo-products/products/eversolo-dmp-a6-gen-2-hi-fi-music-streamer-wireles-audio-player-digital-music-streamer-dac-music-service-streaming-dsd512-eos-audio-engineer-pcm768khz-32bit-bluetooth-5-0-exclusive-app)：原生/第三方应用、网络协议、本地库、光驱和蓝牙等。
- **[S2]** [普通版官方旧产品页](https://www.eversolo.com/Product/cert/model/DMP-A6/target/7abWHw%2B%2BoHhKKmVViAFMcQ%3D%3D.html)：本轮完整清单仅通过官方页面搜索索引获得；当前跳转至动态页面。
- **[S3]** [普通版官方固件下载与更新日志](https://www.eversolo.com/zh/downloads/dmp-a6-gen-2)：可见 OTA V1.6.15（2026-09-18）及历史版本，支持国内服务、投放、CD 和网络功能的型号级核查。
- **[S4]** [DMP-A6 Gen 2 官方用户手册 v1.0](https://music.eversolo.com/dmp/instruction/EVERSOLO-DMP-A6-Gen2-User-Manual-v1.0.pdf)：规格、外置存储、输入与 APK 安装。老手册不等于当前固件功能全集。
- **[S5]** [官方 Qobuz Connect 公告](https://blog.eversolo.com/2025/05/eversolo-announces-that-all-hi-fi-equipment-in-the-dmp-and-play-series-are-now-compatible-with-qobuz-connect-the-new-feature-that-simplifies-and-enhances-the-listening-experience/)：2025-05-16 公告 DMP/Play 系列支持及认证信息。
