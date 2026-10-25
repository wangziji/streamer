# 家用流媒体播放器 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将已讨论的整机方向与已批准的电池优先策略落实为可验证的电源、播放、音频及结构设计，并以完整实测完成验收。

**Architecture:** Android现成主控经USB接入独立音频子系统，独立MCU负责音量、静音和模式控制。正常播放由电池供电，低电量允许充电输入参与供电；电脑USB仅传音频，主控关闭时电脑DAC仍可工作。KiCad工程先审核再修改，核心器件先取得本地官方完整规格。

**Tech Stack:** KiCad 10.0.7/CLI、Konnect、Blender、Android候选平台、官方PDF；计算与证据使用CSV/JSON及Markdown，测量使用具备足够残余性能的仪器。

**Spec:** [整机提案（包含2026-10-24电池修订）](../specs/2026-10-23-streamer-design.md)、[需求记录](../../design-clarifications.md)、[音频验收基线](../../audio-acceptance.md)。

## Global Constraints

- 首版整机预算10000元，包含再次打样；功放、音箱及通用测试仪器另计。旧预算未包含电池，不能直接复用为成本通过证据。
- 屏幕常亮、正常播放纯电池续航至少1小时；60～80Wh仅为试算区间，不是选型或续航保证。
- 插电不自动旁路电池；纯电池播放须验证充电功率路径确实断开；低电量充电播放允许输入参与系统供电。电脑USB不为整机供电或充电。
- XLR最终最低SNR ≥123dBA、THD+N ≤0.0002%；目标≥128dBA、≤0.0001%；纯电池和充电播放均验证，未达标不得自动降级。
- 支持XLR/RCA选择输出、纯后级直连；主控关闭时电脑DAC、旋钮音量与静音独立可用。
- 最大外形300×250×120mm，打印单件≤200×200×200mm；内置电池后重新评估空间、固定和温升。
- 核心电路只依据本地原厂完整规格，记录页码/章节及版本；缺资料阻塞对应设计，禁止论坛、镜像或搜索摘要替代。
- CAD修改只通过Konnect；每次修改有保存、查询/导出及适当ERC/DRC证据。本目录尚无Git元数据，禁止凭空运行提交或创建仓库；先确定实际版本管理位置。
- 当前批准记录只确认已呈现的设计/电池策略进入规划；未证明具体料号、完整电路、采购、接纯后级或生产打样已获准。
- 本文件是总集成计划；软件固件、完整电源电路和PCB实施在接口及详细设计关闭后，各自形成可审核子计划。不预写未经选型的固件工程或分支。

## Review Focus

1. 充电禁止位已设置但适配器仍经SYS供电：纯电池状态须有电流路径证据（Task 3、9）。
2. MCU/AK4191硬复位后0dB输出：模拟静音须持续至限值重新配置及验证（Task 6、9）。
3. 主控断电被USB/UART反灌，或PC模式误因主控失联静音：模式和电源域必须分开验证（Task 5、6、9）。
4. 电池余量不足、电池包/BMS突然切断或供电路径失效导致I/V晚于EX失电：保护关机与真正失电都须满足时序，拔适配器不能替代电池侧故障注入（Task 2、3、6、9）。
5. 满幅指标合格但低音量底噪/充电切换爆音不合格：完整模拟路径、模式转换及实际机壳均需测量（Task 6、7、9）。

---

## 文件与执行边界

`docs/engineering/`存放各工程包的计算、接口和设计；`docs/validation/`存放测试规程；`docs/evidence/`存放实际导出和测试记录。所有新路径均是计划输出，未执行时不得标为存在或通过。设计审核通过记为`design_accepted`，评估台架通过记为`bench_passed`，整机验收通过记为`system_passed`；状态与证据版本一起传递，禁止以设计计算通过替代实测。Task 2的续航实测条件由Task 9执行，不作为Task 2计算交付的前置条件。

