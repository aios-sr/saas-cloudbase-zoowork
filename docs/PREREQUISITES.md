# 开发前置检查

在编写依赖相关代码、真实接入或发布前执行相应阶段检查。把结果写入目标项目 `docs/PRECHECK.md`：检查时间、目标阶段、非秘密环境／服务版本、项目、必需条件、状态、证据与下一步。没有账号时允许规划和受控本地开发；不把后续阶段凭据缺失变成全部工作的阻塞，也不把演示标为真实接通。

## 1. 开发工具与应用依赖分开准备

先检查目标项目、已有安装与授权。仅补齐所需能力；阅读本开发规范不会自动安装 CloudBase 插件、npm SDK 或 UI 包。

| 层次 | 准备与安装路径 | 进入后续阶段前的证据 |
| --- | --- | --- |
| 本地工具链 | 检查 Node.js、npm／npx、Git；版本须满足平台、Vite、UI 与 ZooWork SDK 的交集。缺工具时按系统适用方式准备 | 版本可读、包管理器可用；不反复运行不存在的命令 |
| CloudBase 管理能力 | 先核对国内／国际站，优先复用当前已授权且可用的 MCP。缺少时按当前 [插件安装文档](https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/ai-agent-plugins) 配置 CloudBase 插件；命令行方式仅针对本次 Codex 目标，见下方示例 | 当前会话能描述并调用所需只读工具；“已安装”不等于工具已加载或已登录 |
| MCP 当前不可用 | 按官方配置完成后记录重载要求；需要本轮管理操作时改用已验证的 CLI。缺 CLI 时按授权安装 `@cloudbase/cli`，确认 `tcb --version` 后安全登录 | 只读核对账号、站点和完整 EnvId；不能用机器已有登录替代归属确认，不用通用 `tcb deploy` 猜测发布动作 |
| 应用的 CloudBase SDK | 原生 Web 认证默认安装 `@cloudbase/js-sdk`。后端选 HTTP API 时不额外强装 Node SDK；若采用 JS SDK 的 Node 适配，按 PG 初始化文档核对所需可选包；选用 `@cloudbase/node-sdk` 的能力时再执行 `npm install @cloudbase/node-sdk` | 包版本与锁文件、实际导入、类型与构建通过；认证／PG／存储按所选路径验证，不能拿 NoSQL API 替代 PG |
| 应用的 ZooWork SDK | 后端安装 `@zoowork-ai/sdk`，核对当前文档、所装类型与 ESM／运行时要求。Partner API 单独按官方 HTTP 合同实现 | 后端导入和类型检查通过；客户端显式接收后端解析的员工 Key，不能依赖全局环境变量回退 |
| ZooWork UI | 从已授权发布渠道取得 `@zooclaw/design-system` 与 `@zooclaw/chat-ui`，核对版本、peerDependencies、主题与 CSS 入口 | 锁定来源与版本，能构建并在浏览器显示官方骨架；只有包名或下载链接不算安装完成。缺权限时继续不依赖 UI 包的工作，不暗换库 |

缺 CloudBase 插件且允许安装时，先核对官方命令，再按实际目标执行，例如只面向 Codex：

```sh
npx plugins add TencentCloudBase/cloudbase-plugin -y --scope user --target codex
```

