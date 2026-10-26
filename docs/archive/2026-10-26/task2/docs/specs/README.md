# 官方规格资料库

本目录是后续电路设计的唯一可信参考库。只归档原厂官方来源；厂商数据手册、应用说明、官方参考设计与勘误按各自适用范围使用。论坛、个人文章、分销商镜像、搜索摘要及模型记忆不得作为电路设计依据。此前在线调查文件仅保留为调查历史，涉及电路的结论须重新落到本地官方文件及页码后才能采用。

## 现有工程的核心器件

由 KiCad 保存文件导出网表确认，证据见 [预检查](../existing-design-preflight.md)。

| 位号 / 型号 | 本地完整规格 | 版本 / 页数 | 状态与限制 |
| --- | --- | --- | --- |
| U1 AK4191EQ | [Datasheet](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4191eq/ak4191eq-en-datasheet-myakm.pdf) | 200900053-E-01，130页 | 已归档；brief修订与完整手册不同，冻结前核清更新情况 |
| U3 AK4499EX | [AK4499EXEQ Datasheet](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4499exeq/ak4499exeq-en-datasheet-myakm.pdf) | 220600017-E-00，54页 | 已归档；完整订货号及物理引脚映射待接受 |
| U2 CCHD-957 | [Datasheet](https://www.crystek.com/specification/clock/CCHD-957.pdf) | Rev N，2页 | 已归档；频率及完整订货号尚未指定 |
| U4–U8 LT3045xDD | [LT3045 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/3045fa.pdf) | Rev D，32页 | 已归档；实际等级及订货后缀尚未指定 |

配套：[AK4191＋AK4499EX 应用说明 C018-01](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4191eq/ak4191eq-en-designtransition-myakm.pdf)，24页。Product brief 与质量规格为补充资料，不能代替完整电气规格。

## 候选与板级参考

- [XMOS XU316-1024 Datasheet](https://www.xmos.com/documentation/XM-015129-PC/pdf/XU316-1024.pdf)：候选 USB 接收芯片系列，尚未选定具体封装、速度等级及固件。
- [树莓派5产品简介](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-8-raspberry-pi-5-product-brief.pdf)、[机械图](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008347-DS-1-raspberry-pi-5-mechanical-drawing.pdf)、[RP1外设寄存器资料](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf)、[PCIe连接器规范](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008298-DS-1-pcie-connector-standard.pdf)：各自限于板级说明、机械或接口用途，不是完整主控芯片电气规格。PCIe不是本项目已选接口；不以该规范扩大功能范围。
- [树莓派官方电源章节源文件](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc)：官方文档仓库快照，来源和内容哈希见manifest；外链依赖未打包，仅用于其已覆盖的板级供电约束。
- [OPA1612](https://www.ti.com/lit/ds/symlink/opa1612.pdf)（Rev C，34页）、[TS3USB221A](https://www.ti.com/lit/ds/symlink/ts3usb221a.pdf)（Rev C，27页）、[STM32G0B1系列](https://www.st.com/resource/en/datasheet/stm32g0b1cb.pdf)（DS13560 Rev6，165页）：2026-10-23补充的完整官方候选规格；用途与限制见[评估](../control-analog-candidates.md)，尚未接受选型。

- [BQ25798完整手册](https://www.ti.com/lit/ds/symlink/bq25798.pdf)（SLUSDV2C，2026-06，151页）：2026-10-24归档，限于研究充电/电源路径概念及后续候选评估，不代表本项目已选该芯片；第39～40页§7.3.8说明系统电源选择、充电与电池补充供电。电池体系、串数、容量和充电控制均未确定。

归档复核：[校验报告](../evidence/specs-verification.json)。截至2026-10-24，共19个资料文件（18份PDF及1份官方文档源文件）的哈希与来源域名均通过复核，PDF页数与manifest一致。部分PDF存在可修复的格式警告，已在厂商manifest记录；不等于电气正确性已验证。

## 覆盖缺口与设计门槛

- 2026-10-25 Task 1补充6份原厂PDF，资料库现为24份PDF及1份官方文档源文件；本轮校验见[基线验证](../evidence/task1-2026-10-25/baseline-verification.json)，旧校验报告保留为历史。完整订货号、版本、关键页及符号/封装状态统一见[设计输入表](../engineering/design-inputs.md)。
- 电池比较方向：[RRC2054技术表](https://www.rrc-ps.com/fileadmin/Dokumente/Gen1/DS_RRC2054_E.pdf)（DS_RRC2054_E，2页）与[RRC2054-2数据表](https://www.rrc-ps.com/fileadmin/Dokumente/Data-Sheets/DS_RRC2054-2.pdf)（DS_RRC2054-2_J，7页，P/N 1100640）。均为精确包型的原厂技术资料，非系列brief；发布日期未标明，以内容哈希锁定。这两份尚不足以关闭全部集成、SMBus、放电/寿命和供货版本约束；不能把48Wh/17.4V与≥97.92Wh/16.80V两套参数混用，不能视为已选电池或续航达标。来源及限制见[RRC manifest](rrc/manifest.json)。
- 电源候选补充：[BQ76952](https://www.ti.com/lit/ds/symlink/bq76952.pdf)（SLUSE13B，87页）和[TPS55288](https://www.ti.com/lit/ds/symlink/tps55288.pdf)（SLVSF01B，55页）完整datasheet，仅用于保护监测与正向DC/DC参考比较。BQ76952配套TRM未归档；不自动增加自制BMS范围；负电源、隔离/阻断、欠压监控及模拟门控仍需准确选型和官方规格。
- MCU配套补充：[RM0444](https://www.st.com/resource/en/reference_manual/DM00371828-.pdf)（Rev6，2024-12，1384页）及[ES0548](https://www.st.com/resource/en/errata_sheet/es0548-stm32g0b1xbxcxe-device-errata-stmicroelectronics.pdf)（Rev4，2026-09，31页）。资料下载缺口关闭，实际芯片修订适用性、勘误规避与控制固件设计仍未验证。
- XMOS USB Audio User Guide 9.2.0于2026-10-25尝试官方版本PDF链接仍HTTP406，见[本轮检索](../evidence/task1-2026-10-25/retrieval.json)。指南/固定源码及依赖、配置覆盖与工具链缺口继续阻塞Task 5，不能因XU316 datasheet已下载而关闭。
- AKM完整手册与brief版本差异、AK4191 p54～55与p104 Unlock/BCKO行为差异尚未关闭；分别标识为D-AKM-REV、D-UNLOCK，并映射Task 5/6/7/8冻结门槛，见[具体依赖表](../engineering/design-inputs.md)。

- AKD4499EXEQ 评估板手册尚未取得，尝试的官方URL返回404；不能假设已验证其参考电路。
- AK4499EQ 为另一器件，完整官方手册本轮未取得；不是当前导出网表采用的型号，不得用EX资料替代其规格。
- XMOS USB音频软件资料的本地获取状态以 `xmos/manifest.json` 为准；芯片datasheet不证明任何固件已支持PCM768/DSD512。
- USB选择器、控制MCU、I/V/滤波运放、其他电源转换器及保护器件尚未选型。每个核心器件必须先确定准确型号、归档完整官方规格，再进入对应电路设计。
- 若板级公开资料不足以设计其电气接口，只能在已公开约束内使用现成模块，不能推定未公开芯片参数。

## 使用与更新规则

1. 各厂商目录 `manifest.json` 记录来源URL、最终URL、下载日期、修订、页数、SHA256和下载/验证状态。PDF格式版本与手册修订号分开理解。
2. 设计记录引用本地文件、手册修订和页码/章节；核心参数须核对测试条件、封装、等级、脚注及勘误。
3. 原始PDF保持不变；提取文本只是检索辅助，表格、脚注、引脚图和波形应回到PDF核对。
4. 更新资料时保留原版本与哈希，记录变更并评审对现有设计的影响。发现版本冲突先核清；无法获取完整规格时阻塞相关设计，不以brief或非官方材料代替。
5. 下载完成不是设计完成。现有符号、封装、连线、电源、时钟和保护均须另行验证。
