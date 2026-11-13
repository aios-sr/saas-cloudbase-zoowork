# CloudBase 与 ZooWork SaaS 开发 Skill

面向产品人员，通过 Codex 构建 React＋TypeScript、CloudBase 与 ZooWork 企业 SaaS。默认处理员工身份、租户隔离、Agent／业务 Skill 复用、持久任务和 PR 发布；具体产品、专业方法与账号资源由新项目定义。

本仓库独立维护通用开发 Skill，不包含可直接部署的 SaaS 源码、客户资料或凭据。当前版本见 [SKILL.md](skills/saas-cloudbase-zoowork/SKILL.md) 的 `metadata.version`。

## 开始使用

首次可直接在 Codex 中指定本地文件：

> 使用 $saas-cloudbase-zoowork；若尚未安装，先读取本仓库 skills/saas-cloudbase-zoowork/SKILL.md，并按其指引为我构建一个 SaaS。产品给【使用者】使用，主要流程是【输入、处理与交付物】。技术方案使用默认约定，先完成可操作的预览。

需要在其他项目中方便调用时，将整个 `skills/saas-cloudbase-zoowork` 目录安装到 Codex 的个人技能目录。默认位置为 `~/.codex/skills/saas-cloudbase-zoowork`；设置了 `CODEX_HOME` 时使用该目录下的 `skills/saas-cloudbase-zoowork`。由 Codex 按当前安装机制办理；已有同名 Skill 时先核对版本，不直接覆盖。本 Skill 关闭自动触发，安装后仅在点名时调用。新会话使用：

> 使用 $saas-cloudbase-zoowork，帮采购团队做一个供应商评估系统。员工提交供应商资料，系统生成评估草稿，由负责人确认后保存。

安装的是供 Codex 开发应用的 Skill；应用运行时的 ZooWork 业务 Skill 由生成的应用分别管理。两者的版本、权限和更新记录各自独立。

## 内容

- [Skill 入口](skills/saas-cloudbase-zoowork/SKILL.md)：业务收集、实施顺序与完成条件。
- [参考文档](skills/saas-cloudbase-zoowork/references/architecture.md)：技术架构、CloudBase、环境变量与身份；其余内容由入口按需引导。
- [项目模板](skills/saas-cloudbase-zoowork/assets/templates/)：AGENTS、PRODUCT、HANDOFF 和空值环境变量示例。
- [验证记录](docs/VALIDATION.md)：本包检查、独立场景试跑及未验证范围。

调用前需有 Codex 的文件与开发工具；真实接入还需要所选 CloudBase 环境、服务商账号及 UI 包的合法使用权限。没有权限时先完成可预览、可审查的部分，不自动复用其他项目资源，也不要求产品人员在聊天中粘贴密钥。部署、真实模型费用和外部操作按实际授权处理。

## 维护

修改 `skills/saas-cloudbase-zoowork` 中的单一来源，提升 `metadata.version` 并同步验证记录；不维护另一份相同的长篇规范。新应用将实际采用的技术决定、Skill 版本和例外保存在自己的项目文档中，升级时审查差异，不强行改写已有应用。

本地检查：

```sh
python3 scripts/validate.py
```

该命令只检查包结构、引用和空值模板，不调用云端或模型。真实行为试跑与云端验收另行记录，不能把静态检查当作完整应用验证。首次 GitHub 发布前配置远程仓库并走 PR；本地仓库创建不等于远程发布。未确定许可证前，不自行宣称可公开分发第三方包或资料。
