# 开发交接

## 0.2.0：依赖、凭据前置条件与上下文恢复

- 当前分支 feat/prerequisite-checks。新增 references/prerequisites.md，明确 CloudBase 管理工具、应用 SDK、ZooWork SDK／UI 的安装和验证，以及 local、cloudbase、provision、agent、deploy 分阶段准入。
- 条件凭据不设为全局必填；员工 Key 由后端开通并加密保存。应用 doctor 与本 Skill 包检查分开，诊断不安装、开通或调用模型。
- 新增每轮开工、阶段回写和中断交接规则；目标项目用 AGENTS、PRODUCT、PROJECT_BASELINE、架构、PRECHECK、HANDOFF 与 Git 恢复可验证事实。
- 验证完成：包检查、quick_validate、复制包独立检查通过；断裂／缺失引用以及必填、条件秘密误填均会被拒绝。独立离线试跑覆盖无账号起步、HTTP 路径条件凭据及员工未开通、新会话恢复三个场景，未发现规则冲突；只验证流程，不代表应用已运行。
- 本轮保存于本地功能分支，未安装依赖、配置真实秘密、创建云资源或调用模型；没有远程仓库，未创建 PR、合并、发布或安装。

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
