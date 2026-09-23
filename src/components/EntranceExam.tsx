import { useEffect, useState } from 'react';
import { emitEvent, getUserPrefix, type CISDomainTag } from '../lib/events';

type ExamQuestion = {
  id: string;
  prompt: string;
  options: [string, string, string, string];
  correctIndex: 0 | 1 | 2 | 3;
};

type ExamSection = {
  id: string;
  title: string;
  questions: ExamQuestion[];
};

const EXAM_SECTIONS: ExamSection[] = [
  {
    id: 'pct-fundamentals',
    title: 'A+ — Computing Fundamentals',
    questions: [
      {
        id: 'pct-four-functions-of-computer',
        prompt: 'Which of the following correctly lists the four basic functions of a computer?',
        options: ['Receive, Decode, Execute, Transmit', 'Entry, Execution, Retention, Response', 'Input, Calculation, Memory, Display', 'Input, Processing, Storage, Output'],
        correctIndex: 3,
      },
      {
        id: 'pct-fetch-decode-execute-cycle',
        prompt: 'What is the fetch-decode-execute cycle?',
        options: ['The cycle by which the operating system loads drivers during startup', 'The sequence a hard drive uses to read and write data sectors', 'The routine performed by the BIOS during the power-on self-test', 'The process by which a CPU retrieves, interprets, and carries out instructions from memory'],
        correctIndex: 3,
      },
      {
        id: 'pct-binary-to-decimal-1010',
        prompt: 'What is the decimal value of the binary number 1010?',
        options: ['8', '12', '14', '10'],
        correctIndex: 3,
      },
      {
        id: 'pct-bits-per-byte',
        prompt: 'How many bits are in one byte?',
        options: ['4', '16', '8', '2'],
        correctIndex: 2,
      },
    ],
  },
  {
    id: 'pct-hardware',
    title: 'A+ — Hardware & Components',
    questions: [
      {
        id: 'pct-am5-socket-ryzen7000',
        prompt: 'A client wants to install a new AMD Ryzen 7000 series processor into an existing AM4 motherboard, but the CPU will not seat in the socket. What is the most likely cause?',
        options: ['The BIOS needs to be updated before the CPU will be recognized', 'The CPU cooler is preventing the socket latch from opening', 'The Ryzen 7000 series uses the AM5 socket, which is physically different from AM4', 'The AM4 board requires a BIOS flashback before accepting newer CPUs'],
        correctIndex: 2,
      },
      {
        id: 'pct-ddr5-ddr4-incompatible-slots',
        prompt: 'A client wants to add DDR5 RAM to a motherboard that only has DDR4 slots. What should a technician tell them?',
        options: ['This is possible with a DDR4-to-DDR5 adapter kit', 'DDR5 will work but the system will run it at DDR4 speeds', 'DDR5 and DDR4 use different physical slots and are incompatible — a new motherboard and CPU are required', 'This works only if the DDR5 kit matches the existing DDR4 capacity'],
        correctIndex: 2,
      },
      {
        id: 'pct-psu-sizing-420w-load',
        prompt: 'A system has a calculated total power draw of 420W. Which power supply best follows proper PSU sizing practice?',
        options: ['430W, just above the load for maximum efficiency', '500W, providing 80W of headroom', '1200W, since maximum wattage provides the most stable power delivery', '650W, which puts the system in roughly the 60-65% load range for efficiency and headroom'],
        correctIndex: 3,
      },
      {
        id: 'pct-lga1700-socket-12th-13th-gen',
        prompt: 'Intel 12th and 13th generation Core processors use which CPU socket?',
        options: ['LGA1200', 'AM5', 'LGA1851', 'LGA1700'],
        correctIndex: 3,
      },
      {
        id: 'pct-cmos-battery-purpose',
        prompt: 'What is the purpose of the CMOS battery on a motherboard?',
        options: ['It powers the CPU when the main power supply fails', 'It acts as a surge protector for the motherboard circuitry', 'It provides backup power to RAM so data is not lost during power outages', 'It maintains power to the BIOS chip so BIOS settings and the real-time clock are preserved when the system is off'],
        correctIndex: 3,
      },
      {
        id: 'pct-xmp-profile-ram-speed',
        prompt: 'A technician installs 32GB of DDR4-3600 RAM, but the system reports it running at only 2133 MHz. What is the most likely fix?',
        options: ['Return the RAM — it is defective and cannot run at its rated speed', 'Reinstall Windows so the OS can detect the correct RAM speed', 'Enable the XMP profile in the BIOS settings', 'Install the RAM in different slots to access the higher speed'],
        correctIndex: 2,
      },
    ],
  },
  {
    id: 'pct-os',
    title: 'A+ — Operating Systems',
    questions: [
      {
        id: 'pct-task-manager-processes-tab',
        prompt: "A technician needs to identify which processes are consuming the most CPU on a client's machine. Which Task Manager tab shows this information?",
        options: ['Performance', 'Processes', 'Startup', 'Details'],
        correctIndex: 1,
      },
      {
        id: 'pct-device-manager-purpose',
        prompt: 'What is the primary purpose of Device Manager in Windows?',
        options: ['To manage user accounts and permissions', 'To manage disk partitions and drive letters', 'To configure network adapter IP settings', 'To view, update, disable, and troubleshoot hardware devices and their drivers'],
        correctIndex: 3,
      },
      {
        id: 'pct-clean-install-vs-upgrade',
        prompt: 'What is the primary difference between a clean install and an in-place upgrade of Windows?',
        options: ['A clean install keeps all existing applications; an upgrade erases everything', 'A clean install is faster because it skips driver installation', 'A clean install erases the drive and starts fresh; an upgrade preserves existing applications, files, and settings', 'An upgrade is only available through Windows Update'],
        correctIndex: 2,
      },
      {
        id: 'pct-gpt-required-for-uefi',
        prompt: 'A technician sets up a new system with a UEFI motherboard and a 3TB drive. Which partition table type is required for a UEFI boot?',
        options: ['MBR — UEFI only supports MBR partitions', 'Either MBR or GPT can be used interchangeably on UEFI systems', 'GPT — UEFI requires GPT, and MBR cannot address drives larger than 2TB', 'GUID, a special format required only for UEFI installations'],
        correctIndex: 2,
      },
      {
        id: 'pct-windows11-tpm2-requirement',
        prompt: 'Windows 11 requires which hardware component that Windows 10 does not mandate for installation?',
        options: ['A dedicated GPU', 'TPM 2.0', 'NVMe storage', 'UEFI with Secure Boot enabled only'],
        correctIndex: 1,
      },
    ],
  },
  {
    id: 'pct-troubleshooting',
    title: 'A+ — Troubleshooting',
    questions: [
      {
        id: 'pct-troubleshooting-step1-identify',
        prompt: 'What is Step 1 of the CompTIA troubleshooting methodology?',
        options: ['Establish a theory of probable cause', 'Test the theory to determine the cause', 'Identify the problem', 'Document findings, actions, and outcomes'],
        correctIndex: 2,
      },
      {
        id: 'pct-symptom-vs-cause',
        prompt: 'What is the difference between a symptom and the cause of a problem?',
        options: ['There is no difference — symptoms and causes are the same thing', 'The cause is what the user reports; the symptom is what the technician discovers through testing', 'Symptoms only apply to hardware failures; software problems have causes but no symptoms', 'A symptom is the observable effect the user reports or the technician sees; the cause is the underlying condition that produces that symptom'],
        correctIndex: 3,
      },
      {
        id: 'pct-no-power-first-check',
        prompt: 'A desktop will not power on at all — no fans, no LEDs, nothing happens. What should a technician verify first?',
        options: ['Reseat the RAM modules', 'Remove and reseat the GPU', 'Disconnect all storage devices and attempt to power on', 'Confirm the rear PSU power switch is on and the power cable is properly connected'],
        correctIndex: 3,
      },
      {
        id: 'pct-random-shutdown-overheating',
        prompt: 'A client reports their computer shuts down randomly after 20 to 30 minutes of use, then works fine immediately after restarting. What is the most likely cause?',
        options: ['A corrupted Windows update is causing scheduled shutdowns', 'The hard drive is entering hibernation mode', 'The power button is sticking and accidentally shutting the system down', 'Overheating — the CPU or GPU reaches a critical temperature and the system shuts down as a protective measure'],
        correctIndex: 3,
      },
      {
        id: 'pct-safe-mode-purpose',
        prompt: 'What is the primary purpose of Safe Mode in Windows?',
        options: ['To run Windows with maximum performance settings for diagnostic purposes', 'To create a backup of system files before making changes', 'To load Windows with only essential drivers and services, so a technician can diagnose and remove software causing problems in normal mode', 'To run a hardware memory test without loading the OS'],
        correctIndex: 2,
      },
      {
        id: 'pct-startup-repair-location',
        prompt: 'Where does a technician find Startup Repair for a Windows system that fails to boot?',
        options: ['In the Windows Settings app under Recovery', 'In the Windows Recovery Environment (WinRE) under Troubleshoot > Advanced Options', 'By pressing F8 during POST to access the repair console', 'In Device Manager under System Recovery Tools'],
        correctIndex: 1,
      },
    ],
  },
  {
    id: 'pct-customer',
    title: 'A+ — Security & Professionalism',
    questions: [
      {
        id: 'pct-active-listening-vague-client',
        prompt: 'A client is explaining a computer problem in vague terms. Which active listening technique best helps the technician gather useful information?',
        options: ['Interrupt politely to ask for the specific error code so the explanation can proceed technically', 'Let the client finish speaking, then ask clarifying questions while summarizing what you heard to confirm understanding', 'Begin diagnosing while the client talks to save time', 'Take notes and say nothing until the client is done, then begin the repair immediately'],
        correctIndex: 1,
      },
      {
        id: 'pct-windows-defender-function',
        prompt: 'What is the primary function of Windows Defender in a modern Windows installation?',
        options: ['It monitors network traffic for intrusion attempts', 'It blocks unauthorized applications from being installed', 'It encrypts user files to prevent unauthorized access', 'It provides real-time antivirus and antimalware protection built into the operating system'],
        correctIndex: 3,
      },
      {
        id: 'pct-ransomware-identification',
        prompt: 'A client has lost access to all their files and sees a message demanding payment in cryptocurrency to restore them. What type of malware caused this?',
        options: ['Adware', 'Spyware', 'Ransomware', 'Worm'],
        correctIndex: 2,
      },
      {
        id: 'pct-esd-wrist-strap-purpose',
        prompt: 'What is the primary purpose of an antistatic wrist strap?',
        options: ['To equalize the electrical charge between the technician and the work surface, preventing static discharge', 'To protect the technician from electrical shock', 'To ground excess current from the power supply', 'To shield components from magnetic fields'],
        correctIndex: 0,
      },
    ],
  },
  {
    id: 'net-fundamentals',
    title: 'Net+ — Networking Concepts',
    questions: [
      {
        id: 'net-osi-not-a-layer',
        prompt: 'Which of the following is NOT one of the seven layers of the OSI model?',
        options: ['Transfer', 'Physical', 'Presentation', 'Data Link'],
        correctIndex: 0,
      },
      {
        id: 'net-osi-physical-layer-function',
        prompt: 'Which OSI layer defines the electrical and physical specifications for network devices, such as cabling and connectors?',
        options: ['Transport', 'Network', 'Physical', 'Presentation'],
        correctIndex: 2,
      },
      {
        id: 'net-ipv4-address-space-size',
        prompt: 'How many possible IPv4 addresses exist in the 32-bit address space?',
        options: ['2,147,483,648', '8,589,934,592', '17,179,869,184', '4,294,967,296'],
        correctIndex: 3,
      },
      {
        id: 'net-apipa-auto-assigned-address',
        prompt: 'A workstation cannot reach a DHCP server and self-assigns an address in the 169.254.0.0/16 range. What is this called?',
        options: ['CIDR', 'APIPA', 'MAC address', 'EUI-64'],
        correctIndex: 1,
      },
      {
        id: 'net-loopback-address-identification',
        prompt: "Which IPv4 address is reserved as the loopback address for testing a device's own network stack?",
        options: ['127.0.0.1', '10.0.0.1', '169.254.0.1', '192.168.0.1'],
        correctIndex: 0,
      },
      {
        id: 'net-https-port-number',
        prompt: 'Which port number is reserved for HTTPS traffic?',
        options: ['110', '445', '443', '587'],
        correctIndex: 2,
      },
      {
        id: 'net-dhcp-purpose',
        prompt: 'What is the primary function of DHCP on a network?',
        options: ['It verifies there are no collisions between MAC addresses', 'It automatically assigns IP addresses to devices that connect to a network', 'It assigns MAC addresses to devices on boot', 'It encrypts traffic between devices on the network'],
        correctIndex: 1,
      },
      {
        id: 'net-dns-full-name',
        prompt: 'What is the primary function of DNS on a network?',
        options: ['It translates human-readable domain names into IP addresses', 'It assigns IP addresses automatically to new devices', 'It encrypts traffic between a client and a web server', 'It monitors network bandwidth usage'],
        correctIndex: 0,
      },
    ],
  },
  {
    id: 'net-implementation',
    title: 'Net+ — Network Implementation',
    questions: [
      {
        id: 'net-switch-osi-layer',
        prompt: 'At which OSI layer does a standard network switch primarily operate?',
        options: ['Layer 1', 'Layer 2', 'Layer 3', 'Layer 4'],
        correctIndex: 1,
      },
      {
        id: 'net-load-balancer-function',
        prompt: 'What is the primary function of a load balancer?',
        options: ['Hotspots that extend wireless range', 'It efficiently distributes incoming network traffic across a group of backend servers', 'Hot-swap bays for replacing failed drives without downtime', 'A device that modulates and demodulates analog signals'],
        correctIndex: 1,
      },
      {
        id: 'net-static-routing-definition',
        prompt: 'What is static routing?',
        options: ['A routing method that routes packets through fixed, manually configured paths', 'A routing method that routes packets based on real-time electrical interference in the air', 'A routing method that dynamically changes routes based on current network conditions', 'A method that only applies to wireless networks'],
        correctIndex: 0,
      },
      {
        id: 'net-bgp-core-internet-protocol',
        prompt: 'Which routing protocol is considered the core routing protocol of the Internet, used to exchange routes between autonomous systems?',
        options: ['BGP', 'RIP', 'OSPF', 'EIGRP'],
        correctIndex: 0,
      },
      {
        id: 'net-ospf-link-state-shortest-path',
        prompt: 'Which routing protocol finds the best path from source to destination using its own shortest-path-first, link-state algorithm?',
        options: ['OSPF', 'RIP', 'EIGRP', 'BGP'],
        correctIndex: 0,
      },
      {
        id: 'net-ssid-definition',
        prompt: 'What is an SSID?',
        options: ['The password used to join the WLAN', 'The name of the wireless (WLAN) network', 'The serial number printed on the access point', "The LAN's internal network name"],
        correctIndex: 1,
      },
      {
        id: 'net-24ghz-channel-count',
        prompt: 'In the United States, the 2.4GHz Wi-Fi frequency band is divided into how many channels?',
        options: ['7', '11', '25', '45'],
        correctIndex: 1,
      },
    ],
  },
  {
    id: 'net-operations',
    title: 'Net+ — Network Operations',
    questions: [
      {
        id: 'net-bandwidth-definition',
        prompt: 'What does bandwidth measure on a network?',
        options: ['The maximum transfer throughput capacity of a network, measured in bits per second', 'The delay between sending and receiving a packet', 'The variation in packet arrival times', 'The percentage of time a network is operational'],
        correctIndex: 0,
      },
      {
        id: 'net-baseline-definition',
        prompt: 'What is the standard, expected level of performance for a device or network called?',
        options: ['Baseline', 'Bottom line', 'Availability', 'Data flow level'],
        correctIndex: 0,
      },
      {
        id: 'net-policies-vs-procedures',
        prompt: 'In network documentation, what best describes a policy versus a procedure?',
        options: ['A policy states how people are expected to behave and how the network should be configured and operated; a procedure is the specific step-by-step description of how to carry that out', 'A policy is a step-by-step technical guide; a procedure is a high-level statement of intent', 'Policies and procedures are interchangeable terms for the same document', 'A policy applies only to hardware; a procedure applies only to software'],
        correctIndex: 0,
      },
      {
        id: 'net-redundancy-definition',
        prompt: 'What is redundancy in the context of network design?',
        options: ['The duplication of components or functions of a system to increase reliability', 'A firewall rule that blocks duplicate traffic', 'The process of reengineering an outdated network', 'A method of replicating only user data, never hardware'],
        correctIndex: 0,
      },
    ],
  },
  {
    id: 'net-security',
    title: 'Net+ — Network Security',
    questions: [
      {
        id: 'net-cia-confidentiality-definition',
        prompt: 'In the CIA triad, what does confidentiality refer to?',
        options: ['Assurance of how accurate and trustworthy data is', 'Access to data is restricted to only those who need it', 'Data is protected from being changed', 'Data is available to authorized users when needed'],
        correctIndex: 1,
      },
      {
        id: 'net-vulnerability-definition',
        prompt: 'What is a vulnerability, as distinct from a threat or an exploit?',
        options: ['A person or condition capable of causing harm to a system', 'A weakness in software, hardware, or personnel that could be exploited', 'A tool or piece of code used to actively attack a weakness', 'A patch released to fix a known weakness'],
        correctIndex: 1,
      },
      {
        id: 'net-network-segmentation-definition',
        prompt: 'What is network segmentation?',
        options: ['Encrypting all traffic between two segments of a network', 'Breaking a network into smaller segments for better performance and security', 'A defense-in-depth strategy limited to physical security controls', 'The process of assigning IPv6 addresses instead of IPv4'],
        correctIndex: 1,
      },
    ],
  },
  {
    id: 'net-troubleshooting',
    title: 'Net+ — Network Troubleshooting',
    questions: [
      {
        id: 'net-troubleshooting-first-step',
        prompt: 'When identifying a network problem, what is the first step in correcting the issue?',
        options: ['Reboot the network router', 'Consider multiple approaches to the problem', 'Gather information about the problem', 'Escalate to a senior network administrator'],
        correctIndex: 2,
      },
      {
        id: 'net-ping-command-purpose',
        prompt: 'What is the primary purpose of the ping command?',
        options: ['To determine what ports are open on a remote host', 'To determine the default gateway of a device', 'To determine whether a target host can be reached', 'To determine the operating system running on a remote host'],
        correctIndex: 2,
      },
      {
        id: 'net-ipconfig-windows-command',
        prompt: 'On a Windows machine, which command displays the current IP address, DNS configuration, and default gateway?',
        options: ['ipconfig', 'ifconfig', 'ping', 'nmap'],
        correctIndex: 0,
      },
    ],
  },
];

