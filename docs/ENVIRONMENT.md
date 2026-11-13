# 本地 .env 的创建、加载与验收

由 Codex 在目标应用中执行本规范，不在本开发规范仓库生成真实 `.env`。变量用途以 [架构合同](ARCHITECTURE.md) 为准，阶段必需项以 [前置检查](PREREQUISITES.md) 为准；缺后续阶段 Key 不阻塞规划或受控本地开发。

## 1. 文件位置与创建顺序

新应用默认在根目录（应用 package.json 所在目录）保存 `.env.example` 与本地后端 `.env`。前者提交空值示例与非秘密默认值，后者仅供本机后端加载。多 workspace 项目明确后端配置文件的唯一位置与解析基准，写入应用 README 和 PROJECT_BASELINE，不靠启动目录猜测。

按顺序完成：

1. 根据 [环境变量模板](../templates/env.example) 建立 `.env.example`，说明条件启用项，不放真实 Key、员工凭据或可登录的测试秘密。
2. 将 [Git 忽略模板](../templates/gitignore) 合并到新应用 `.gitignore`；有容器构建时，将 [Docker 忽略模板](../templates/dockerignore) 合并到实际构建上下文的 `.dockerignore`。保留已有规则，不整文件覆盖。即使项目暂无 Docker，也记录首次容器构建前必须完成该项。
3. 验证根目录与后端子目录的 `.env`、`.env.local`、`.env.production` 被 Git 忽略、`.env.example` 可提交，并核对实际索引中没有受保护配置；确认后再创建或填写 `.env`。
4. 仅在 `.env` 不存在时从空值示例独占创建；已存在则保留内容，不用复制、重定向或模板更新覆盖。遇到目录或符号链接先停止并核对路径。Unix 本地秘密文件使用仅当前用户可读写的权限，Windows 核对等效 ACL；填入秘密前完成权限检查。
5. 由 Codex 经受控渠道写入已授权配置，缺失项保持空值并按阶段记未就绪。新根钥与会话秘密安全生成且彼此独立；已有根钥不重新生成。不要要求产品人员在聊天提供 Key，不打印配置值或秘密片段。

下面是仅供 Codex 在目标应用根目录执行的初始化逻辑；它只复制示例，不生成或填入真实秘密：

```js
import { constants, copyFileSync, chmodSync, lstatSync } from 'node:fs';

try {
  copyFileSync('.env.example', '.env', constants.COPYFILE_EXCL);
  if (process.platform !== 'win32') chmodSync('.env', 0o600);
  console.log('已创建本地配置，真实凭据尚未填写');
} catch (error) {
  if (error.code !== 'EEXIST') throw error;
  if (!lstatSync('.env').isFile()) throw new Error('.env 路径不是普通文件');
  console.log('已有本地配置，保留原内容并核对权限');
}
```

此处不执行 `cp .env.example .env` 等可能覆盖已有配置的操作。模板新增变量时，仅追加确实缺少的字段与注释，保留原值、格式及不明来源的合法设置；不得因示例为空而清空本地值。已有秘密配置不是普通可提交草稿，不能进入自动快照或交接附件。

## 2. Git 与构建边界

`.gitignore` 不能移除已经受 Git 跟踪的文件。Codex 应结合忽略检查与索引检查核验；发现真实秘密已进入索引或历史时，停止相关提交、报告受影响范围，按授权处理停止跟踪与凭据轮换，不把“补一条忽略规则”当作修复。不能在诊断输出中展示文件内容。[Git 规则](https://git-scm.com/docs/gitignore)

Docker 忽略规则必须排除根目录及嵌套的 `.env`、`.env.*`，本地 `.env.example` 也不需要进入运行镜像。核对实际 build context、COPY／上传清单，以及可能优先生效的 Dockerfile 专用忽略文件；不能只检查仓库根目录。其他打包、静态托管和云端上传脚本也必须排除这些本地配置；服务端秘密不经 Docker ARG／ENV 固化进镜像。[Docker 构建上下文](https://docs.docker.com/build/concepts/context/#dockerignore-files)

## 3. 后端加载与优先级

新应用默认只加载这一份本地后端 `.env`，不另设未记录的 `.env.local`、模式文件或多份覆盖链。已有项目保留明确记录并验证的加载约定；需要改变时审查迁移影响。

- `dev:api` 与本地 doctor 显式解析配置文件的绝对位置，在导入依赖配置的业务模块、构造客户端之前完成加载。Node 运行时支持时使用原生 `--env-file` 或等效原生入口；采用其他加载器时保持相同优先级，并记录其版本与实际路径。
- **进程／平台注入值优先，本地文件只补未设置项。** 已注入的空字符串也不能被文件静默覆盖，应由本阶段必填校验报错；不使用无条件 override。加载后通过同一个配置模块完成类型、格式及阶段校验。[Node 环境文件](https://nodejs.org/api/cli.html#--env-filefile)
- 修改 `.env` 后按实际加载机制重启进程并重跑检查。文件有值不代表已加载，客户端能构造也不代表已认证。不要通过 `source .env` 或 shell 字符串拼接执行配置；引号、特殊字符和 JSON 按选定解析器的真实规则处理。
- 测试使用隔离的合成配置，不隐式读取开发者真实 `.env`。本地缺云端凭据时保留受控演示和只读诊断边界，不自动调用模型验证 Key。

应用 README 写明各启动／诊断入口、路径基准、配置来源和优先级；不能仅写“配置好环境变量”。

## 4. 前端与生产分开处理

Vite 的环境加载不会替后端完成上述工作。只有明确允许公开的初始化字段可进入前端；不得给秘密加 `VITE_` 前缀，也不能通过 define、放宽 envPrefix 或完整导出 process.env 绕过白名单。前后端解析器可能对变量展开有不同处理，不能据前端结果判断后端 Key 正确。[Vite 环境变量](https://vite.dev/guide/env-and-mode)

生产启动只读取目标服务实际注入的配置，不要求镜像内存在 `.env`，也不从开发机文件补齐缺项。`doctor --stage deploy` 同样不能加载本地 `.env`：在目标版本上下文或受控管理读取中验证注入；本地无法证明时记 blocked。若本地启动采用固定的 `--env-file` 参数，不能直接复用该启动命令执行部署阶段检查，须在应用入口区分配置来源。

## 5. 创建后的验收与记录

至少用合成值验证：首次创建成功、再次执行保留原文件与原值；本地文件未进 Git／上传／构建；`.env.example` 可提交；配置在业务模块前加载；进程值（含空字符串）不被文件覆盖；缺必需项按阶段失败；部署检查不会用本地文件掩盖缺失注入。

在 PRECHECK 记录配置文件位置（非内容）、来源、加载／注入上下文、检查时间及本地存在、进程加载、目标版本注入、只读认证四类证据。HANDOFF 仅引用结果和下一步，不复制秘密。应用 doctor 必须在生成应用中实现；本仓库的文档检查不能代替运行验收。
