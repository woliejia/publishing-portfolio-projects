#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDir, '..');
const skillPath = path.join(root, 'SKILL.md');
const failures = [];

if (!fs.existsSync(skillPath)) {
  failures.push('技能包根目录缺少 SKILL.md');
} else {
  const skill = fs.readFileSync(skillPath, 'utf8');
  const match = skill.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) {
    failures.push('SKILL.md 缺少 YAML frontmatter');
  } else {
    const keys = [...match[1].matchAll(/^([A-Za-z0-9_-]+):/gm)].map((item) => item[1]);
    for (const required of ['name', 'description']) {
      if (!keys.includes(required)) failures.push(`缺少 frontmatter 字段：${required}`);
    }
    const unsupported = keys.filter((key) => !['name', 'description'].includes(key));
    if (unsupported.length) failures.push(`发现厂商专属 frontmatter 字段：${unsupported.join(', ')}`);
  }

  for (const link of skill.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const target = link[1];
    if (/^(?:https?:|#)/i.test(target)) continue;
    if (!fs.existsSync(path.resolve(root, target))) failures.push(`缺少引用文件：${target}`);
  }

  const forbidden = [
    /[A-Za-z]:\\Users\\/i,
    /\/Users\/[^/]+\//,
    /\/home\/[^/]+\//,
    /(?:password|secret|token|api[_-]?key)\s*[:=]\s*\S+/i,
  ];
  for (const pattern of forbidden) {
    if (pattern.test(skill)) failures.push(`发现不可移植或敏感内容，匹配规则：${pattern}`);
  }
}

for (const relative of ['references/verification.md', 'references/platform-compatibility.md', 'scripts/check-release.mjs']) {
  if (!fs.existsSync(path.join(root, relative))) failures.push(`缺少通用资源：${relative}`);
}

if (failures.length) {
  for (const failure of failures) console.error(`失败：${failure}`);
  process.exit(1);
}

console.log('通过：通用 Agent Skill 技能包检查');