const ALL_QUESTIONS = EXAM_SECTIONS.flatMap((s) => s.questions);
const TOTAL = ALL_QUESTIONS.length; // 50

// Domain sections below this score are treated as "not yet mastered" for placement purposes.
const GATE_THRESHOLD = 70;

type DomainBreakdown = {
  domainId: string;
  moduleId: string;
  track: string;
  label: string;
  correct: number;
  total: number;
  percent: number;
};

type PlacementResult = {
  totalScore: number;
  placementTier: string;
  recommendedTrack: string;
  recommendedStart: string;
  domainBreakdown: DomainBreakdown[];
};

const TIER_LABELS: Record<string, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
  accelerated: 'Accelerated',
};

const TIER_COLORS: Record<string, string> = {
  beginner: '#EF9F27',
  intermediate: '#378ADD',
  advanced: '#00C875',
  accelerated: '#00FF41',
};

function moduleIdForSection(sectionId: string): string {
  return sectionId.replace('-', '.');
}

function trackForSection(sectionId: string): string {
  return sectionId.startsWith('pct-') ? 'pc-technician' : 'network-engineer';
}

// Scored entirely client-side so results are instant and don't depend on the
// hub's scoring engine being reachable. See emitPlacementEvent() below for the
// best-effort, non-blocking notification sent to the hub for teacher visibility.
function scoreExam(answers: Record<string, number>): PlacementResult {
  let totalCorrect = 0;

  const domainBreakdown: DomainBreakdown[] = EXAM_SECTIONS.map((section) => {
    const total = section.questions.length;
    const correct = section.questions.filter((q) => answers[q.id] === q.correctIndex).length;
    totalCorrect += correct;
    return {
      domainId: section.id,
      moduleId: moduleIdForSection(section.id),
      track: trackForSection(section.id),
      label: section.title.replace(/^A\+ — |^Net\+ — /, ''),
      correct,
      total,
      percent: Math.round((correct / total) * 100),
    };
  });

  const totalScore = Math.round((totalCorrect / TOTAL) * 100);

  let placementTier: string;
  if (totalScore >= 90) placementTier = 'accelerated';
  else if (totalScore >= 75) placementTier = 'advanced';
  else if (totalScore >= 50) placementTier = 'intermediate';
  else placementTier = 'beginner';

  const weakestDomain = domainBreakdown.find((d) => d.percent < GATE_THRESHOLD);

  const recommendedTrack = weakestDomain ? weakestDomain.track : 'network-engineer';
  const recommendedStart = weakestDomain
    ? `${weakestDomain.moduleId} — ${weakestDomain.label}`
    : 'You scored above the gate threshold on every domain — talk to your instructor about the competency placement exam for network-engineer.';

  return { totalScore, placementTier, recommendedTrack, recommendedStart, domainBreakdown };
}

