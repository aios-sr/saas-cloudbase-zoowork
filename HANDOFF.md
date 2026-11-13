# 文档仓库交接

## 当前范围

版本 0.3.0，分支 docs/online-guide。已将原开发技能改写为 GitHub 文档模式：README 作为产品人员与 Codex 的入口，docs 保存执行流程、前置检查、架构、ZooWork、Agent／业务 Skill、上下文及交付规则，templates 保存新项目文件。

已移除技能入口和调用元数据，不再要求安装或点名调用。本仓库原开发技能未安装到用户技能目录，无需卸载；ZooWork 运行时业务 Skill 机制保留。未修改来源客户项目、真实 Key 或云资源，未调用模型。

## 版本与上下文

规范版本保存于 VERSION。生成应用记录来源仓库、完整提交、版本与采用范围，并在项目内保存实际决定、前置证据和恢复点；后续会话不依赖原聊天或实时访问文档仓库。

## 发布目标与状态

已创建并核对 aios-sr/saas-cloudbase-zoowork 为私有 GitHub 仓库。远程默认 main 仅用初始化 README 建立 PR 基线；完整规范内容通过功能分支 PR 合并发布。README 是线上入口，不另部署网站。

本地文档、故障样例和两张图表检查通过。[发布 PR #1](https://github.com/aios-sr/saas-cloudbase-zoowork/pull/1) 记录检查、合并提交与私有在线读取结果，最终状态以 PR 为准；文档检查不代表生成应用已经上线。
