/**
 * Seed Script: Simulate Learning Path Event Stream for Fake Mason and Fake Jacob.
 *
 * This script demonstrates the exact event stream emitted from BeattieNetTrack LMS
 * to the CIS Hub (api.beattietech.local / localhost:4321 / API) across diagnostic placement,
 * lesson reading beacons, quiz submissions, and lab completions.
 */

const API_URL = process.env.PUBLIC_API_URL || 'https://api.beattietech.local';

const FAKE_STUDENTS = {
  mason: {
    username: 'fake_mason',
    displayName: 'Fake Mason',
    track: 'network-engineer',
    targetCert: 'CompTIA Network+ (N10-009)',
    learningPath: [
      {
        step: 1,
        type: 'lesson',
        title: 'The OSI 7-Layer Reference Model',
        id: 'net-osi-model',
        domains: [{ domainId: 'netplus.networking_concepts', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }],
        minutesActive: 15,
      },
      {
        step: 2,
        type: 'quiz',
        title: 'OSI Model Deep-Dive Assessment',
        id: 'net-1-1-1-osi-model',
        domains: [{ domainId: 'netplus.networking_concepts', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }],
        score: 92,
      },
      {
        step: 3,
        type: 'lesson',
        title: 'VLANs and Trunking Fundamentals',
        id: 'net-vlans',
        domains: [{ domainId: 'netplus.infrastructure', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }],
        minutesActive: 20,
      },
      {
        step: 4,
        type: 'lab',
        title: 'Network Terminal Basics Lab',
        id: 'network-terminal-basics',
        domains: [{ domainId: 'netplus.troubleshooting', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }],
        score: 100,
        minutesActive: 35,
      },
    ],
  },
  jacob: {
    username: 'fake_jacob',
    displayName: 'Fake Jacob',
    track: 'pc-technician',
    targetCert: 'CompTIA A+ (220-1101 & 220-1102)',
    learningPath: [
      {
        step: 1,
        type: 'lesson',
        title: 'CPU Sockets and Motherboard Architecture',
        id: 'pct-motherboards',
        domains: [{ domainId: 'aplus1.hardware', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }],
        minutesActive: 18,
      },
      {
        step: 2,
        type: 'lab',
        title: 'PC Assembly Simulator Lab',
        id: 'pc-assembly',
        domains: [{ domainId: 'aplus1.hardware', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }],
        score: 100,
        minutesActive: 30,
      },
      {
        step: 3,
        type: 'quiz',
        title: 'Hardware Components & Field Triage',
        id: 'pct-1-1-1-hardware-components',
        domains: [{ domainId: 'aplus1.hardware', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }],
        score: 88,
      },
      {
        step: 4,
        type: 'lab',
        title: 'Windows Security Hardening Lab',
        id: 'pct-windows-security-hardening-lab',
        domains: [{ domainId: 'aplus2.security', weight: 0.8 }, { domainId: 'nocti.security', weight: 0.2 }],
        score: 100,
        minutesActive: 25,
      },
    ],
  },
};

async function dispatchEvents() {
  console.log('=== Rack Server Learning Path Event Dispatch ===');
  console.log(`Target Hub API: ${API_URL}`);
  console.log(`Environment: Beattie Tech Rack Server Network (beattie)`);

  const shouldSend = process.argv.includes('--send');

  for (const [key, student] of Object.entries(FAKE_STUDENTS)) {
    console.log(`\n▶ Processing Student: ${student.displayName} (${student.username}) -> Target: ${student.targetCert}`);
    for (const item of student.learningPath) {
      console.log(`  [Step ${item.step}] (${item.type.toUpperCase()}) ${item.title}`);
      
      let payload;
      let eventType;

      if (item.type === 'lesson') {
        eventType = 'lms.lab_beacon';
        payload = {
          domains: item.domains,
          contentType: 'lesson',
          contentId: item.id,
          sessionId: `sim-${student.username}-${item.id}`,
          idleSecondsTotal: 0,
          idleCount: 0,
          studentUsername: student.username,
        };
      } else if (item.type === 'quiz') {
        eventType = 'lms.quiz_completed';
        payload = {
          domains: item.domains,
          contentType: 'quiz',
          contentId: item.id,
          score: item.score,
          maxScore: 100,
          studentUsername: student.username,
          submittedAt: new Date().toISOString(),
        };
      } else if (item.type === 'lab') {
        eventType = 'lms.lab_completed';
        payload = {
          domains: item.domains,
          contentType: 'lab',
          contentId: item.id,
          score: item.score,
          maxScore: 100,
          answerCount: 4,
          studentUsername: student.username,
        };
      }

      if (shouldSend) {
        try {
          const res = await fetch(`${API_URL}/api/events`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ appId: 'lms', eventType, payload }),
          });
          console.log(`    ↳ Sent ${eventType} -> HTTP ${res.status}`);
        } catch (err) {
          console.log(`    ↳ Notice: Could not reach ${API_URL} directly: ${err.message}`);
        }
      }
    }
  }

  if (!shouldSend) {
    console.log('\nDry run complete. Pass --send to dispatch live HTTP events to the rack server.');
  }
}

dispatchEvents();

