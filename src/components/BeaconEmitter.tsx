import { useEffect } from 'react';
import { startBeaconSession } from '../lib/cis/beacon';

interface BeaconEmitterProps {
  domainIds: string[];
  contentId: string;
  apiUrl: string;
}

/**
 * Null-rendering React island that starts a CIS time-beacon session for the
 * current lab. Mount once when a student opens any lab workspace.
 */
export default function BeaconEmitter({ domainIds, contentId, apiUrl }: BeaconEmitterProps) {
  useEffect(() => {
    if (!apiUrl || domainIds.length === 0) return;
    const stop = startBeaconSession({
      domainIds,
      contentType: 'lab',
      contentId,
      apiUrl,
    });
    return stop;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}
