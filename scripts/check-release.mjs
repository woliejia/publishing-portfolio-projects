#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const [publicArg, slugArg] = process.argv.slice(2);
if (!publicArg || !slugArg) {
  console.error('用法：node scripts/check-release.mjs <公开目录> <slug>');
  process.exit(2);
}

const slug = slugArg.replace(/^\/+|\/+$/g, '');
if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) {
  console.error('slug 只能包含小写字母、数字和连字符。');
  process.exit(2);
}

const publicDir = path.resolve(publicArg);
const homePath = path.join(publicDir, 'index.html');
const childDir = path.join(publicDir, slug);
const childPath = path.join(childDir, 'index.html');
const failures = [];

for (const file of [homePath, childPath]) {
  if (!fs.existsSync(file)) failures.push(`缺少文件：${path.relative(publicDir, file)}`);
}

if (!failures.length) {
  const home = fs.readFileSync(homePath, 'utf8');
  const child = fs.readFileSync(childPath, 'utf8');
  if (!home.includes(`/${slug}/`) && !home.includes(`./${slug}/`)) {
    failures.push(`首页没有链接到 /${slug}/`);
  }
  for (const marker of ['/src/', '/@vite/client', '/node_modules/']) {
    if (child.includes(marker)) failures.push(`子页面构建仍包含开发环境引用：${marker}`);
  }

  const attributes = [...child.matchAll(/(?:src|href)=["']([^"']+)["']/gi)].map((match) => match[1]);
  for (const value of attributes) {
    if (/^(?:https?:|data:|blob:|#|mailto:|tel:)/i.test(value)) continue;
    const clean = value.split(/[?#]/, 1)[0];
    const target = clean.startsWith('/')
      ? path.resolve(publicDir, `.${clean}`)
      : path.resolve(childDir, clean);
    const relative = path.relative(publicDir, target);
    if (relative.startsWith('..') || path.isAbsolute(relative)) {
      failures.push(`资源路径越过公开目录边界：${value}`);
    } else if (!fs.existsSync(target)) {
      failures.push(`缺少本地资源：${value}`);
    }
  }

  const sitemap = path.join(publicDir, 'sitemap.xml');
  if (fs.existsSync(sitemap) && !fs.readFileSync(sitemap, 'utf8').includes(`/${slug}/`)) {
    failures.push(`sitemap.xml 没有包含 /${slug}/`);
  }
}

if (failures.length) {
  for (const failure of [...new Set(failures)]) console.error(`失败：${failure}`);
  process.exit(1);
}

console.log(`通过：静态作品集发布检查 ${publicDir} -> /${slug}/`);