前置顺序：Task 1 → Task 2计算 → Task 3设计审核；Task 4的平台基础验证可在器材具备后单独执行。Task 5A接口设计使用Task 3设计和Task 4基础USB播放证据；Task 6控制设计消费Task 5A，之后Task 5B按Task 6设计准备评估硬件和最小固件并实测，不反过来要求Task 5B先通过才能设计Task 6。Task 7消费Task 3和Task 6的设计产物。Task 4涉及自研控制的集成检查待Task 5B完成，不能作为Task 5A的前置条件。Task 8原理图可消费相关`design_accepted`产物，最终PCB冻结另需Task 5B的接口台架证据。Task 9入口是已通过制造/装配及上电前检查、获准限流首次上电的样机，不要求样机预先通过Task 9自身的调试或验收。Task 10汇总全部结果。实际硬件不可用时可继续资料和计算，不伪造实测，不跨越所缺门槛。

### Task 1: 需求、资料与现有工程基线

**Files:** 修改`docs/design-clarifications.md`、`docs/specs/README.md`；创建`docs/engineering/traceability.csv`和`docs/engineering/design-inputs.md`；需要时更新`docs/evidence/`导出与来源记录。

**Interfaces:** 输入现有提案、网表和官方manifest；输出需求编号`R-POWER-01`（电池优先）、`R-RUNTIME-01`（≥1小时）、`R-AUDIO-01`（最低模拟指标）、`R-PC-01`（独立电脑模式）、`R-SOURCE-01`（音源矩阵）、`R-MECH-01`（尺寸）以及逐条验证包映射。

- [ ] 确认保存的CAD哈希是否仍与`netlist-provenance.json`一致；不一致时重新导出并记录差异，不覆盖旧证据后冒称未变化。
- [ ] 对每个核心器件建立完整订货号、规格版本、页码、符号与封装状态表；补齐电池、充电/保护、DC/DC等候选资料，不把系列brief当确切型号规格。
- [ ] 将XMOS软件指南、ST参考手册/勘误、AKM版本差异和Unlock行为矛盾列为具体依赖；分别指定被阻塞的后续任务。不能因下载一份datasheet就关闭固件资料缺口。
- [ ] 逐条映射需求、产物、测试及当前状态；原型调试线和最终线分列。确认蓝牙/光驱/Trigger等范围是否被实际批准，未批准则保留待决，不静默删除音源目标。

**Pass:** 每条需求有负责包；每个核心候选有准确资料状态；导出来源可追溯。此包不作电路正确性结论。

### Task 2: 整机功耗、续航和电量测量定义

**Files:** 创建`docs/engineering/power-budget.csv`、`docs/engineering/battery-energy.md`、`docs/validation/runtime-protocol.md`。

**Interfaces:** 输入Task 1器件资料及可用台架；输出每轨字段`rail, voltage_V, idle_A, playback_A, peak_A, evidence_kind, source_page, efficiency_basis, power_W`。`evidence_kind`只用`measured/manufacturer_bound/assumed`，假设不能作为实测通过证据。

- [ ] 分别核算控制域、主控、屏幕背光、USB桥、时钟、AKM、I/V和输出域；区别典型功耗、能力上限及峰值，避免将USB外设功耗重复算入主控输入。
- [ ] 用`E_nom >= P_load_avg × 1h / (eta_path × usable_fraction × retention_fraction)`计算能量需求；若`usable_fraction`已包含老化则不再重复乘`retention_fraction`。标明截止线、关机储能、温度和电池老化条件。
- [ ] 核算`I_bat_peak >= P_load_peak / (V_bat_min × eta_min)`，并检查电池包、BMS、连接器、线束和转换器限制；不能只验证Wh。
- [ ] 定义续航测试：固定屏幕常亮及亮度、网络、音源、输出负载和环境，充满后断开充电功率路径，从可播放至受控关机前计时；原始输入功率/各轨、电池电压电流与事件日志留存。

**Checks:** 仅作算术检验的30W/85%/80%示例应得44.12Wh，40W对应58.82Wh；这些值不是本机负载。整机通过要求实际播放≥3600秒且期间无欠压重启、提前掉音或借用外部电源；老化余量用可追溯电池规格或实测支持。

### Task 3: 电池、充电路径和热预算设计包

**Files:** 创建`docs/engineering/battery-power-design.md`、`docs/engineering/power-state-table.csv`、`docs/engineering/power-bom.csv`、`docs/validation/power-transition-protocol.md`；核心规格加入`docs/specs/<manufacturer>/`及manifest。

