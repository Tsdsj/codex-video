// Pure frame functions: safe for nonsequential rendering and Studio seeking.
export const beatFrame = (index: number, bpm: number, fps: number, offset = 0) => {
  if (![index, bpm, fps, offset].every(Number.isFinite) || bpm <= 0 || fps <= 0) throw new Error('Invalid beat clock');
  return Math.round((offset + index * 60 / bpm) * fps);
};
export const travel = (frame: number, start: number, end: number) => {
  if (![frame, start, end].every(Number.isFinite) || end <= start) throw new Error('Invalid travel interval');
  const t = Math.max(0, Math.min(1, (frame - start) / (end - start)));
  // Quintic interpolation: zero velocity and acceleration at either hold.
  return t * t * t * (t * (t * 6 - 15) + 10);
};
export const EVENTS = {depart: 1.0, arrive: 3.0, resolve: 4.8};
export const stage = (frame: number, fps: number) => ({
  x: travel(frame, EVENTS.depart * fps, EVENTS.arrive * fps),
  reveal: travel(frame, 3.15 * fps, EVENTS.resolve * fps),
  title: travel(frame, 0.2 * fps, 0.9 * fps),
});