const STORAGE_KEY = 'lms_entrance_exam_result';

function loadStoredResult(): PlacementResult | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = window.localStorage.getItem(`${getUserPrefix()}${STORAGE_KEY}`);
    return raw ? (JSON.parse(raw) as PlacementResult) : null;
  } catch {
    return null;
  }
}

function storeResult(result: PlacementResult): void {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(`${getUserPrefix()}${STORAGE_KEY}`, JSON.stringify(result));
  } catch {
    // localStorage unavailable — result still displays for this session
  }
}

// Fire-and-forget notification to the hub for the teacher-facing dashboards.
// Never blocks or gates the student-facing result — see src/lib/events.ts.
function emitPlacementEvent(result: PlacementResult, apiUrl: string): void {
  const domains: CISDomainTag[] = result.domainBreakdown.map((d) => ({
    domainId: d.moduleId,
    weight: d.total / TOTAL,
  }));
  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.placement_exam_completed',
      payload: {
        domains,
        contentType: 'placement_exam',
        contentId: 'entrance-exam-aplus-netplus-v2',
        score: result.totalScore,
        maxScore: 100,
        placementTier: result.placementTier,
        recommendedTrack: result.recommendedTrack,
        recommendedStart: result.recommendedStart,
      },
    },
    apiUrl,
  );
}

