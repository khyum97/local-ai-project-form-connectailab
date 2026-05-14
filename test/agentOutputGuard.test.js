const assert = require('assert');

const {
  validateAgentFileWrite,
  formatValidationReasons,
} = require('../out/agentOutputGuard.testable.js');

function assertBlocked(result, label) {
  assert.strictEqual(result.ok, false, label || 'expected validation failure');
  assert.ok(result.reasons.length > 0, 'blocked result should include reasons');
}

function assertAllowed(result, label) {
  assert.strictEqual(result.ok, true, label || formatValidationReasons(result));
}

assertBlocked(
  validateAgentFileWrite('src/workers/compensation_worker.py', 'print("ok")\n<create_file path="src/models.py">\n'),
  'action tags must not be written into Python files'
);

assertBlocked(
  validateAgentFileWrite('src/app.py', 'def broken(:\n    pass\n'),
  'invalid Python must be blocked before file write'
);

assertBlocked(
  validateAgentFileWrite('package.json', '{ "name": "broken", }'),
  'invalid JSON must be blocked before file write'
);

assertAllowed(
  validateAgentFileWrite('src/app.py', 'def ok():\n    return 1\n'),
  'valid Python should pass'
);

assertAllowed(
  validateAgentFileWrite('docs/notes.md', '```python\n<create_file path="x.py">\n```\n'),
  'markdown notes may contain fenced examples'
);

console.log('agent output guard tests passed');
