# 仓库协作约定

使用简体中文。先读 README.md、skills/saas-cloudbase-zoowork/SKILL.md 和 docs/VALIDATION.md。本仓库仅维护供 Codex 开发 SaaS 的通用 Skill，不承载具体 SaaS 业务或云环境。

- 保持仅点名 `$saas-cloudbase-zoowork` 时调用，保留 `allow_implicit_invocation: false`，不得自动加载到无关项目。
- 保持 Skill 自包含；按需读取参考文件，避免在入口重复整套规范。不依赖其他业务仓库、本机绝对路径、客户数据或真实资源标识。
- 保持 React＋TypeScript、CloudBase、员工身份调用 ZooWork 的默认约定；尊重目标项目明确选择，不自动迁移现有架构。
- 明确区分本 Codex Skill 与应用运行时的 ZooWork 业务 Skill。通用机制归本仓库，产品专用规则归生成项目。
- 模板不含真实秘密；已有文件不直接覆盖。只有确定性重复操作值得加入脚本，不添加空脚手架或通用执行框架。
- 变更提升 Skill 的 metadata.version，运行 python3 scripts/validate.py；新增或改动决策分支时补充独立场景试跑，按实际结果更新 docs/VALIDATION.md 和 HANDOFF.md。
- 有远程仓库后使用功能分支与 PR，禁止直接推送 main。未获授权不创建远程、不发布、不安装到用户技能目录、不调用模型或创建云资源。
