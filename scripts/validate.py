#!/usr/bin/env python3
"""只读检查文档仓库与模板，不访问网络或读取应用秘密。"""

from pathlib import Path
import re
import sys
import os
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate():
    required = [
        'README.md', 'AGENTS.md', 'HANDOFF.md', 'VERSION',
        'docs/WORKFLOW.md', 'docs/ARCHITECTURE.md', 'docs/PREREQUISITES.md',
        'docs/ENVIRONMENT.md',
        'docs/ZOOWORK.md', 'docs/AGENTS_AND_SKILLS.md', 'docs/CONTEXT.md',
        'docs/DELIVERY.md', 'docs/LINKS.md', 'docs/VALIDATION.md',
        'templates/AGENTS.md', 'templates/PRODUCT.md', 'templates/HANDOFF.md',
        'templates/PROJECT_BASELINE.md', 'templates/PRECHECK.md',
        'templates/env.example', 'templates/gitignore', 'templates/dockerignore',
    ]
    errors = []
    for name in required:
        if not (ROOT / name).is_file():
            errors.append('缺少文件：' + name)
    if errors:
        return errors
    if not re.fullmatch(r'\d+\.\d+\.\d+\n', (ROOT / 'VERSION').read_text()):
        errors.append('规范版本须为独立的语义版本号')
    if (ROOT / 'skills').exists() or (ROOT / 'agents').exists() or (ROOT / 'SKILL.md').exists():
        errors.append('本仓库不能保留 Codex 技能入口或安装目录')

    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts:
            continue
        if path.suffix not in {'.md', '.example'}:
            continue
        content = path.read_text()
        if re.search(r'(?:zpk|zwp)_live_[A-Za-z0-9_-]{12,}', content):
            errors.append('疑似真实凭据：' + str(path.relative_to(ROOT)))
        if path.suffix != '.md':
            continue
        if re.search(r'\$saas-cloudbase-zoowork|metadata\.version|assets/templates/|references/', content):
            errors.append('残留旧的技能调用或内部路径：' + str(path.relative_to(ROOT)))
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
    architecture = (ROOT / 'docs/ARCHITECTURE.md').read_text()
    for line in (ROOT / 'templates/env.example').read_text().splitlines():
        if not line:
            continue
        assignment = re.fullmatch(r'(?:#\s*)?([A-Z][A-Z0-9_]*)=(.*)', line)
        if not assignment:
            if not line.startswith('#'):
                errors.append('环境变量模板格式错误')
            continue
        name, value = assignment.groups()
        variables.append(name)
        defaults = {'PORTAL_ENABLED': 'true', 'APP_ORIGIN': 'http://127.0.0.1:8787', 'PORT': '8787'}
        if value != defaults.get(name, ''):
            errors.append('环境模板含非空秘密或未经定义的默认值：' + name)
        if '`' + name + '`' not in architecture:
            errors.append('环境变量缺少定义：' + name)
    if len(set(variables)) != len(variables):
        errors.append('环境变量模板有重复定义')
    git_environment = {name: os.environ[name] for name in ('PATH', 'SYSTEMROOT', 'WINDIR', 'TMP', 'TEMP', 'TMPDIR') if name in os.environ}
    git_environment.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
    try:
        with tempfile.TemporaryDirectory(prefix='saas-ignore-check-') as temporary:
            app = Path(temporary)
            (app / '.gitignore').write_text((ROOT / 'templates/gitignore').read_text())
            (app / 'empty-excludes').write_text('')
            subprocess.run(['git', 'init', '--quiet', str(app)], check=True, capture_output=True, env=git_environment)
            excluded = ['.env', '.env.local', '.env.production', 'server/.env', 'server/.env.local']
            included = ['.env.example', 'server/.env.example', 'src/index.ts']
            result = subprocess.run(
                ['git', '-c', 'core.excludesFile=' + str(app / 'empty-excludes'), '-C', str(app), 'check-ignore', '--no-index', '--stdin'],
                input='\n'.join(excluded + included) + '\n', capture_output=True, text=True, env=git_environment,
            )
            if result.returncode != 0 or set(result.stdout.splitlines()) != set(excluded):
                errors.append('Git 忽略模板不能正确区分真实配置与可提交示例')
    except (OSError, subprocess.CalledProcessError):
        errors.append('无法用隔离 Git 仓库验证忽略模板')

    docker_rules = [line.strip() for line in (ROOT / 'templates/dockerignore').read_text().splitlines() if line.strip() and not line.startswith('#')]
    if not {'.env', '.env.*', '**/.env', '**/.env.*'}.issubset(docker_rules) or any(line.startswith('!') for line in docker_rules):
        errors.append('Docker 忽略模板须排除根目录与嵌套配置，且不能重新包含它们')
    return errors


if __name__ == '__main__':
    failures = validate()
    for failure in failures:
        print('失败：' + failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print('通过：文档结构、规范版本、相对引用、空值／忽略模板与旧技能入口移除检查。')
    print('未执行：私有仓库在线读取、依赖安装、云资源或真实模型验收。')
