import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { spawnSync } from 'child_process';

export type AgentOutputValidation = {
  ok: boolean;
  reasons: string[];
};

const ACTION_TAG_RE = /<\/?(?:create_file|write_file|edit_file|delete_file|read_file|list_files|run_command|command|bash|terminal|file)\b/i;
const MARKDOWN_FENCE_RE = /^\s*```|```\s*$/m;
const CODE_EXTENSIONS = new Set([
  '.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
  '.json', '.sql', '.css', '.scss', '.html', '.vue',
  '.yaml', '.yml', '.toml',
]);

function isCodeLike(filePath: string): boolean {
  return CODE_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

function pythonCandidates(): string[][] {
  const out: string[][] = [];
  const envPython = process.env.PYTHON || process.env.PYTHON_PATH;
  if (envPython) out.push([envPython]);
  if (process.platform === 'win32') out.push(['py', '-3'], ['python']);
  else out.push(['python3'], ['python']);
  return out;
}

function validatePythonSyntax(content: string): string | null {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'yum-agent-guard-'));
  const file = path.join(dir, 'candidate.py');
  try {
    fs.writeFileSync(file, content, 'utf-8');
    for (const cmd of pythonCandidates()) {
      const [bin, ...prefix] = cmd;
      const res = spawnSync(bin, [...prefix, '-m', 'py_compile', file], {
        encoding: 'utf-8',
        timeout: 15000,
        windowsHide: true,
      });
      if (res.error && (res.error as any).code === 'ENOENT') continue;
      if (res.status === 0) return null;
      const err = (res.stderr || res.stdout || '').trim();
      return err ? err.split(/\r?\n/).slice(-4).join('\n') : 'python syntax check failed';
    }
    return null;
  } finally {
    try { fs.rmSync(dir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

export function validateAgentFileWrite(filePath: string, content: string): AgentOutputValidation {
  const reasons: string[] = [];
  const ext = path.extname(filePath).toLowerCase();
  const codeLike = isCodeLike(filePath);

  if (codeLike && ACTION_TAG_RE.test(content)) {
    reasons.push('agent action tag leaked into code content');
  }

  if (codeLike && MARKDOWN_FENCE_RE.test(content)) {
    reasons.push('markdown code fence leaked into code content');
  }

  if (ext === '.py') {
    const syntaxError = validatePythonSyntax(content);
    if (syntaxError) reasons.push(`python syntax check failed: ${syntaxError}`);
  }

  if (ext === '.json') {
    try { JSON.parse(content); }
    catch (e: any) { reasons.push(`json syntax check failed: ${e?.message || e}`); }
  }

  return { ok: reasons.length === 0, reasons };
}

export function formatValidationReasons(result: AgentOutputValidation): string {
  return result.reasons.join('; ');
}
