import { useState } from 'react';

type ExamQuestion = {
  id: string;
  prompt: string;
  options: [string, string, string, string];
};

type ExamSection = {
  id: string;
  title: string;
  questions: ExamQuestion[];
};

const EXAM_SECTIONS: ExamSection[] = [
  {
    id: 'apc1-hw',
    title: 'A+ Core 1 — Hardware & Components',
    questions: [
      {
        id: 'apc1-hw-01',
        prompt: 'Which RAM type is standard in modern desktop computers?',
        options: ['DDR2', 'SDRAM', 'DDR4', 'Rambus RDRAM'],
      },
      {
        id: 'apc1-hw-02',
        prompt: 'What is the primary function of a power supply unit (PSU)?',
        options: [
          'Convert AC power to DC for computer components',
          'Store data when the computer is powered off',
          'Provide wireless network connectivity',
          'Regulate CPU temperature via voltage throttling',
        ],
      },
      {
        id: 'apc1-hw-03',
        prompt: 'Which storage interface provides the fastest data transfer in modern PCs?',
        options: ['SATA I', 'SATA II', 'SATA III', 'NVMe PCIe'],
      },
      {
        id: 'apc1-hw-04',
        prompt: 'A technician must add a second monitor to a workstation. What component is most likely needed?',
        options: [
          'Sound card',
          'Discrete GPU with multiple display outputs',
          'Network interface card',
          'USB hub',
        ],
      },
      {
        id: 'apc1-hw-05',
        prompt: 'What does the acronym BIOS stand for?',
        options: [
          'Basic Input/Output Storage',
          'Binary Input/Output System',
          'Basic Input/Output System',
          'Binary Integrated Operating System',
        ],
      },
      {
        id: 'apc1-hw-06',
        prompt: 'Which of the following is a non-volatile storage medium?',
        options: ['SSD', 'CPU cache', 'RAM', 'CPU registers'],
      },
      {
        id: 'apc1-hw-07',
        prompt: 'What socket do most modern AMD desktop CPUs use?',
        options: ['LGA 1700', 'AM5', 'LGA 2066', 'FM2+'],
      },
      {
        id: 'apc1-hw-08',
        prompt: 'A PC will not POST and shows a memory error LED. What is the first action to take?',
        options: [
          'Replace the motherboard',
          'Re-flash the BIOS firmware',
          'Replace the power supply',
          'Reseat the RAM modules',
        ],
      },
    ],
  },
  {
    id: 'apc1-net',
    title: 'A+ Core 1 — Networking Fundamentals',
    questions: [
      {
        id: 'apc1-net-01',
        prompt: 'Which device operates at Layer 2 and forwards frames based on MAC addresses?',
        options: ['Router', 'Switch', 'Hub', 'Modem'],
      },
      {
        id: 'apc1-net-02',
        prompt: 'Which IPv4 range defines the Class B private address space?',
        options: ['10.0.0.0/8', '192.168.0.0/16', '172.0.0.0/8', '172.16.0.0/12'],
      },
      {
        id: 'apc1-net-03',
        prompt: 'Which protocol automatically assigns IP addresses to network clients?',
        options: ['DHCP', 'DNS', 'ARP', 'SMTP'],
      },
      {
        id: 'apc1-net-04',
        prompt: 'A user can ping IP addresses but cannot reach websites by name. Which service is failing?',
        options: ['DHCP', 'HTTP', 'DNS', 'SMTP'],
      },
      {
        id: 'apc1-net-05',
        prompt: 'A subnet mask of 255.255.255.0 indicates that the subnet supports how many hosts?',
        options: [
          'It is a Class A network',
          'Up to 254 hosts on the subnet',
          'No subnet — flat network only',
          'The network uses IPv6 addressing',
        ],
      },
      {
        id: 'apc1-net-06',
        prompt: 'Which wireless standard operates exclusively on 5 GHz and supports speeds up to 3.5 Gbps?',
        options: ['802.11ac (Wi-Fi 5)', '802.11b', '802.11g', '802.11n'],
      },
      {
        id: 'apc1-net-07',
        prompt: 'What default port does HTTPS use?',
        options: ['21', '80', '25', '443'],
      },
      {
        id: 'apc1-net-08',
        prompt: 'Which network topology provides the highest fault tolerance by connecting every node to every other node?',
        options: ['Star', 'Bus', 'Mesh', 'Ring'],
      },
    ],
  },
  {
    id: 'apc1-ts',
    title: 'A+ Core 1 — Troubleshooting Basics',
    questions: [
      {
        id: 'apc1-ts-01',
        prompt: 'According to CompTIA best practices, what is the FIRST step in the troubleshooting methodology?',
        options: [
          'Identify the problem',
          'Establish a theory of probable cause',
          'Test the theory',
          'Implement the solution',
        ],
      },
      {
        id: 'apc1-ts-02',
        prompt: 'A laptop display is flickering. After verifying the display cable, what should be checked next?',
        options: [
          'Hard drive health',
          'RAM seating',
          'Video driver and display settings',
          'Power supply output',
        ],
      },
      {
        id: 'apc1-ts-03',
        prompt: 'Which tool would a technician use to verify that a network cable has correct wiring?',
        options: ['Toner probe', 'Cable tester', 'Network tap', 'Crimping tool'],
      },
      {
        id: 'apc1-ts-04',
        prompt: 'A PC randomly powers off during intensive workloads. What is the MOST likely cause?',
        options: [
          'Faulty monitor',
          'Corrupt OS files',
          'Bad RAM module',
          'Overheating CPU or GPU',
        ],
      },
      {
        id: 'apc1-ts-05',
        prompt: 'After replacing a failed hard drive and restoring from backup, what CompTIA step is this?',
        options: [
          'Verify full system functionality and preventive measures',
          'Establish a theory of probable cause',
          'Document findings and outcomes',
          'Identify the problem',
        ],
      },
      {
        id: 'apc1-ts-06',
        prompt: 'A printer produces blank pages. The driver is confirmed correct. What should be checked next?',
        options: [
          'Network connectivity',
          'OS version compatibility',
          'Ink or toner cartridge',
          'Monitor resolution settings',
        ],
      },
    ],
  },
  {
    id: 'apc2-os',
    title: 'A+ Core 2 — Operating Systems',
    questions: [
      {
        id: 'apc2-os-01',
        prompt: 'Which Windows command displays the current IP configuration of network interfaces?',
        options: ['netstat', 'nslookup', 'ping', 'ipconfig'],
      },
      {
        id: 'apc2-os-02',
        prompt: 'Which Windows utility allows a technician to view and terminate running processes?',
        options: ['Device Manager', 'Task Manager', 'Event Viewer', 'System Configuration'],
      },
      {
        id: 'apc2-os-03',
        prompt: 'Which file system is the default for modern Windows installations?',
        options: ['NTFS', 'FAT32', 'exFAT', 'EXT4'],
      },
      {
        id: 'apc2-os-04',
        prompt: "A Windows PC shows 'Missing OS' on boot, but BIOS detects the drive. What is the next step?",
        options: [
          'Reinstall Windows immediately',
          'Replace the hard drive',
          'Run Startup Repair from Windows Recovery Environment',
          'Check RAM modules',
        ],
      },
      {
        id: 'apc2-os-05',
        prompt: 'Which macOS utility is equivalent to Windows Device Manager for viewing hardware info?',
        options: ['Finder', 'System Information', 'Activity Monitor', 'Terminal'],
      },
      {
        id: 'apc2-os-06',
        prompt: 'Which built-in Windows tool allows scheduling a task to run automatically each night?',
        options: ['Services.msc', 'Msconfig', 'Regedit', 'Task Scheduler'],
      },
    ],
  },
  {
    id: 'apc2-sec',
    title: 'A+ Core 2 — Security Fundamentals',
    questions: [
      {
        id: 'apc2-sec-01',
        prompt: 'Which type of malware encrypts user files and demands payment for a decryption key?',
        options: ['Adware', 'Spyware', 'Ransomware', 'Rootkit'],
      },
      {
        id: 'apc2-sec-02',
        prompt: 'What is the purpose of multi-factor authentication (MFA)?',
        options: [
          'Require users to verify identity using two or more independent factors',
          'Encrypt data stored on disk',
          'Filter outbound network traffic',
          'Generate hardware OTP tokens exclusively',
        ],
      },
      {
        id: 'apc2-sec-03',
        prompt: 'Which attack sends a massive volume of traffic to overwhelm and disable a target server?',
        options: ['Phishing', 'Man-in-the-middle', 'SQL injection', 'Denial of Service (DoS)'],
      },
      {
        id: 'apc2-sec-04',
        prompt: 'A user receives an email from "IT Support" asking them to click a link and reset their password. What is this?',
        options: ['Brute force attack', 'Phishing', 'Spear phishing', 'Vishing'],
      },
      {
        id: 'apc2-sec-05',
        prompt: 'Which Windows feature encrypts entire volumes and requires a recovery key for access?',
        options: ['Windows Defender', 'UAC', 'BitLocker', 'SmartScreen'],
      },
      {
        id: 'apc2-sec-06',
        prompt: 'Which statement BEST describes the principle of least privilege?',
        options: [
          'Grant users only the minimum access required to perform their job',
          'Give all users administrator rights to reduce IT support calls',
          'Share passwords among a team for operational efficiency',
          'Disable accounts inactive for more than 90 days',
        ],
      },
    ],
  },
  {
    id: 'nocti-safe',
    title: 'NOCTI — Safety & Professionalism',
    questions: [
      {
        id: 'nocti-safe-01',
        prompt: 'What is the purpose of an ESD wrist strap when working on computer components?',
        options: [
          'Secure components during installation',
          'Prevent electrostatic discharge from damaging sensitive components',
          'Improve grip when handling circuit boards',
          'Ground the power supply before removal',
        ],
      },
      {
        id: 'nocti-safe-02',
        prompt: 'Before working inside a computer, a technician should ALWAYS:',
        options: [
          'Power off and unplug the computer from the outlet',
          'Remove the hard drive first',
          'Enable onboard battery mode',
          'Enable Administrator mode in the OS',
        ],
      },
      {
        id: 'nocti-safe-03',
        prompt: 'A customer is upset about a repair estimate. How should a professional technician respond?',
        options: [
          'Argue that the estimate is entirely fair',
          'Immediately escalate to management without engaging',
          'Refuse further service and end the conversation',
          'Listen actively, acknowledge their concerns, and calmly explain the reasoning',
        ],
      },
    ],
  },
  {
    id: 'nocti-it',
    title: 'NOCTI — General IT Concepts',
    questions: [
      {
        id: 'nocti-it-01',
        prompt: "What does 'cloud computing' mean in a professional IT context?",
        options: [
          'Storing files on a local NAS device on the company network',
          'Running all applications on a personal laptop offline',
          'Accessing computing resources (servers, storage, apps) via the internet on demand',
          'Using wireless networking inside an office building',
        ],
      },
      {
        id: 'nocti-it-02',
        prompt: "Which component is considered the computer's brain, performing arithmetic and logic operations?",
        options: ['RAM', 'CPU', 'GPU', 'SSD'],
      },
      {
        id: 'nocti-it-03',
        prompt: 'What is the correct order of OSI model layers from bottom (Layer 1) to top (Layer 7)?',
        options: [
          'Physical, Data Link, Network, Transport, Session, Presentation, Application',
          'Application, Presentation, Session, Transport, Network, Data Link, Physical',
          'Physical, Network, Data Link, Transport, Session, Presentation, Application',
          'Data Link, Physical, Network, Transport, Application, Session, Presentation',
        ],
      },
    ],
  },
];

