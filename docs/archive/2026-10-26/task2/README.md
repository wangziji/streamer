# Task 2：功耗、续航和电量测量定义（v2）

2026-10-26。此目录是修复VBUS连接检测判据后的Task 2独立快照，保留Task 1及设计上下文以便阅读。既有历史归档不作覆盖。

- [Task 2交付记录](docs/evidence/task2-2026-10-26/completion.md)
- [24分组功耗预算](docs/engineering/power-budget.csv)
- [能量与峰值计算](docs/engineering/battery-energy.md)
- [续航与VBUS分路径测量规程](docs/validation/runtime-protocol.md)
- [复核与P2修复记录](docs/evidence/task2-2026-10-26/review.md)
- [计算与来源验证结果](docs/evidence/task2-2026-10-26/calculations.json)
- [进展与后续门槛](docs/progress-2026-10-26.md)
- [源文件与归档摘要/链接转换](archive-manifest.json)

P2修复允许有官方依据、预算受限且与系统供电隔离的必要VBUS检测；任何向系统轨或电池供电仍失败。无法证明分路径电流/隔离或预算未冻结时记inconclusive，不允许仅从总电流减去名义检测预算来取通过。

本包算术和文档回归通过，硬件测试not_run，design_accepted/bench_passed/system_passed均为false。20行电流和全部路径效率仍是假设。没有采购、CAD修改、打样或续航实测；Task 3尚未执行。

原厂PDF、官方文档源文件、KiCad工程、XML网表及提取全文不在此快照。Markdown原厂资料链接转换为官方来源，原始版本/来源/摘要保存在各厂商manifest，后续电路设计须重新本地归档确切版本并核对SHA-256。证据及交付manifest中的源文件摘要仍标识本地原件，转换后文件以archive-manifest中的archive_sha256为准。验证脚本作为源码记录保留，依赖未携带的原件，不能直接在这个文档快照中声称重现完整基线验证。
