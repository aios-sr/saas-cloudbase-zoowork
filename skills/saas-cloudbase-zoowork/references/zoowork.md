# ZooWork 接入

## 8. ZooWork 接入合同

### 8.1 两类接口分工

| 接口 | 固定官方地址 | 使用身份 |
| --- | --- | --- |
| Partner API | `https://ecap-partner-gateway.ecap.gsmo.ai/partner/v1` | 当前服务商的 `PARTNER_API_KEY` |
| Agent API | `https://clawapi.ecap.gsmo.ai/service/v1` | 后端解析出的具体员工密钥 |
| 公共接入文档 | `https://ecap-partner-gateway.ecap.gsmo.ai/partner/v1/docs` | 无需密钥即可阅读 |
| OpenAPI | `https://ecap-partner-gateway.ecap.gsmo.ai/partner/v1/openapi.json` | 由后端带服务商密钥读取，不提交带密钥请求或完整回包 |

以下按该服务商接入合同实现；部署端能力仍须只读核对，不能把通用 SDK 示例中的鉴权方式直接变成共享执行身份。

- 使用 `Authorization: Bearer ...`，设置本应用自定义 `User-Agent`。
- Partner 写操作使用稳定 `Idempotency-Key`；重试复用原操作标识和参数。Agent、消息和 Skill 等操作按所装 SDK 及目标服务真正支持的幂等合同实现，不能只加一个 Header 就宣称结果可重放。
- 固定并校验官方目的地址，禁止把密钥转发到用户提供的 URL 或跟随不受信任的重定向。工件下载使用返回的受控下载地址，不把员工鉴权头带给对象存储域名。
- 列表查询完整处理分页；第一页未找到不等于不存在。权限、版本、就绪状态和归属不匹配时停止，不以猜测字段或扩大权限处理。
- 上游超时或返回不明确时记录结果未知，查询原操作或受理状态；不能立即生成新幂等标识再次扣费。

### 8.2 企业与员工开通

1. 保存企业草稿只写本地；明确正式开通后调用 `POST /enterprises`，校验并保存上游 ID。
2. 生成员工邀请不立即发钥；接受邀请并绑定本应用账户后，由后端调用 `POST /enterprises/{id}/members`。
3. 使用稳定且包含新应用命名空间的 `external_id`／`external_identity`，与本地服务商、企业和账户唯一对应；名称或职位变化不改变身份映射。
4. 校验响应的企业、成员和外部标识。只有员工密钥安全取得并加密保存后，连接状态才可就绪；未知结果可恢复，不能伪造成功。
5. 开通成员不代表已创建业务 Agent。首次任务再按 [Agent 创建规则](agents-and-skills.md) 创建；界面区分账户、成员连接、Agent 就绪与任务状态。
6. 员工本人不需要看到密钥。丢失时走受控换钥；`previous_key_revoked` 缺失或未确认时关闭执行连接并记问题，不把返回新 Key 当作旧 Key 已撤销。

成员密钥不替代应用权限。旧成员的上游空间可能具有不同隔离行为，应验证实际能力并坚持本应用的归属检查；不能因为同企业密钥可见某个 Agent 就授予访问权。服务商 Key 没有直接创建业务 Agent 的职责，Partner 管理清单也不能代替员工身份下的 Agent 清单。[Partner 接入文档](https://ecap-partner-gateway.ecap.gsmo.ai/partner/v1/docs)
