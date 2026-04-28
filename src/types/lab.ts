export interface DomainMapping {
  domainId: string;
  weight: number;
}

/** Subset of the labs content collection schema used by CIS wiring. */
export interface LabMeta {
  title: string;
  description: string;
  domains: DomainMapping[];
}