const ALL_QUESTIONS = EXAM_SECTIONS.flatMap((s) => s.questions);
const TOTAL = ALL_QUESTIONS.length; // 40

type PlacementResult = {
  totalScore: number;
  placementTier: string;
  recommendedTrack: string;
  recommendedStart: string;
  domainScores: Record<string, number>;
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

type Props = {
  apiUrl: string;
};

export default function EntranceExam({ apiUrl }: Props) {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PlacementResult | null>(null);
  const [alreadyTaken, setAlreadyTaken] = useState(false);

  const answered = Object.keys(answers).length;
  const canSubmit = answered === TOTAL && !submitting;

  const handleSelect = (questionId: string, optionIndex: number) => {
    if (result || alreadyTaken) return;
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleSubmit = async () => {
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);

    const payload = Object.entries(answers).map(([questionId, selectedOption]) => ({
      questionId,
      selectedOption,
    }));

    try {
      const res = await fetch(`${apiUrl}/api/competency/entrance-exam`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: payload }),
      });

      if (res.status === 409) {
        setAlreadyTaken(true);
        return;
      }

      if (!res.ok) {
        const body = await res.json().catch(() => ({})) as { message?: string };
        setError(body.message ?? 'Submission failed. Please try again.');
        return;
      }

      const data = await res.json() as PlacementResult;
      setResult(data);
    } catch {
      setError('Network error. Check your connection and try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Already taken ──────────────────────────────────────────────────────────
  if (alreadyTaken) {
    return (
      <div className="entrance-exam__done">
        <div className="entrance-exam__done-icon">✓</div>
        <h2>Exam Already Completed</h2>
        <p>You have already taken the placement exam. Your results are saved to your profile.</p>
        <a href="/competency" className="btn btn--primary">
          View My Competency Profile
        </a>
      </div>
    );
  }

  // ── Results screen ─────────────────────────────────────────────────────────
  if (result) {
    const tier = result.placementTier;
    const tierColor = TIER_COLORS[tier] ?? '#94a3b8';

    return (
      <div className="entrance-exam__results">
        <div className="entrance-exam__results-header">
          <h2>Placement Results</h2>
          <p className="entrance-exam__results-sub">
            Your answers have been scored and your competency baseline has been recorded.
          </p>
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

        <div className="entrance-exam__cta">
          <a href="/competency" className="btn btn--primary">
            View My Competency Profile →
          </a>
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

          {section.questions.map((q, qi) => {
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

      {error && <p className="entrance-exam__error" role="alert">{error}</p>}

      <div className="entrance-exam__submit-row">
        {!canSubmit && answered < TOTAL && (
          <p className="entrance-exam__submit-hint">
            Answer all {TOTAL} questions to submit.
          </p>
        )}
        <button
          className="btn btn--primary btn--lg"
          disabled={!canSubmit}
          onClick={handleSubmit}
        >
          {submitting ? 'Submitting…' : 'Submit Exam'}
        </button>
      </div>
    </div>
  );
}
