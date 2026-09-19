#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const [publicArg, slugArg] = process.argv.slice(2);
if (!publicArg || !slugArg) {
  console.error('Usage: node scripts/check-release.mjs <public-dir> <slug>');
  process.exit(2);
}

const slug = slugArg.replace(/^\/+|\/+$/g, '');
if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) {
  console.error('Slug must contain lowercase letters, numbers, and hyphens only.');
  process.exit(2);
}

const publicDir = path.resolve(publicArg);
const homePath = path.join(publicDir, 'index.html');
const childDir = path.join(publicDir, slug);
const childPath = path.join(childDir, 'index.html');
const failures = [];

for (const file of [homePath, childPath]) {
  if (!fs.existsSync(file)) failures.push(`Missing ${path.relative(publicDir, file)}`);
}

if (!failures.length) {
  const home = fs.readFileSync(homePath, 'utf8');
  const child = fs.readFileSync(childPath, 'utf8');
  if (!home.includes(`/${slug}/`) && !home.includes(`./${slug}/`)) {
    failures.push(`Homepage does not link to /${slug}/`);
  }
  for (const marker of ['/src/', '/@vite/client', '/node_modules/']) {
    if (child.includes(marker)) failures.push(`Child bundle contains development reference: ${marker}`);
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
      failures.push(`Asset escapes public directory: ${value}`);
    } else if (!fs.existsSync(target)) {
      failures.push(`Missing local asset: ${value}`);
    }
  }

  const sitemap = path.join(publicDir, 'sitemap.xml');
  if (fs.existsSync(sitemap) && !fs.readFileSync(sitemap, 'utf8').includes(`/${slug}/`)) {
    failures.push(`sitemap.xml does not contain /${slug}/`);
  }
}

if (failures.length) {
  for (const failure of [...new Set(failures)]) console.error(`FAIL ${failure}`);
  process.exit(1);
}

console.log(`PASS static portfolio release: ${publicDir} -> /${slug}/`);