如果已包含所需 CloudBase Skills，不重复安装；仅装 Skills 不等于 MCP 已连接。不同客户端可能使用市场安装方式，按本次客户端的官方说明选择。[CloudBase 开发工具](https://docs.cloudbase.net/ai/cloudbase-ai-toolkit/)

应用首次添加依赖的命令形态如下；Codex 先选兼容版本再安装，提交实际 package.json 与锁文件。已有锁文件且无新增依赖时使用 `npm ci`；不升级全部大版本，也不在本规范仓库安装应用依赖。

```sh
npm install @cloudbase/js-sdk
npm install @zoowork-ai/sdk
```

在实际应用或对应 workspace 的 package.json 所在目录安装；ZooWork 客户端只从后端模块导入，不能被前端打包。UI 包按实际授权渠道安装；需要私有 registry Token 时放在包管理器受控凭据中，不写入仓库或前端，也不将其当成应用运行 Key。不要因为包不可访问而反复尝试未经确认的镜像。

CloudBase SDK 路径以 [PG SDK 初始化](https://docs.cloudbase.net/api-reference/webv3-pg/initialization) 和 [Node SDK 说明](https://docs.cloudbase.net/quick-start/frameworks/nodejs) 为准。ZooWork 的运行时与模块要求以 [SDK 安装文档](https://zoowork.ai/docs/en/reference/typescript-sdk) 为准；创建客户端成功不代表其凭据已通过认证。

## 2. 按阶段检查配置与 Key

创建、填写或加载本地配置前先执行 [.env 生命周期](ENVIRONMENT.md)。本地 doctor 显式加载所选本地文件；deploy 阶段只验证目标版本注入，不用本地文件补缺项。

变量用途与秘密分类以 [配置合同](ARCHITECTURE.md) 为单一来源；以下只定义生效条件。将实际采用的认证／数据库路径写入 PROJECT_BASELINE，不要求产品人员选择字段名称或 SDK。

| 阶段 | 必需条件 | 缺失时允许继续的工作 |
| --- | --- | --- |
| `local` 本地开发 | 已用到的依赖安装与导入检查通过；本地端口和来源一致；受控演示显式隔离。开发真实会话能力时本地 SESSION_SECRET 就绪 | 云端账号与 Key 可未配置；继续文档、纯逻辑、受控测试及可构建部分，不能声称云端登录或 Agent 可用 |
| `cloudbase` 真实基础服务 | 完整 EnvId、站点、地域和应用资源归属明确；管理操作有已授权 MCP／CLI 身份。默认 HTTP 后端路径需要 CLOUDBASE_HTTP_BASE 与后端 CLOUDBASE_APIKEY；原生认证需要其 Publishable Key、提供方及权限；用文件功能时私有桶存在 | 可继续不依赖云端的工作；阻断真实数据／认证／文件接通的完成结论 |
| `provision` 企业成员开通 | 默认应用数据与会话路径就绪；APP_ID、PORTAL_PROVIDER_ID、后端 PARTNER_API_KEY 和 ENTERPRISE_ENCRYPTION_KEY 就绪；会话需 SESSION_SECRET；Partner 只读认证通过 | 可实现受控回归；不正式开通企业／员工，不以服务商 Key 执行 Agent |
| `agent` 员工 Agent 执行 | 应用、成员与对象权限通过；后端已有该员工的加密凭据及版本，解密和只读认证有效；SDK、实例归属及实际可用模型／Skill 权限满足本任务。真实模型调用另需既有费用授权 | 员工尚未接受邀请或开通时标记未就绪；不要求用户手填员工 Key，不使用共享或管理员身份回退 |
| `deploy` 正式部署 | 目标服务所启用能力的配置完整；秘密安全注入实际发布版本，生产来源／端口／资源一致；从合并的干净提交发布并分项验收 | 准备构建、变更清单及回滚；不能以本地有值代替生产注入。部署检查不要求预先开通所有未来员工，员工调用时另过 agent 阶段 |

`agent` 阶段的准入针对真实执行：没有实例或业务 Skill 时，可以在凭据与权限已核对后进行独立的创建／安装准备，再核验就绪；这些写操作不放入 doctor。已存在资源先按归属读取复用，不能以“准备”为由反复创建。

管理登录与应用访问凭据相互独立。OAuth／设备登录可完成管理授权时，不额外要求一把管理 API Key。确实使用本地 MCP API Key 登录时，按该工具文档配置 `CLOUDBASE_API_KEY`，不能把它和应用的 `CLOUDBASE_APIKEY` 混用或复制到可提交的 MCP 配置。

### 条件启用项与获取方式

- `CLOUDBASE_CUSTOM_CREDENTIALS` 仅自定义签票桥接启用时必需；未采用时记不适用。若所选 SDK 的签票或请求签名需要额外包，按当前初始化文档安装并验证，不假设装主包就已包含。
- `CLOUDBASE_SECRET_ID`／`CLOUDBASE_SECRET_KEY` 只在明确选择需要 CAM 凭据的服务端 SDK 路径时成对配置；临时凭据再配置其 Token 与有效期。可使用受支持的平台角色／临时身份时优先采用，不为默认 HTTP 路径额外索取永久 CAM 密钥。
- `DATABASE_URL` 只在明确选择 PG 协议直连时配置，并验证网络、SSL、权限及所用驱动；默认 HTTP 访问不要求它。不要以直连字符串代替原生用户认证。
- Publishable Key 是允许公开的初始化字段；它不授予后端管理权限。只通过前端白名单暴露公开字段，其他凭据不放进 `VITE_*`。
- 员工 Key 由本应用后端通过 Partner 开通接口取得并认证加密保存，不能作为 `.env.example` 的全局必填项。禁止新增全局 `ZOOWORK_API_KEY`。
- `ENTERPRISE_ENCRYPTION_KEY` 由后端安全生成独立的 32 字节随机根钥并按 Base64 保存；`SESSION_SECRET` 使用另一份至少 32 字节随机秘密。直接写受控秘密存储或被忽略的本地配置，不把生成结果打印到终端或聊天；既有项目先读取绑定状态，不重生成覆盖。
- 模型、维护账号与特定定时业务配置按实际启用功能要求；其他外部集成的凭据按已确认功能加入项目清单，不预先索取未使用服务的 Key。

## 3. 在生成应用中实现 doctor

由 Codex 在目标应用中实现入口，例如 `npm run doctor -- --stage local`；stage 只接受 `local`、`cloudbase`、`provision`、`agent`、`deploy` 中的一个值。默认只检查 `local`，不因无 Key 误发上游请求。`agent` 通过非秘密成员／对象 ID 选择明确执行范围，不收明文 Key 参数。该命令是生成项目的合同，本规范仓库没有预制适用于所有应用的运行脚本。

逐项报告检查 ID、是否为本阶段必需、状态与非秘密证据。状态限定为 `pass`、`fail`、`blocked`、`not_applicable`；缺失或未执行的必需项记 blocked／fail，不能假报 pass。可选功能未启用时记 not_applicable；其他阶段仍必需的凭据不能被永久标成不适用。当前阶段全部必需项通过才退出 0，否则非零，并在报告与 HANDOFF 留下受影响能力和下一步。

Key 的“本地存在、当前进程加载、目标服务版本注入、实际只读认证成功”分别核验和记录时间，不沿用过期状态。生产检查应在实际目标版本上下文或受控管理读取中确认；本地无法验证时记 blocked。默认不吐出 Key、片段、密文、签名 URL、完整环境或请求／回包。

doctor 只读检查，不创建企业、成员、Agent、Session 或 Skill，不发码、兑换、发登录验证码、不写迁移、不发布、不调用模型，也不执行插件／依赖安装。安装、生成根钥、开通成员与最小真实模型验收属于各自显式的准备或实施步骤，不通过诊断命令暗中执行。目标只读认证接口按当前合同核对；没有可用安全读取方式时保留 blocked，不拿写操作探测权限。

报告保存在目标项目 docs/PRECHECK.md，关联阶段、时间和非秘密版本；不得保存原始秘密回包或客户正文。项目变更依赖、环境、凭据绑定或认证路径后，重跑受影响阶段。本规范仓库的 scripts/validate.py 只验证文档与模板，不能作为应用 doctor 或云端凭据验收。
