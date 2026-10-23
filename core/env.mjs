// core/env.mjs — Load .env configuration and provide runtime environment variables
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(__dirname, '..');

function loadDotEnv() {
  const envPath = path.join(REPO_ROOT, '.env');
  if (!fs.existsSync(envPath)) return {};
  const res = {};
  const content = fs.readFileSync(envPath, 'utf8');
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const eqIdx = line.indexOf('=');
    if (eqIdx === -1) continue;
    const key = line.slice(0, eqIdx).trim();
    let val = line.slice(eqIdx + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    res[key] = val;
  }
  return res;
}

const fileEnv = loadDotEnv();

/**
 * Returns environment variable value, prioritizing process.env over .env file.
 */
export function getEnv(key, defaultValue = '') {
  return process.env[key] !== undefined ? process.env[key] : (fileEnv[key] !== undefined ? fileEnv[key] : defaultValue);
}

/**
 * Output directory name or path for films / generated projects.
 * Default: 'films'
 */
export const OUTPUT_DIR = getEnv('OUTPUT_DIR', 'films');

/**
 * Get the full path for a film project given its name or relative path.
 */
export function getProjectDir(name) {
  if (path.isAbsolute(name)) return name;
  return path.resolve(REPO_ROOT, OUTPUT_DIR, name);
}
