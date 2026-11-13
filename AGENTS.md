# 文档仓库协作约定

使用简体中文。先读 README.md、VERSION、docs/WORKFLOW.md、docs/CONTEXT.md、docs/VALIDATION.md 和 HANDOFF.md。本仓库维护以 React＋TypeScript、CloudBase 和 ZooWork 为默认方案的 SaaS 开发文档与模板，不承载客户应用或云环境。

- 使用线上文档模式，不恢复 SKILL.md、Codex 技能元数据、安装步骤或调用命令。ZooWork 运行时业务 Skill 和 CloudBase 官方开发工具仍按各自合同维护，不因本仓库改版而删除。
- 保持章节与模板可从 README 发现，相对引用在同一提交内有效；不依赖来源业务仓库、机器绝对路径、客户数据或真实资源标识。
- 文档升级写入 VERSION。生成应用固定来源仓库、文档版本、完整提交和采用范围；不自动迁移已有架构或覆盖目标项目规则。
- 模板与文档不含真实秘密，已有文件不直接覆盖。只为确定性重复检查添加必要脚本，不引入通用开发执行器。
- 每轮核对分支、git status 和差异；阶段完成及时更新 HANDOFF。修改后运行 python3 scripts/validate.py；重要流程变更补充场景验证，按实际证据更新 docs/VALIDATION.md。
- 功能分支经 PR 合并到 main，禁止直接推送 main。首次初始化远程可以创建默认 README 作为 PR 基线；规范内容仍通过 PR 发布。没有完成 CI 时明确记录本地检查范围，不虚构线上验收。
- 创建远程、变更可见性或发布按用户授权；本仓库不调用模型、不绑定真实 Key、不修改客户项目或云资源。不要把文档发布当作生成应用已上线。