type Props = {
  apiUrl: string;
};

export default function EntranceExam({ apiUrl }: Props) {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<PlacementResult | null>(null);
  const [restored, setRestored] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    const stored = loadStoredResult();
    if (stored) {
      setResult(stored);
      setRestored(true);
    }
  }, []);

  const answered = Object.keys(answers).length;
  const canSubmit = answered === TOTAL;

  const handleSelect = (questionId: string, optionIndex: number) => {
    if (result) return;
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleRetake = () => {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(`${getUserPrefix()}${STORAGE_KEY}`);
    }
    setResult(null);
    setRestored(false);
    setAnswers({});
    setSubmitError(null);
  };

  const handleSubmit = async () => {
    if (!canSubmit || submitting) return;
    setSubmitting(true);
    setSubmitError(null);

    const scored = scoreExam(answers);
    const payload = Object.entries(answers).map(([questionId, selectedOption]) => ({
      questionId,
      selectedOption,
    }));

    try {
      const res = await fetch(`${apiUrl}/api/competency/entrance-exam`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ answers: payload }),
      });

      if (res.ok) {
        const data = await res.json();
        if (typeof data.totalScore === 'number') {
          scored.totalScore = data.totalScore;
        }
        if (data.placementTier) {
          scored.placementTier = data.placementTier;
        }
        if (data.recommendedTrack) {
          scored.recommendedTrack = data.recommendedTrack;
        }
        if (data.recommendedStart) {
          scored.recommendedStart = data.recommendedStart;
        }
      } else {
        setSubmitError('Offline Mode: Assessment recorded locally. CIS server will sync on reconnect.');
      }
    } catch {
      setSubmitError('Offline Mode: Assessment recorded locally. CIS server will sync on reconnect.');
    } finally {
      storeResult(scored);
      emitPlacementEvent(scored, apiUrl);
      setResult(scored);
      setSubmitting(false);
    }
  };

  // ── Results screen ─────────────────────────────────────────────────────────
  if (result) {
    const tier = result.placementTier;
    const tierColor = TIER_COLORS[tier] ?? '#94a3b8';

    return (
      <div className="entrance-exam__results">
        <div className="entrance-exam__results-header">
          <h2>Placement Results</h2>
          <p className="entrance-exam__results-sub">
            {restored
              ? 'These are your saved results from your last attempt.'
              : 'Your answers have been scored and your competency baseline has been recorded.'}
          </p>
          {submitError && (
            <p className="entrance-exam__results-sub" style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
              {submitError}
            </p>
          )}
        </div>

        <div className="entrance-exam__score-card">
          <div className="entrance-exam__score-number">
            {Math.round(result.totalScore)}%
          </div>
          <div
            className="entrance-exam__tier-badge"
            style={{ color: tierColor, borderColor: tierColor }}
          >
            {TIER_LABELS[tier] ?? tier}
          </div>
        </div>

        <div className="entrance-exam__placement-info">
          <div className="entrance-exam__placement-row">
            <span className="entrance-exam__placement-label">Recommended Track</span>
            <span className="entrance-exam__placement-value">{result.recommendedTrack}</span>
          </div>
          <div className="entrance-exam__placement-row">
            <span className="entrance-exam__placement-label">Suggested Starting Point</span>
            <span className="entrance-exam__placement-value">{result.recommendedStart}</span>
          </div>
        </div>

        <div className="entrance-exam__placement-info">
          <h3 className="entrance-exam__section-title">Domain Breakdown</h3>
          {result.domainBreakdown.map((d) => (
            <div key={d.domainId} className="entrance-exam__placement-row">
              <span className="entrance-exam__placement-label">{d.label}</span>
              <span className="entrance-exam__placement-value">
                {d.correct}/{d.total} ({d.percent}%)
              </span>
            </div>
          ))}
        </div>

        <div className="entrance-exam__cta" style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <a href="/competency" className="btn btn--primary">
            View My Competency Profile →
          </a>
          <button
            type="button"
            className="btn btn--secondary"
            onClick={handleRetake}
          >
            Retake Placement Exam ↺
          </button>
        </div>
      </div>
    );
  }

  // ── Exam form ──────────────────────────────────────────────────────────────
  return (
    <div className="entrance-exam">
      <div className="entrance-exam__progress-bar">
        <div
          className="entrance-exam__progress-fill"
          style={{ width: `${(answered / TOTAL) * 100}%` }}
        />
      </div>
      <p className="entrance-exam__progress-label">
        {answered} / {TOTAL} answered
      </p>

      {EXAM_SECTIONS.map((section) => (
        <section key={section.id} className="entrance-exam__section">
          <h3 className="entrance-exam__section-title">{section.title}</h3>

          {section.questions.map((q) => {
            const globalIndex = ALL_QUESTIONS.findIndex((x) => x.id === q.id);
            const selected = answers[q.id];

            return (
              <div key={q.id} className="entrance-exam__question">
                <p className="entrance-exam__question-prompt">
                  <span className="entrance-exam__question-num">{globalIndex + 1}.</span>{' '}
                  {q.prompt}
                </p>
                <div className="entrance-exam__options" role="radiogroup">
                  {q.options.map((option, idx) => {
                    const isSelected = selected === idx;
                    return (
                      <div
                        key={idx}
                        role="radio"
                        aria-checked={isSelected}
                        tabIndex={0}
                        className={`entrance-exam__option${isSelected ? ' entrance-exam__option--selected' : ''}`}
                        onClick={() => handleSelect(q.id, idx)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') handleSelect(q.id, idx);
                        }}
                      >
                        <span className="entrance-exam__option-letter">
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span className="entrance-exam__option-text">{option}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </section>
      ))}

      <div className="entrance-exam__submit-row">
        {!canSubmit && (
          <p className="entrance-exam__submit-hint">
            Answer all {TOTAL} questions to submit.
          </p>
        )}
        <button
          className="btn btn--primary btn--lg"
          disabled={!canSubmit || submitting}
          onClick={handleSubmit}
        >
          {submitting ? 'Submitting to CIS...' : 'Submit Exam'}
        </button>
      </div>
    </div>
  );
}
