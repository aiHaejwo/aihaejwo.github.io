import { adConfig } from './onestore-config.mjs';

const privacyPath = './privacy.html';

// The injected SDK/environment also let the lifecycle contract run in Node tests.
export function createBridge(sdk, env, config = adConfig) {
  let initialized = false;
  let started = false;
  let rewardInFlight = false;
  let pauseCallback;
  let resumeCallback;
  let snapshot;
  const bridge = {
    paused: false,
    ringerSilent: false,
    get interstitialAvailable() {
      return initialized && !!config.interstitialPlacementId &&
        sdk.ads.isSupported('interstitial');
    },
    get rewardedAvailable() {
      return initialized && !!config.rewardedPlacementId &&
        /^https:\/\//.test(config.rewardServerUrl ?? '') && sdk.ads.isSupported('rewarded');
    },
    async showRewarded() {
      if (!bridge.rewardedAvailable || rewardInFlight) return false;
      rewardInFlight = true;
      const post = async (path, body) => {
        const response = await env.fetch(`${config.rewardServerUrl.replace(/\/$/, '')}${path}`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
        });
        if (!response.ok) throw new Error('Reward verification unavailable');
        return response.json();
      };
      try {
        const { requestId, claimToken } = await post('/requests', {});
        const result = await sdk.ads.showRewardedAsync({
          placementId: config.rewardedPlacementId, requestId,
        });
        if (result.status !== 'rewarded') return false;
        // The SDK result is only a UI event; only signed SSV can authorize a reward.
        for (let attempt = 0; attempt < 60; attempt++) {
          const claim = await post(`/rewards/${requestId}/claim`, { claimToken });
          if (claim.status === 'granted') return true;
          if (claim.status !== 'pending') return false;
          await env.delay(1000);
        }
        throw new Error('Reward verification timed out');
      } finally {
        rewardInFlight = false;
      }
    },
    async showInterstitial() {
      if (!bridge.interstitialAvailable) return;
      // Failure/no_fill never blocks the next battle.
      await sdk.ads.showInterstitialAsync({
        placementId: config.interstitialPlacementId,
      });
    },
    bind(pause, resume, serialize) {
      pauseCallback = pause;
      resumeCallback = resume;
      snapshot = serialize;
    },
    async initialize() {
      sdk.on('pause', () => {
        bridge.paused = true;
        pauseCallback?.();
      });
      sdk.on('resume', (event) => {
        if (typeof event.ringerSilent === 'boolean') {
          bridge.ringerSilent = event.ringerSilent;
        }
        bridge.paused = false;
        resumeCallback?.();
      });
      sdk.on('exit', () => {
        bridge.paused = true;
        pauseCallback?.();
        if (snapshot) env.save(snapshot());
      });
      const info = await sdk.initializeAsync();
      if (info.err) {
        // Standalone browsers are a playable preview; host failures still reject.
        if (info.err !== 'Platform Not Supported') throw new Error(info.err);
        return;
      }
      initialized = true;
      bridge.ringerSilent = info.ringerSilent === true;
      env.safeArea(info.safeArea);
      bridge.loadingProgress(0);
    },
    loadingProgress(progress) {
      if (initialized) sdk.setLoadingProgress(progress);
    },
    async startGame() {
      if (!initialized || started) return;
      bridge.loadingProgress(100);
      await sdk.startGameAsync();
      started = true;
    },
    async openPrivacyPolicy() {
      if (initialized) await sdk.openDeeplink(env.privacyUrl);
      else env.open(env.privacyUrl);
    },
  };
  return bridge;
}

export async function initializeOneStore() {
  const { createSDK } = await import(
    'https://h5sdk.onestore.net/lib/v1.1.0/onestore-h5-sdk.min.js'
  );
  const bridge = createBridge(createSDK(), {
    privacyUrl: new URL(privacyPath, document.baseURI).href,
    save: (value) => localStorage.setItem(
      'flutter.mythic_roll_defense_save_v2', JSON.stringify(value)),
    safeArea: (area = {}) => {
      for (const edge of ['top', 'bottom', 'left', 'right']) {
        const inset = Number(area[edge]);
        document.body.style.setProperty(`--safe-${edge}`,
          `${Number.isFinite(inset) ? Math.max(0, inset) : 0}px`);
      }
    },
    open: (url) => window.open(url, '_blank', 'noopener,noreferrer'),
    fetch: (...args) => fetch(...args),
    delay: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
  });
  window.mythicOneStore = bridge;
  await bridge.initialize();
}