**Interfaces:** 输入Task 2的能量、峰值和各轨预算；输出准确电池包、充电器和保护候选比较、原理框图、全部电流路径、各模式阈值/单位/误差/滞回/时间参数、充电及续航预算。

- [ ] 比较至少两种有完整原厂规格的成品电池包方向，以全工作电压范围、Wh、允许充放电电流、温度、均衡/保护、寿命、尺寸和价格筛选；不按任意裸电芯数量先定包。
- [ ] 对纯电池、充电播放、停止播放充电、无电源低电关机、空电池插电及故障分别画电流路径；核查候选充电器在禁充、待机、失控和断电状态是否仍向SYS送电。需要真正阻断的路径单独选器件并归档规格。
- [ ] 根据电池规格及实际负载确定SOC/电压阈值、滞回和最短驻留时间；不只按瞬时电压判断SOC。定义监测失效、温度越界、异常电芯和充电器不可用时的行为。
- [ ] 计算`P_input >= P_system_in_charge_mode + P_stored_charge/eta_charge`，分别核算转换器、充电器及电池发热。不得将标称充电电流视为净入电池功率。
- [ ] 对长期插电播放计算周期和电池优先占比：`f_battery = P_stored_charge_net / (P_stored_charge_net + P_battery_draw)`为稳态简化模型，需说明两模式能量窗口一致及损耗边界。报告所选充电功率下的占比，不能未经计算承诺“绝大部分时间”纯电池。占比目标和寿命/温升取舍交用户审核。
- [ ] 定义电流测量、噪声、供电切换及直接拔适配器测试；提出最坏负载下关机所需时间和储能，验证I/V先于EX失电。不得靠BMS硬切断完成日常关机。
- [ ] 单独分析电池包/BMS意外切断、包连接器脱落、充电输入和电池同时不可用、板内供电路径失效；设计其局部储能、受控放电/钳位或其他有官方依据的保护策略，证明真正失电时仍满足EX与I/V约束。测试规程指定可控断开装置、假负载、断点、最坏负载和各轨示波捕获；禁止用故意过放、短路或损坏电池触发故障。依据本地[AK4499EX手册第29页§9.7](https://www.akm.com/content/dam/documents/products/audio/audio-dac/ak4499exeq/ak4499exeq-en-datasheet-myakm.pdf)。

**Pass:** 用户可审核的完整电源包、带电池的新总BOM预算≤10000元、阈值与故障表可执行。通过评审后才进入具体电源原理图；当前BQ25798仅为参考候选，不默认适配全部要求。

### Task 4: Android、屏幕和逐音源台架

**Files:** 使用`docs/platform-validation-plan.md`和`docs/reference-source-matrix.md`；创建`docs/evidence/platform-run-<date>/manifest.json`、`source-results.csv`、`audio-path-results.csv`和`capacity-results.csv`。

**Interfaces:** 输入可用主板、屏幕、合规电源、现成USB DAC及服务权限；输出固定版本/摘要的配置与逐项通过、失败、依赖外部条件的结果，不直接冻结自研硬件。

- [ ] 先记录现有器材与缺件清单，形成有型号和报价的采购候选供审核；本计划不授权购买或覆盖已有启动盘。
- [ ] 按既有P0～P5验证主板、镜像、屏幕、App、存储/缓存、网络重连及全部音源；安装或刷写前确认具体介质与数据影响。
- [ ] 逐源记录实际输出采样率；要声明bit-perfect时提供数字捕获/可比对样本，不能用DAC显示图标代替。DSD转PCM路径明确记录转换。
- [ ] 验证24小时播放、通知抢占、音源退出、热插拔及手机基本控制；输出容量、屏幕与主板的选择证据。

**Pass:** 必需音源均有独立结论及可重放步骤；未实现项经用户接受或继续处理，不能用另一App成功覆盖。缺器材时本包保持未执行，其他资料包可继续。

### Task 5: USB接收、选源及时钟接口冻结

**Files:** 创建`docs/engineering/usb-clock-interface.md`、`clock-matrix.csv`、`power-off-interface-matrix.csv`、`docs/validation/usb-clock-protocol.md`、`docs/superpowers/plans/2026-10-25-usb-clock-bench.md`和`docs/evidence/interface-bench-<revision>/`。

**Interfaces:** Task 5A消费Task 1、Task 3的`design_accepted`电源约束、Task 4的平台基础USB播放证据及本地AKM/XMOS/TI规格，输出时钟频率/主从/电平、USB固件版本、选源/枚举时序及器件候选。Task 5B另消费Task 6的`design_accepted`控制接口，输出评估台架和`bench_passed`接口证据；不要求预先具备Task 8整机PCB。

- [ ] 先取得官方USB音频固件资料或官方源码固定版本；核实384kHz以上及DSD512的实现覆盖，不从XU316规格推断软件已支持。
- [ ] 比较AKM Case2共同基准同步与Case1本地异步输入，选择一条并填写USB反馈、BICK/LRCK、AK4191 MCLKI、EX MCLK的完整关系；两颗AKM时钟保持官方同步关系。
- [ ] 对内置主控/外部PC的数据选择及VBUS检测、反灌、拔插、两个主机同时接线做状态表；TS3USB221A不承担VBUS或隔离功能。
- [ ] 完成Task 5A设计审核并将接口版本交给Task 6；此时只记`design_accepted`，不宣称双主机切换、时钟或保护已经实测通过。
- [ ] 接口包实施者负责Task 5B台架：提交列有确切型号、接线、电平、供电、原厂规格和仪器的USB桥、AKM/时钟评估硬件、USB选择载体及MCU开发板清单；独立临时载板需要另附可审设计。消费Task 6接口，编写上述台架子计划，限定最小固件仅做选源、时钟配置、状态读取和静音控制。审核设计和子计划、解决缺件授权后才准备硬件与固件；不能用现成USB DAC成功代替此台架。
- [ ] 在Task 5B台架上执行Android关电、音频关电、PC接线、充电/电池供电边界的组合测试，验证无反向供电、稳定枚举、格式/时钟关系及静音控制。评估板未覆盖的真实电池转换、模拟瞬态及最终布局记为未验证，交Task 9；最小固件与接线版本随证据保存。

**Pass:** Task 5A以资料齐备且完整接口可审核交付为设计通过条件；Task 5B另以评估硬件及最小固件实际测试通过为条件，任一未通过不得写为整体接口已验证。Task 8开始相关原理图需Task 5A；最终PCB冻结需Task 5B的关键选源/时钟证据。缺可用载体时明确阻塞Task 5B，不把首次验证挪到最终整机板后隐性放行。不支持的格式明确上报，不增加GPIO第二路径绕过问题。

### Task 6: 音量、保护与电源控制详细设计

**Files:** 创建`docs/engineering/control-protocol.md`、`control-state-machine.csv`、`fault-response-matrix.csv`、`docs/validation/control-fault-protocol.md`。审核后另建MCU/Android子计划，当前不生成未选工具链的产品代码。

**Interfaces:** 统一状态字段`mode, active_input, volume_db, volume_limit_db, muted, power_state, battery_state, fault_code, sequence_id, protocol_version`；命令包括`SET_VOLUME, SET_MUTE, SELECT_INPUT, REQUEST_SHUTDOWN, GET_STATE`，请求/实际状态分离，单位和无效值在协议中固定。

- [ ] 明确旋钮、Android和USB主机请求的权限、主音量唯一权威、上限及初始化策略；DSDD=1不可通过普通界面开启。
- [ ] 以独立MCU复位、AK4191 PDN复位、坏配置、读回失败、卡总线及失锁为输入，写默认模拟静音和恢复条件；不依赖单一BCKO停振判断失锁。
- [ ] 区分PC独立模式允许Android关机与内置播放模式失联；验证PC模式不被主控缺心跳永久静音，且音频/MCU故障仍受保护。
- [ ] 把Task 3电池低电和硬件欠压时序接入控制状态机；故障测试先接假负载，不接纯后级。升级和恢复流程始终保持模拟输出禁止。

**Pass:** 所有故障有触发证据、输出状态、恢复条件和测试步骤；具体启动上限、DC/瞬态限值须结合后级兼容设计先定后测，未闭合不放行直连后级。

此处交付首先为`design_accepted`控制设计，供Task 5B评估台架最小固件使用。Task 6不等待Task 5B先通过才开始设计；其控制行为在Task 5B进行接口级检查，完整保护在Task 9实测，分别留存状态。

### Task 7: I/V、滤波、输出和完整模拟验收条件

**Files:** 创建`docs/engineering/analog-design.md`、`analog-budget.csv`、`docs/validation/analog-protocol.md`；更新`docs/audio-acceptance.md`的已审核测试条件。

**Interfaces:** 输入AKM本地规格、OPA1612候选资料、Task 3各轨及Task 6门控；输出反馈/滤波计算、直流/峰值/噪声/稳定性预算、输出负载与完整测试规程。

- [ ] 从EX电流输出和官方I/V示例开始核算共模、峰值、差分合成及4Vrms XLR/2Vrms RCA提案；OPA1612官方推荐不替代本机稳定性或失真验证。
- [ ] 对数字音量＋模拟门控评估满幅及−20/−40/−60dB残余噪声和匹配；若不合格，在布局前比较模拟/混合衰减并更新设计，不能打样后才默认接受降级。
- [ ] 冻结10kΩ负载、1kHz THD+N、20Hz～20kHz带宽及计权条件，明确SNR防自动静音测法；同时定频响、串扰、输出阻抗、DC偏置和开关瞬态限值以及测量不确定度处理。
- [ ] 分别规定XLR差分/必要的单端输出阻抗、RCA输出阻抗随频率的限值及允许负载范围，不只定义10kΩ单点。冻结负载法或小信号注入法的接线、信号幅度、频点、计算及不确定度；采用两负载法时记录准确负载与电压，以线性Thevenin模型求等效阻抗并核查模型适用性。验证最小允许负载下摆幅、失真和稳定性；测试限值在测量前确定。
- [ ] 设计纯电池、插电但充电路径断开、充电播放和切换过程的同条件对比；所选模拟门控须纳入信号路径测量，不只测门控之前。

**Pass:** 测量条件及全部直连后级相关限值可执行且被审核；无仪器证据时只标设计计算通过，不能宣称模拟性能实测通过。

### Task 8: 原理图、PCB与电池结构集成

**Files:** 审核后通过Konnect修改实际`AK4499.kicad_sch/.kicad_pcb/.kicad_pro`及必要库；创建`docs/engineering/pin-package-map.csv`、`docs/validation/design-review.md`。结构文件计划为`mechanical/streamer-enclosure.blend`和`mechanical/assembly-notes.md`。

**Interfaces:** 原理图消费Task 3、Task 5A、Task 6、Task 7的`design_accepted`接口和电路计算；最终PCB冻结另须Task 5B接口台架证据。产出源工程、符号/封装对照、可渲染图和制造评审包。分板/子页实际名称在正式CAD子计划中固定，不在未知项目层级上直接批量新建。

- [ ] 逐器件建立官方物理引脚—符号—封装pad映射，区分顶/底视图、散热焊盘、重复电源脚；验证后再布局布线。
- [ ] 先完成电源、控制/保护、数字音频、模拟输出的集成原理图及独立评审；保存后跑ERC、导出网表和渲染，逐项处理或解释剩余问题。
- [ ] 用真实主板、屏幕、电池和连接器包络确定板形、安装孔、散热和分件；验证电池固定及线束磨损风险，禁用未核实的占位模型冻结外形。
- [ ] 完成受控布局与布线，保存后DRC、机械装配和生产检查；制造包的Gerber/BOM/坐标与同一源版本绑定。

**Pass:** 无未处理的阻断性电气/制造/机械问题，完整源文件可恢复，评审记录和生产包可追溯。输出制造包不等于提交订单。

### Task 9: 样机分阶段上电、故障和整机验收

**Files:** 创建`docs/evidence/bringup-<revision>/`、`docs/evidence/acceptance-<revision>/`，含`manifest.json`、原始测量、时序捕获和逐项结论；更新各验证规程执行状态。

**Interfaces:** 消费已通过制造/装配及上电前检查、获准限流首次上电的样机和Task 2～7规程；样机的电气调试、故障测试与整机通过由本任务建立，不作为其入口。输出可重现通过、失败或无法验证记录。

- [ ] 限流分域上电，先检查短路、各轨及失电状态，再验证时钟、数字数据、假负载模拟输出；禁止直接以功放/音箱作为初次调试负载。
- [ ] 实测电池路径电流，确认插电禁充状态不会暗中由SYS供电；测试插拔、低电转充、恢复纯电池、MCU硬复位、AK4191硬复位、Android关电及异常适配器断电。
- [ ] 在假负载与可控断开装置下，分别模拟电池包/BMS意外断开、包连接器脱落、全部输入丢失和已识别的板内供电路径失效；按Task 3已审核策略用限流电源/等效电池源进行受控故障注入，禁止过放或短路真实电池。记录I/V正负电源、EX供电/参考、模拟门控与输出的同步波形，验证储能/钳位/时序及瞬态；适配器拔插证据不能替代真正失电证据。
- [ ] 按冻结规程测纯电池及充电播放的XLR最低线、目标差距、RCA、低音量、XLR/RCA输出阻抗及允许负载范围结果；保存各频点负载/注入条件与原始电压数据。模拟门控、线缆、最终机壳、屏幕/网络/充电负载全部纳入。
- [ ] 运行≥3600秒屏幕常亮纯电池续航、24小时初步稳定性及72小时最终运行；重复切换的次数须执行前冻结并全部留证，不能用单次成功覆盖循环试验。

**Pass:** 最低模拟线与续航均通过，故障测试及其他冻结指标无阻断；仪器残余不足、关键测试缺失或任何失败均不签署整机通过，记录整改并回归对应包。

### Task 10: 总集成复核与交付

**Files:** 创建`docs/delivery/acceptance-summary.md`、`docs/delivery/revision-manifest.json`，汇总BOM、系统镜像/固件构建与烧录说明、CAD/结构源和全部证据的路径及摘要。

**Interfaces:** 消费Task 1～9结果；输出用户可验收的整机版本，已知限制与未实现音源逐项显式列出。

- [ ] 回查`traceability.csv`的每条需求，所有通过声明必须指向实际记录和同一硬件/固件版本。
- [ ] 核对一万元预算实际支出及剩余修板余量，记录电池更换、充电、运输/存放相关原厂约束和维护入口。
- [ ] 进行整机独立复核，修复阻断项后只回归受影响包；再交用户验收，不以本地计算、芯片典型指标或资料下载代替样机证据。

**Pass:** 用户能依据资料复现版本、理解限制并验收；未验证或未完成项保留真实状态，不以文档齐全标记产品完成。

## 执行记录与版本管理

每包完成后记录输入版本、改动、验证和剩余依赖。若用户指定的Git工作副本已确认，则每个独立工程包提交一次；在此之前保留文件及哈希证据，不初始化仓库或推送。计划选择执行方式并审核后，优先执行Task 1～3的资料/计算部分；缺硬件项挂在对应包，能独立推进的官方资料与只读检查继续。

## 计划自查（2026-10-25）

- 规格§1～3→Task 1、4、5、8；§4～5→Task 5～7；§6→Task 2、3、8、9；§7→Task 1、3、5～7；§8→Task 4、6；§9→Task 7、9、10；§10→Task 3、10；§11待决→Task 1；§12→本计划及各详细子计划。
- Review Focus五项均落到指定包的明确检查步骤，未使用“适当验证”等空泛通过条件。
- 所有任务只将已有本地资料作为事实；报价、容量、芯片冻结、器材可用和实测均未预先宣布完成。
- 未编造软件框架或测试命令；工程计算和实物验证按本项目类型定义，不为文档修改搭建无用测试框架。

## 独立审查修订记录（2026-10-25）

初审发现1项P1、2项P2；用户要求修正后，由同一独立reviewer只读复核，三项均在计划层面关闭，未发现新增阻断性循环依赖：

- 电池侧真正失电：Task 3定义保护策略，Task 9要求受控断开、假负载和同步波形，不能以拔适配器或损坏真实电池代替。
- 评估台架与入口：分开`design_accepted / bench_passed / system_passed`；明确Task 5A→Task 6设计→Task 5B载体及最小固件，首次上电不再要求预先通过自身验证。
- 输出兼容性：Task 7定义XLR/RCA输出阻抗、允许负载及测法，Task 9保存对应实测数据。

复核只确认计划覆盖与依赖闭合，不代表硬件测试通过，也不是采购、通电接后级或打样放行。修订过程中未改动CAD。
