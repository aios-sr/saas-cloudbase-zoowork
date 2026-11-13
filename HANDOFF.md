# 文档仓库交接

## 当前范围

规范版本 0.4.0，本轮开发分支 docs/env-file-lifecycle。新增 docs/ENVIRONMENT.md 及 templates/gitignore、templates/dockerignore，补齐新应用本地 .env 的位置、独占创建、既有值保留、忽略与权限、显式加载和生产隔离。

README、执行流程、架构与前置检查已引用该专题，项目 AGENTS／PRECHECK 和环境模板同步约定。变量用途与阶段条件保留原有单一来源；员工 Key 仍由后端开通并加密保存，不新增全局执行 Key。

## 验证

文档检查与真实 Git 忽略场景通过；在临时目录用 Node.js v24.15.0 验证初始化示例与加载优先级，未修改开发者本地配置。故障样例覆盖忽略遗漏与反向包含，结果见 docs/VALIDATION.md。

未创建真实 .env、读取或写入 Key、安装依赖、构建 Docker 镜像、调用模型或修改客户应用／云资源。未来生成应用仍需实现并验证实际加载入口、doctor 和生产配置。

## 发布与上下文

目标为 aios-sr/saas-cloudbase-zoowork 私有 GitHub 仓库，以 PR 合并到 main 发布文档，不另部署应用。初次文档发布记录见 [PR #1](https://github.com/aios-sr/saas-cloudbase-zoowork/pull/1)；本轮 [PR #2](https://github.com/aios-sr/saas-cloudbase-zoowork/pull/2) 记录合并提交、检查与线上读取的实际结果。

生成应用固定仓库、VERSION、完整提交与采用范围，保留自己的技术决定、PRECHECK 和恢复点；不自动跟随本仓库 main，也不依赖原聊天。
