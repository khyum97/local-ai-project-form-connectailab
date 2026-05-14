import * as fs from 'fs';
import * as path from 'path';

export type AgentPermission = {
  canReadFiles?: boolean;
  canEditFiles?: boolean;
  canDeleteFiles?: boolean;
  canRunCommands?: boolean;
  allowedCommands?: string[];
};

export type PermissionPolicy = {
  defaultMode?: 'full' | 'restricted';
  allowedRoots?: string[];
  protectedPaths?: string[];
  dangerousCommandsRequireApproval?: string[];
  agents?: Record<string, AgentPermission>;
};

export type PermissionDecision = {
  allowed: boolean;
  reason?: string;
};

export type FileAction = 'create' | 'edit' | 'delete' | 'read' | 'list' | 'open';

const DEFAULT_DANGEROUS_COMMANDS = [
  'rm -rf',
  'Remove-Item',
  'rmdir',
  'del ',
  'format ',
  'diskpart',
  'git push',
  'npm publish',
  'pnpm publish',
  'yarn publish',
  'docker push',
  'kubectl delete',
  'terraform destroy',
];

const POLICY_FILENAMES = [
  'agents.permissions.json',
  'permissions.json',
  '권한정책.json',
  'agents.permissions.md',
  'permissions.md',
  '권한정책.md',
];

function normalizePathForCompare(p: string): string {
  const resolved = path.resolve(p);
  return process.platform === 'win32' ? resolved.toUpperCase() : resolved;
}

function isInsideOrSame(child: string, parent: string): boolean {
  const c = normalizePathForCompare(child);
  const p = normalizePathForCompare(parent);
  if (c === p) return true;
  const rel = path.relative(p, c);
  return !!rel && !rel.startsWith('..') && !path.isAbsolute(rel);
}

function commandMatches(command: string, pattern: string): boolean {
  const cmd = command.trim().toLowerCase();
  const p = pattern.trim().toLowerCase();
  if (!p) return false;
  return cmd === p || cmd.startsWith(p + ' ') || cmd.includes(p);
}

function agentPolicy(policy: PermissionPolicy | undefined, agentId: string | undefined): AgentPermission | undefined {
  if (!policy || !agentId || !policy.agents) return undefined;
  return policy.agents[agentId];
}

function hasAllowedRoot(policy: PermissionPolicy | undefined, absPath: string, rootPath: string, brainDir?: string): PermissionDecision {
  const roots = policy?.allowedRoots && policy.allowedRoots.length > 0
    ? policy.allowedRoots
    : policy?.defaultMode === 'restricted'
      ? [rootPath, brainDir].filter(Boolean) as string[]
      : [];

  if (roots.length === 0) return { allowed: true };
  if (roots.some(r => isInsideOrSame(absPath, r))) return { allowed: true };
  return { allowed: false, reason: `권한정책 allowedRoots 밖입니다: ${absPath}` };
}

function hasProtectedPath(policy: PermissionPolicy | undefined, absPath: string): PermissionDecision {
  const protectedPaths = policy?.protectedPaths || [];
  const hit = protectedPaths.find(p => isInsideOrSame(absPath, p));
  if (!hit) return { allowed: true };
  return { allowed: false, reason: `권한정책 protectedPaths로 보호된 경로입니다: ${hit}` };
}

export function evaluateFileAction(input: {
  action: FileAction;
  absPath: string;
  rootPath: string;
  brainDir?: string;
  agentId?: string;
  policy?: PermissionPolicy | null;
}): PermissionDecision {
  const policy = input.policy || undefined;
  const protectedDecision = hasProtectedPath(policy, input.absPath);
  if (!protectedDecision.allowed) return protectedDecision;

  const rootDecision = hasAllowedRoot(policy, input.absPath, input.rootPath, input.brainDir);
  if (!rootDecision.allowed) return rootDecision;

  const ap = agentPolicy(policy, input.agentId);
  if (ap) {
    if ((input.action === 'create' || input.action === 'edit') && ap.canEditFiles === false) {
      return { allowed: false, reason: `${input.agentId} 에이전트는 파일 편집 권한이 없습니다.` };
    }
    if (input.action === 'delete' && ap.canDeleteFiles === false) {
      return { allowed: false, reason: `${input.agentId} 에이전트는 파일 삭제 권한이 없습니다.` };
    }
    if ((input.action === 'read' || input.action === 'list') && ap.canReadFiles === false) {
      return { allowed: false, reason: `${input.agentId} 에이전트는 파일 읽기 권한이 없습니다.` };
    }
  }

  return { allowed: true };
}

export function evaluateCommandAction(input: {
  command: string;
  cwd: string;
  rootPath: string;
  brainDir?: string;
  agentId?: string;
  policy?: PermissionPolicy | null;
}): PermissionDecision {
  const policy = input.policy || undefined;

  const cwdDecision = hasAllowedRoot(policy, input.cwd, input.rootPath, input.brainDir);
  if (!cwdDecision.allowed) return cwdDecision;

  const ap = agentPolicy(policy, input.agentId);
  if (ap?.canRunCommands === false) {
    return { allowed: false, reason: `${input.agentId} 에이전트는 명령 실행 권한이 없습니다.` };
  }
  if (ap?.allowedCommands && ap.allowedCommands.length > 0) {
    const ok = ap.allowedCommands.some(p => commandMatches(input.command, p));
    if (!ok) return { allowed: false, reason: `${input.agentId} 에이전트 allowedCommands에 없는 명령입니다.` };
  }

  const dangerous = [
    ...DEFAULT_DANGEROUS_COMMANDS,
    ...(policy?.dangerousCommandsRequireApproval || []),
  ];
  const hit = dangerous.find(p => commandMatches(input.command, p));
  if (hit) {
    return { allowed: false, reason: `위험 명령은 권한정책상 사용자 승인이 필요합니다: ${hit}` };
  }

  return { allowed: true };
}

export function loadPermissionPolicyFromText(text: string): PermissionPolicy | null {
  const trimmed = text.trim();
  if (!trimmed) return null;

  const jsonBlock = trimmed.match(/```json\s*([\s\S]*?)```/i);
  const candidate = jsonBlock ? jsonBlock[1].trim() : trimmed;
  try {
    const parsed = JSON.parse(candidate);
    if (parsed && typeof parsed === 'object') return parsed as PermissionPolicy;
  } catch {
    return null;
  }
  return null;
}

export function loadPermissionPolicyFromDirs(dirs: Array<string | undefined | null>): PermissionPolicy | null {
  const seen = new Set<string>();
  for (const dir of dirs) {
    if (!dir) continue;
    const absDir = path.resolve(dir);
    if (seen.has(absDir)) continue;
    seen.add(absDir);
    for (const filename of POLICY_FILENAMES) {
      const file = path.join(absDir, filename);
      try {
        if (!fs.existsSync(file) || !fs.statSync(file).isFile()) continue;
        const parsed = loadPermissionPolicyFromText(fs.readFileSync(file, 'utf-8'));
        if (parsed) return parsed;
      } catch {
        continue;
      }
    }
  }
  return null;
}
