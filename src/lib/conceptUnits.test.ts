import test from 'node:test';
import assert from 'node:assert/strict';
import { groupActivitiesIntoConceptUnits } from '../components/islands/TrackModuleList';
import type { TrackActivitySummary } from './content';

test('groupActivitiesIntoConceptUnits pairs matching lesson and quiz into concept unit', () => {
  const activities: TrackActivitySummary[] = [
    {
      slug: 'tech-plus-1-3-1-storage-units',
      type: 'lesson',
      title: 'Storage Units — From Bits to Petabytes',
      description: 'Demystifying digital storage',
      order: 5,
      href: '/lessons/tech-plus-1-3-1-storage-units',
      module: 'tech-plus.it-concepts',
    },
    {
      slug: 'tech-plus-1-3-1-storage-units',
      type: 'quiz',
      title: 'Storage Units',
      description: 'Quiz workspace',
      order: 5,
      href: '/quizzes/tech-plus-1-3-1-storage-units',
      module: 'tech-plus.it-concepts',
    },
    {
      slug: 'tech-plus-1-4-1-troubleshooting-methodology',
      type: 'lesson',
      title: 'Troubleshooting Methodology — The Framework That Keeps You From Breaking Things',
      description: 'Master CompTIA methodology',
      order: 8,
      href: '/lessons/tech-plus-1-4-1-troubleshooting-methodology',
      module: 'tech-plus.it-concepts',
    },
    {
      slug: 'tech-plus-1-4-1-troubleshooting-methodology',
      type: 'quiz',
      title: 'Troubleshooting Methodology',
      description: 'Quiz workspace',
      order: 8,
      href: '/quizzes/tech-plus-1-4-1-troubleshooting-methodology',
      module: 'tech-plus.it-concepts',
    },
  ];

  const units = groupActivitiesIntoConceptUnits(activities);
  assert.equal(units.length, 2);

  // Concept 1: Storage Units
  assert.equal(units[0].order, 5);
  assert.equal(units[0].title, 'Storage Units');
  assert.equal(units[0].lesson?.slug, 'tech-plus-1-3-1-storage-units');
  assert.equal(units[0].quiz?.slug, 'tech-plus-1-3-1-storage-units');

  // Concept 2: Troubleshooting Methodology
  assert.equal(units[1].order, 8);
  assert.equal(units[1].title, 'Troubleshooting Methodology');
  assert.equal(units[1].lesson?.slug, 'tech-plus-1-4-1-troubleshooting-methodology');
  assert.equal(units[1].quiz?.slug, 'tech-plus-1-4-1-troubleshooting-methodology');
});

test('groupActivitiesIntoConceptUnits handles standalone activities cleanly', () => {
  const activities: TrackActivitySummary[] = [
    {
      slug: 'net-cable-lab',
      type: 'lab',
      title: 'Cable Termination Lab',
      description: 'Crimp RJ-45 cables',
      order: 3,
      href: '/labs/net-cable-lab',
      module: 'net.cabling',
    },
  ];

  const units = groupActivitiesIntoConceptUnits(activities);
  assert.equal(units.length, 1);
  assert.equal(units[0].standalone?.slug, 'net-cable-lab');
  assert.equal(units[0].standalone?.type, 'lab');
});

test('groupActivitiesIntoConceptUnits pairs cross-prefix concept slugs like net-copper-cables and net-1-3-1-copper-cables', () => {
  const activities: TrackActivitySummary[] = [
    {
      slug: 'net-copper-cables',
      type: 'lesson',
      title: 'Copper Cabling Standards',
      description: 'Twisted pair specifications',
      order: 1,
      href: '/lessons/net-copper-cables',
      module: 'net.cabling',
    },
    {
      slug: 'net-1-3-1-copper-cables',
      type: 'quiz',
      title: 'Copper Cables Checkpoint',
      description: 'Quiz',
      order: 1,
      href: '/quizzes/net-1-3-1-copper-cables',
      module: 'net.cabling',
    },
  ];

  const units = groupActivitiesIntoConceptUnits(activities);
  assert.equal(units.length, 1);
  assert.equal(units[0].lesson?.slug, 'net-copper-cables');
  assert.equal(units[0].quiz?.slug, 'net-1-3-1-copper-cables');
});

test('groupActivitiesIntoConceptUnits does NOT pair unrelated activities that share order number', () => {
  const activities: TrackActivitySummary[] = [
    {
      slug: 'pct-motherboards-architecture',
      type: 'lesson',
      title: 'Motherboard Form Factors and Busses',
      description: 'Motherboard architecture',
      order: 2,
      href: '/lessons/pct-motherboards-architecture',
      module: 'pct.hardware',
    },
    {
      slug: 'pc-tech-hardware-checkpoint',
      type: 'quiz',
      title: 'Hardware Comprehensive Checkpoint',
      description: 'Module checkpoint',
      order: 2,
      href: '/quizzes/pc-tech-hardware-checkpoint',
      module: 'pct.hardware',
    },
  ];

  const units = groupActivitiesIntoConceptUnits(activities);
  // Must NOT pair motherboard lesson with general hardware checkpoint!
  assert.equal(units.length, 2);
  assert.equal(units[0].standalone?.slug, 'pct-motherboards-architecture');
  assert.equal(units[1].standalone?.slug, 'pc-tech-hardware-checkpoint');
});

