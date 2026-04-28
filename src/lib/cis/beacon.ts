const BEACON_INTERVAL_MS = 30_000;
const IDLE_THRESHOLD_MS = 3 * 60 * 1000; // 3 minutes

export function startBeaconSession(params: {
  domainIds: string[];
  contentType: string;
  contentId: string;
  apiUrl: string;
}): () => void {
  const sessionId = crypto.randomUUID();
  let lastActivity = Date.now();
  let idleSecondsTotal = 0;
  let idleCount = 0;
  let lastBeaconTime = Date.now();

  // Activity detection
  const resetActivity = () => {
    lastActivity = Date.now();
  };
  window.addEventListener('keydown', resetActivity);
  window.addEventListener('click', resetActivity);
  window.addEventListener('scroll', resetActivity);

  const interval = setInterval(async () => {
    const now = Date.now();
    const gap = now - lastBeaconTime;

    if (now - lastActivity > IDLE_THRESHOLD_MS) {
      // Student is idle — accumulate idle time, don't send beacon
      idleSecondsTotal += Math.floor(gap / 1000);
      idleCount++;
      lastBeaconTime = now;
      return;
    }

    // Student is active — send beacon
    try {
      await fetch(`${params.apiUrl}/api/cis/beacon`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          domainIds: params.domainIds,
          contentType: params.contentType,
          contentId: params.contentId,
          sessionId,
          idleSecondsTotal,
          idleCount,
        }),
      });
    } catch {
      // Silent fail — beacon loss is acceptable
    }

    lastBeaconTime = now;
  }, BEACON_INTERVAL_MS);

  // Return cleanup function
  return () => {
    clearInterval(interval);
    window.removeEventListener('keydown', resetActivity);
    window.removeEventListener('click', resetActivity);
    window.removeEventListener('scroll', resetActivity);
  };
}
