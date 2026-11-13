# 开发交接

## 初始范围

已建立独立的 SaaS 开发 Skill 源码仓库：Skill 入口、按需读取的架构与接入规则、多 Agent 协作、官方链接、项目模板及本地包检查。未复制原业务仓库、真实资源配置、客户资料或凭据。

默认使用 React＋TypeScript、CloudBase 和员工身份下的 ZooWork。多 Agent 覆盖角色规格、实例归属、串并行、汇总、人审、版本快照、失败恢复与取消传播。

## 验证与边界

实际检查与独立场景试跑见 docs/VALIDATION.md。该仓库不包含可运行 SaaS 脚手架；创建包不等于已完成任意新业务的云端验收。

## 仓库与发布

按用户确认，仓库与 Skill 统一命名为 saas-cloudbase-zoowork，关闭自动触发，仅点名 `$saas-cloudbase-zoowork` 时使用。

仅创建本地 Git 仓库；未配置远程，未创建 GitHub PR，未发布或安装 Skill。未修改来源项目，未创建云资源，未调用真实模型。

## 下一步

用户选择远程托管位置后配置仓库并按 PR 流程维护；需要使用时将 skills/saas-cloudbase-zoowork 作为整体安装。首次真实产品开发时按 Skill 记录应用层验证，基于实际问题做有界修正。
