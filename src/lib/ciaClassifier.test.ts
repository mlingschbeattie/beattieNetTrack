import test from 'node:test';
import assert from 'node:assert/strict';
import { INCIDENTS } from '../components/islands/CiaTriadClassifier';

test('INCIDENTS contains all 3 core CIA scenarios with distinct primary pillars', () => {
  assert.equal(INCIDENTS.length, 3);

  const pillars = INCIDENTS.map((i) => i.correctPillar);
  assert.ok(pillars.includes('confidentiality'));
  assert.ok(pillars.includes('integrity'));
  assert.ok(pillars.includes('availability'));

  // Ensure 1-to-1 mapping
  assert.equal(new Set(pillars).size, 3);
});

test('Incident 1 (Cloud Bucket) evaluates Confidentiality, correct threat, and defense', () => {
  const inc = INCIDENTS[0];
  assert.equal(inc.correctPillar, 'confidentiality');
  assert.equal(inc.correctThreatIndex, 0);
  assert.equal(inc.correctDefenseIndex, 0);
  assert.ok(inc.socraticExplanation.includes('Confidentiality was breached first'));
});

test('Incident 2 (Payroll Script) evaluates Integrity, correct threat, and defense', () => {
  const inc = INCIDENTS[1];
  assert.equal(inc.correctPillar, 'integrity');
  assert.equal(inc.correctThreatIndex, 1);
  assert.equal(inc.correctDefenseIndex, 0);
  assert.ok(inc.socraticExplanation.includes('Integrity was violated first'));
});

test('Incident 3 (Registration Outage) evaluates Availability, correct threat, and defense', () => {
  const inc = INCIDENTS[2];
  assert.equal(inc.correctPillar, 'availability');
  assert.equal(inc.correctThreatIndex, 2);
  assert.equal(inc.correctDefenseIndex, 1);
  assert.ok(inc.socraticExplanation.includes('Availability is the primary failure'));
});
