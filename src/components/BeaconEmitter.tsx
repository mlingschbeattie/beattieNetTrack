import { useEffect } from 'react';
import { startBeaconSession } from '../lib/cis/beacon';
import type { CISDomainTag } from '../lib/events';
import type { DomainMapping } from '../types/lab';

interface BeaconEmitterProps {
  domains: DomainMapping[];
  contentId: string;
  apiUrl: string;
}

/**
 * Null-rendering React island that starts a CIS time-beacon session for the
 * current lab. Mount once when a student opens any lab workspace.
 */
export default function BeaconEmitter({ domains, contentId, apiUrl }: BeaconEmitterProps) {
  useEffect(() => {
    if (!apiUrl || domains.length === 0) return;
    const cisDomains: CISDomainTag[] = domains.map((d) => ({
      domainId: d.domainId,
      weight: d.weight ?? 1.0,
    }));
    const stop = startBeaconSession({
      domains: cisDomains,
      contentType: 'lab',
      contentId,
      apiUrl,
    });
    return stop;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}
