## Crons
https://github.com/Hassanmushtaq524/sentry-javascript/blob/develop/packages/node/src/cron/cron.ts
BEFORE
```js
async function monitoredTick(context: unknown, onComplete?: unknown): Promise<void> {
      const checkInId = Sentry.captureCheckIn({
  monitorSlug: monitorSlug,
  status: 'in_progress',
});
```
AFTER
```js
async function monitoredTick(context: unknown, onComplete?: unknown): Promise<void> {
  return withMonitor(
    monitorSlug,
    async () => {
      try {
        await onTick(context, onComplete);
        Sentry.captureCheckIn({
          monitorSlug,
          status: 'ok',
        });
      } catch (e) {
        captureException(e);
        Sentry.captureCheckIn({
          monitorSlug,
          status: 'error',
        });
        throw e;
      }
    },
    {
      schedule: { type: 'crontab', value: cronString },
      timezone: timeZone || undefined,
    }
  );
}```




## Feedback Widget
https://github.com/Hassanmushtaq524/sentry-javascript/blob/ea9200c078a539d29078a67cc33d39a8274db01b/packages/feedback/src/core/createMainStyles.ts
```js
const GREEN = 'rgba(34, 139, 34, 1)';

const DEFAULT_CUSTOM: InternalTheme = {
  foreground: '#1f2937', // dark navy
  background: '#f9fafb', // off-white
  accentForeground: '#ffffff', // white
  accentBackground: GREEN, // custom green color
  successColor: '#10b981', // light green
  errorColor: '#ef4444', // light red
  border: '2px solid rgba(31, 41, 55, 0.2)', // darker border
  boxShadow: '0px 6px 30px rgba(0, 0, 0, 0.15)', // stronger shadow
  outline: '2px auto var(--accent-background)',
  interactiveFilter: 'brightness(98%)',
};
```



## Session Replay (Add Framerate)
https://github.com/Hassanmushtaq524/sentry-javascript/blob/develop/packages/replay-canvas/src/canvas.ts
```js
interface ReplayCanvasOptions {
  enableManualSnapshot?: boolean;
  maxCanvasSize?: [width: number, height: number];
  quality: 'low' | 'medium' | 'high';
  frameRate?: number;  // Add frame rate control
}```
```js
const manager = new CanvasManager({
  ...getCanvasManagerOptions,
  enableManualSnapshot,
  maxCanvasSize,
  frameRate: options.frameRate || 2,  // Default frame rate is 2fps
});
```