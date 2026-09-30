import {test} from 'node:test';
import assert from 'node:assert/strict';
import {beatFrame, travel, stage} from './motion.ts';

test('non-integer beats do not accumulate rounding drift', () => {
  assert.equal(beatFrame(1000, 127, 30), 14173);
  assert.equal(beatFrame(0, 120, 60, 0.5), 30);
  assert.throws(() => beatFrame(1, 0, 30));
});
test('travel holds endpoints and has smooth endpoint velocity', () => {
  assert.equal(travel(-1, 10, 30), 0);
  assert.equal(travel(31, 10, 30), 1);
  const dt = 0.001;
  assert.ok(travel(10 + dt, 10, 30) / dt < 1e-5);
  assert.ok((1 - travel(30 - dt, 10, 30)) / dt < 1e-5);
  assert.throws(() => travel(0, 10, 10));
});
test('frame state is seekable and has finite, bounded position at 30 and 60 fps', () => {
  for (const fps of [30, 60]) {
    const reference = stage(3.2 * fps, fps);
    for (let f = 8 * fps - 1; f >= 0; f--) {
      const s = stage(f, fps);
      assert.ok(Number.isFinite(s.x) && s.x >= 0 && s.x <= 1);
      assert.ok(Number.isFinite(s.reveal) && s.reveal >= 0 && s.reveal <= 1);
    }
    assert.deepEqual(stage(3.2 * fps, fps), reference);
  }
});
test('hero holds still during final reading window', () => {
  assert.equal(stage(6 * 60, 60).x, stage(7.9 * 60, 60).x);
  assert.equal(stage(7.9 * 60, 60).reveal, 1);
});
