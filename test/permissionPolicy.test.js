const assert = require('assert');
const path = require('path');

const {
  evaluateFileAction,
  evaluateCommandAction,
  loadPermissionPolicyFromText,
} = require('../out/permissionPolicy.testable.js');

const root = path.resolve('E:/workspace');
const brain = path.resolve('E:/brain');

function assertAllowed(result, label) {
  assert.strictEqual(result.allowed, true, label || result.reason);
}

function assertBlocked(result, label) {
  assert.strictEqual(result.allowed, false, label || 'expected blocked');
  assert.ok(result.reason && result.reason.length > 0, 'blocked result should explain why');
}

assertAllowed(
  evaluateFileAction({ action: 'edit', absPath: path.join(root, 'src/app.ts'), rootPath: root, brainDir: brain }),
  'missing policy keeps full local capability'
);

assertBlocked(
  evaluateFileAction({
    action: 'delete',
    absPath: 'C:/Windows/System32/drivers/etc/hosts',
    rootPath: root,
    brainDir: brain,
    policy: { protectedPaths: ['C:/Windows'] },
  }),
  'protected Windows paths are blocked'
);

assertBlocked(
  evaluateFileAction({
    action: 'create',
    absPath: 'D:/outside/file.txt',
    rootPath: root,
    brainDir: brain,
    policy: { allowedRoots: [root, brain] },
  }),
  'allowedRoots confines file writes'
);

assertAllowed(
  evaluateCommandAction({
    command: 'npm run build',
    cwd: root,
    rootPath: root,
    brainDir: brain,
    policy: { dangerousCommandsRequireApproval: ['Remove-Item', 'del', 'git push'] },
  }),
  'ordinary verification commands are allowed'
);

assertBlocked(
  evaluateCommandAction({
    command: 'Remove-Item -Recurse E:/workspace/dist',
    cwd: root,
    rootPath: root,
    brainDir: brain,
    policy: { dangerousCommandsRequireApproval: ['Remove-Item', 'del', 'git push'] },
  }),
  'dangerous command patterns are blocked'
);

assertBlocked(
  evaluateCommandAction({
    command: 'npm install left-pad',
    cwd: root,
    rootPath: root,
    brainDir: brain,
    agentId: 'qa',
    policy: {
      agents: {
        qa: { canRunCommands: true, allowedCommands: ['npm test', 'npm run build'] },
      },
    },
  }),
  'agent command allowlists are enforced'
);

const parsed = loadPermissionPolicyFromText(`
# Policy

\`\`\`json
{
  "allowedRoots": ["E:/workspace"],
  "agents": {
    "qa": { "canEditFiles": false }
  }
}
\`\`\`
`);

assert.deepStrictEqual(parsed && parsed.allowedRoots, ['E:/workspace']);
assert.strictEqual(parsed && parsed.agents.qa.canEditFiles, false);

console.log('permission policy tests passed');
