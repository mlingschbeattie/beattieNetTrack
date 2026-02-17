(() => {
  const state = {
    progress: 0,
    completed: false,
    metadata: {},
  };

  const handlers = {
    run: null,
    check: null,
    submit: null,
    reset: null,
  };

  const normalizeResult = (action, result) => ({
    type: 'CLASSROOM_RESULT',
    action,
    passed: Boolean(result?.passed),
    progress: typeof result?.progress === 'number' ? result.progress : state.progress,
    message: typeof result?.message === 'string' ? result.message : '',
    difficulty: result?.difficulty,
    estMinutes: result?.estMinutes,
    metadata: result?.metadata ?? state.metadata,
  });

  const api = {
    get() {
      return { ...state };
    },
    set(next = {}) {
      state.progress = typeof next.progress === 'number' ? next.progress : state.progress;
      state.completed = typeof next.completed === 'boolean' ? next.completed : state.completed;
      state.metadata = { ...state.metadata, ...(next.metadata ?? {}) };
      return api.get();
    },
    on(action, callback) {
      if (!(action in handlers) || typeof callback !== 'function') return;
      handlers[action] = callback;
    },
    send(action, payload = {}) {
      if (!window.parent || window.parent === window) return;
      window.parent.postMessage(normalizeResult(action, payload), window.location.origin);
    },
  };

  window.ClassroomProgress = api;

  window.addEventListener('message', async (event) => {
    if (event.origin !== window.location.origin) return;
    const data = event.data;
    if (!data || data.type !== 'CLASSROOM_ACTION') return;

    const action = data.action;
    const handler = handlers[action];
    if (typeof handler !== 'function') {
      api.send(action, {
        passed: action === 'run',
        progress: state.progress,
        message: `No ${action} handler registered`,
      });
      return;
    }

    try {
      const result = await handler(data.payload ?? {});
      api.send(action, result ?? {});
    } catch (error) {
      api.send(action, {
        passed: false,
        progress: state.progress,
        message: error instanceof Error ? error.message : `${action} failed`,
      });
    }
  });
})();
