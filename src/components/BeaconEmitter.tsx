import { useEffect } from 'react';
import { startBeaconSession } from '../lib/cis/beacon';
import { emitLessonStarted, type CISDomainTag } from '../lib/events';
import type { DomainMapping } from '../types/lab';

interface BeaconEmitterProps {
  domains: DomainMapping[];
  contentId: string;
  contentType?: string;
  contentTitle?: string;
  apiUrl: string;
}

/**
 * Null-rendering React island that starts a CIS time-beacon session for the
 * current content item (lab, lesson, or quiz). Mount once on view.
 */
export default function BeaconEmitter({
  domains,
  contentId,
  contentType = 'lab',
  contentTitle,
  apiUrl,
}: BeaconEmitterProps) {
  useEffect(() => {
    if (!apiUrl || domains.length === 0) return;
    const cisDomains: CISDomainTag[] = domains.map((d) => ({
      domainId: d.domainId,
      weight: d.weight ?? 1.0,
    }));

    if (contentType === 'lesson' && contentTitle) {
      emitLessonStarted(contentId, contentTitle, cisDomains, apiUrl);
    }

    const stop = startBeaconSession({
      domains: cisDomains,
      contentType,
      contentId,
      apiUrl,
    });
    return stop;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}

