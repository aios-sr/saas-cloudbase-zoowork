#!/usr/bin/env python3
"""只读检查本仓库 Skill 包及模板，不访问网络或读取应用秘密。"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'saas-cloudbase-zoowork'


def validate():
    required = [
        'SKILL.md', 'agents/openai.yaml',
        'references/architecture.md', 'references/zoowork.md',
        'references/agents-and-skills.md', 'references/delivery.md',
        'references/links.md', 'assets/templates/AGENTS.md',
        'assets/templates/PRODUCT.md', 'assets/templates/HANDOFF.md',
        'assets/templates/env.example',
    ]
    errors = []
    for name in required:
        if not (SKILL / name).is_file():
            errors.append('缺少文件：' + name)
    if errors:
        return errors

    entry = (SKILL / 'SKILL.md').read_text()
    front = re.match(r'\A---\n(.*?)\n---\n', entry, re.S)
    if not front:
        errors.append('入口缺少闭合的 YAML 头部')
    else:
        if not re.search(r'^name: saas-cloudbase-zoowork$', front[1], re.M):
            errors.append('Skill 名称与目录不一致')
        if not re.search(r'^description: \S.+$', front[1], re.M):
            errors.append('缺少触发描述')
        if not re.search(r'^  version: "\d+\.\d+\.\d+"$', front[1], re.M):
            errors.append('缺少明确的语义版本')

    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts:
            continue
        if path.suffix not in {'.md', '.yaml', '.example'}:
            continue
        content = path.read_text()
        if re.search(r'(?:zpk|zwp)_live_[A-Za-z0-9_-]{12,}', content):
            errors.append('疑似真实凭据：' + str(path.relative_to(ROOT)))
        if path.suffix != '.md':
            continue
        if len(re.findall(r'^```', content, re.M)) % 2:
            errors.append('代码围栏未成对：' + str(path.relative_to(ROOT)))
        for target in re.findall(r'\]\(([^)]+)\)', content):
            parsed = urlsplit(target)
            if parsed.scheme:
                if parsed.scheme != 'https':
                    errors.append('外部文档须使用 HTTPS：' + str(path.relative_to(ROOT)))
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
                errors.append('本地引用失效或越出仓库：' + str(path.relative_to(ROOT)))

    variables = []
    for line in (SKILL / 'assets/templates/env.example').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        if not re.fullmatch(r'[A-Z][A-Z0-9_]*=.*', line):
            errors.append('环境变量模板格式错误')
            continue
        name, value = line.split('=', 1)
        variables.append(name)
        defaults = {'PORTAL_ENABLED': 'true', 'APP_ORIGIN': 'http://127.0.0.1:8787', 'PORT': '8787'}
        if value != defaults.get(name, ''):
            errors.append('环境模板含非空秘密或未经定义的默认值：' + name)
        architecture = (SKILL / 'references/architecture.md').read_text()
        if '`' + name + '`' not in architecture:
            errors.append('环境变量缺少定义：' + name)
    if len(set(variables)) != len(variables):
        errors.append('环境变量模板有重复定义')
    metadata = (SKILL / 'agents/openai.yaml').read_text()
    if '$saas-cloudbase-zoowork' not in metadata:
        errors.append('界面提示缺少 Skill 调用名称')
    if not re.search(r'^  allow_implicit_invocation: false$', metadata, re.M):
        errors.append('Skill 必须关闭自动触发')
    return errors


if __name__ == '__main__':
    failures = validate()
    for failure in failures:
        print('失败：' + failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print('通过：包结构、入口标识、仓库内引用、围栏、环境模板与凭据模式检查。')
    print('未执行：链接在线可达性、Codex 自动触发、UI 包安装、云资源与真实模型验收。')
