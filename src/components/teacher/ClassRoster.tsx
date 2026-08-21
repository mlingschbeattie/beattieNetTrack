import { useEffect, useState, useMemo } from 'react';

type PATier = 'NOT_STARTED' | 'CRITICAL' | 'NEEDS_WORK' | 'DEVELOPING' | 'ON_TRACK' | 'STRONG' | 'MASTERED';

type CertReadiness = {
  certId: string;
  certName: string;
  readiness: number;
  paTier: PATier;
};

type Student = {
  id?: string;
  username: string;
  displayName: string;
  period: string;
  grade?: number;
  xp?: number;
  level?: number;
  certs: CertReadiness[];
  totalActiveMinutes: number;
  lastActive: string | null;
};

type GapItem = {
  studentUsername: string;
  displayName: string;
  certId: string;
  domainCode: string;
  domainName: string;
  readiness: number;
  deficitMinutes: number;
  priority: 'CRITICAL' | 'NEEDS_WORK';
  coachingAction?: string;
};

const TIER_COLOR: Record<string, string> = {
  NOT_STARTED: '#4A5568',
  CRITICAL:    '#EF4444',
  NEEDS_WORK:  '#F59E0B',
  DEVELOPING:  '#3B82F6',
  ON_TRACK:    '#3B82F6',
  STRONG:      '#10B981',
  MASTERED:    '#10B981',
};

const TIER_LABEL: Record<string, string> = {
  NOT_STARTED: 'Not Started',
  CRITICAL:    'Critical',
  NEEDS_WORK:  'Needs Work',
  DEVELOPING:  'Developing',
  ON_TRACK:    'On Track',
  STRONG:      'Strong',
  MASTERED:    'Mastered',
};

const CERT_NAMES: Record<string, string> = {
  aplus1: 'CompTIA A+ Core 1',
  aplus2: 'CompTIA A+ Core 2',
  netplus: 'CompTIA Network+',
  secplus: 'CompTIA Security+',
  nocti: 'NOCTI / OCA',
};

const CIS_DOMAIN_BENCHMARKS: Array<{ id: string; certTrackId: string; name: string; expectedMinutes: number }> = [
  { id: 'aplus1.mobile', certTrackId: 'aplus1', name: 'Mobile Devices', expectedMinutes: 120 },
  { id: 'aplus1.networking', certTrackId: 'aplus1', name: 'Networking', expectedMinutes: 180 },
  { id: 'aplus1.hardware', certTrackId: 'aplus1', name: 'Hardware', expectedMinutes: 240 },
  { id: 'aplus1.virtualization', certTrackId: 'aplus1', name: 'Virtualization & Cloud', expectedMinutes: 90 },
  { id: 'aplus1.hardware_troubleshooting', certTrackId: 'aplus1', name: 'Hardware & Troubleshooting', expectedMinutes: 180 },
  { id: 'aplus2.os', certTrackId: 'aplus2', name: 'Operating Systems', expectedMinutes: 240 },
  { id: 'aplus2.security', certTrackId: 'aplus2', name: 'Security', expectedMinutes: 120 },
  { id: 'aplus2.software_troubleshooting', certTrackId: 'aplus2', name: 'Software Troubleshooting', expectedMinutes: 150 },
  { id: 'aplus2.ops', certTrackId: 'aplus2', name: 'Operational Procedures', expectedMinutes: 90 },
  { id: 'netplus.networking', certTrackId: 'netplus', name: 'Networking Concepts', expectedMinutes: 180 },
  { id: 'netplus.infrastructure', certTrackId: 'netplus', name: 'Network Infrastructure', expectedMinutes: 150 },
  { id: 'netplus.ops', certTrackId: 'netplus', name: 'Network Operations', expectedMinutes: 120 },
  { id: 'netplus.security', certTrackId: 'netplus', name: 'Network Security', expectedMinutes: 120 },
  { id: 'netplus.troubleshooting', certTrackId: 'netplus', name: 'Network Troubleshooting', expectedMinutes: 90 },
  { id: 'secplus.threats', certTrackId: 'secplus', name: 'Threats & Vulnerabilities', expectedMinutes: 150 },
  { id: 'secplus.architecture', certTrackId: 'secplus', name: 'Architecture & Design', expectedMinutes: 120 },
  { id: 'secplus.implementation', certTrackId: 'secplus', name: 'Implementation', expectedMinutes: 150 },
  { id: 'secplus.ops', certTrackId: 'secplus', name: 'Operations & Incident Response', expectedMinutes: 90 },
  { id: 'secplus.governance', certTrackId: 'secplus', name: 'Governance & Compliance', expectedMinutes: 90 },
  { id: 'nocti.safety', certTrackId: 'nocti', name: 'Safety Procedures', expectedMinutes: 60 },
  { id: 'nocti.hardware', certTrackId: 'nocti', name: 'Hardware Architecture', expectedMinutes: 180 },
  { id: 'nocti.troubleshooting', certTrackId: 'nocti', name: 'Diagnostic Troubleshooting', expectedMinutes: 150 },
  { id: 'nocti.os', certTrackId: 'nocti', name: 'Operating Systems', expectedMinutes: 120 },
  { id: 'nocti.networking', certTrackId: 'nocti', name: 'Network Technology', expectedMinutes: 120 },
  { id: 'nocti.media', certTrackId: 'nocti', name: 'Media & Cabling', expectedMinutes: 90 },
  { id: 'nocti.devices', certTrackId: 'nocti', name: 'Network Devices', expectedMinutes: 90 },
  { id: 'nocti.management', certTrackId: 'nocti', name: 'Network Management', expectedMinutes: 90 },
  { id: 'nocti.tools', certTrackId: 'nocti', name: 'Tools & Testing', expectedMinutes: 60 }
];

const MITRE_TACTICS = [
  { id: 'TA0043', name: 'Reconnaissance', domain: 'secplus.threats', standard: 'CompTIA Sec+' },
  { id: 'TA0001', name: 'Initial Access', domain: 'secplus.threats', standard: 'CompTIA Sec+' },
  { id: 'TA0002', name: 'Execution', domain: 'secplus.implementation', standard: 'CompTIA Sec+' },
  { id: 'TA0003', name: 'Persistence', domain: 'secplus.implementation', standard: 'CompTIA Sec+' },
  { id: 'TA0004', name: 'Privilege Escalation', domain: 'secplus.ops', standard: 'CompTIA Sec+' },
  { id: 'TA0005', name: 'Defense Evasion', domain: 'secplus.ops', standard: 'CompTIA Sec+' },
  { id: 'TA0006', name: 'Credential Access', domain: 'secplus.threats', standard: 'CompTIA Sec+' },
  { id: 'TA0007', name: 'Discovery', domain: 'netplus.troubleshooting', standard: 'CompTIA Net+' },
  { id: 'TA0008', name: 'Lateral Movement', domain: 'netplus.security', standard: 'CompTIA Net+' },
  { id: 'TA0009', name: 'Collection', domain: 'secplus.ops', standard: 'CompTIA Sec+' },
  { id: 'TA0011', name: 'Command and Control', domain: 'netplus.networking', standard: 'CompTIA Net+' },
  { id: 'TA0040', name: 'Impact & Mitigation', domain: 'secplus.governance', standard: 'CompTIA Sec+' }
];

function ReadinessGauge({ value, tier }: { value?: number; tier?: string }) {
  const normTier = (tier?.toUpperCase?.() || 'NOT_STARTED');
  const color = TIER_COLOR[normTier] || '#4A5568';
  const label = TIER_LABEL[normTier] || 'Not Started';
  const pct = Math.min(100, Math.max(0, Math.round(Number(value) || 0)));

  return (
    <div className="flex flex-col gap-1 w-24">
      <div className="flex items-center justify-between text-xs font-mono">
        <span style={{ color }}>{pct}%</span>
        <span className="text-[10px] text-gray-400 truncate max-w-[50px]">{label}</span>
      </div>
      <div className="h-1.5 w-full bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-300"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  );
}

type Props = {
  apiUrl?: string;
};

export default function ClassRoster({ apiUrl }: Props) {
  const baseApiUrl = apiUrl || 'https://api.beattietech.local';
  const [data, setData] = useState<unknown>(null);
  const [gaps, setGaps] = useState<unknown>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [periodFilter, setPeriodFilter] = useState('');
  const [certFilter, setCertFilter] = useState('');
  const [activeTab, setActiveTab] = useState<'roster' | 'gaps' | 'matrix' | 'skyward' | 'mitre'>('roster');
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);

  useEffect(() => {
    // 1. Load class roster
    fetch(`${baseApiUrl}/api/cis/students`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`Class API error (${r.status})`);
        return r.json();
      })
      .then((classData) => {
        setData(classData);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load class roster');
        setLoading(false);
      });

    // 2. Load critical gaps
    fetch(`${baseApiUrl}/api/cis/students?bucket=CRITICAL`, { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : []))
      .then((gapData) => setGaps(gapData || []))
      .catch(() => setGaps([]));
  }, [baseApiUrl]);

  // Adapter for student roster
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawData: any = data;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawList = rawData?.students || rawData?.data?.students || rawData?.data || (Array.isArray(rawData) ? rawData : []);
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const students: Student[] = useMemo(() => {
    return (Array.isArray(rawList) ? rawList : []).map((s: any) => {
      const rawCerts = s?.certTracks || s?.certs || s?.certifications || [];
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const certs = (Array.isArray(rawCerts) ? rawCerts : []).map((c: any) => ({
        certId: c?.certTrackId || c?.certId || c?.cert_id || 'unknown',
        certName: c?.title || c?.certTrackId || c?.certName || c?.name || 'Certification',
        readiness: Number(c?.averageCombinedScore ?? c?.readiness ?? c?.score ?? 0),
        paTier: String(c?.readinessBucket || c?.paTier || c?.pa_tier || 'NOT_STARTED').toUpperCase() as PATier,
      }));

      return {
        id: s?.id,
        username: s?.username || s?.student_username || s?.studentId || s?.id || 'unknown',
        displayName: s?.displayName || s?.display_name || s?.name || s?.username || 'Student',
        period: s?.period != null ? `Period ${s.period}` : '—',
        grade: s?.grade ?? 12,
        xp: s?.xp ?? 0,
        level: s?.level ?? 1,
        certs,
        totalActiveMinutes: Number(s?.totalActiveMinutes ?? s?.total_active_minutes ?? s?.activeMinutes ?? 0),
        lastActive: s?.lastActive || s?.last_active || null,
      };
    });
  }, [rawList]);

  // Adapter for gap items
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawGaps: any = gaps;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawGapList = rawGaps?.students || rawGaps?.data?.students || rawGaps?.data?.gaps || rawGaps?.data || rawGaps?.gaps || (Array.isArray(rawGaps) ? rawGaps : []);
  
  const safeGaps: GapItem[] = useMemo(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return (Array.isArray(rawGapList) ? rawGapList : []).flatMap((g: any) => {
      if (g?.certTracks && Array.isArray(g.certTracks)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return g.certTracks
          .filter((t: any) => t?.readinessBucket === 'CRITICAL' || t?.criticalDomains > 0)
          .map((t: any) => ({
            studentUsername: g?.username || '',
            displayName: g?.displayName || g?.username || 'Student',
            certId: t?.certTrackId || '',
            domainCode: t?.certTrackId || '',
            domainName: CERT_NAMES[t?.certTrackId] || t?.certTrackId || 'Certification Track',
            readiness: Number(t?.averageCombinedScore ?? 0),
            deficitMinutes: Math.max(0, 120 - Math.round(Number(t?.averageCombinedScore ?? 0) * 1.2)),
            priority: 'CRITICAL' as const,
            coachingAction: `Assign targeted hands-on lab and review scenarios in ${CERT_NAMES[t?.certTrackId] || t?.certTrackId}.`,
          }));
      }
      return [{
        studentUsername: g?.studentUsername || g?.student_username || g?.username || '',
        displayName: g?.displayName || g?.display_name || g?.name || g?.studentUsername || 'Student',
        certId: g?.certId || g?.cert_id || '',
        domainCode: g?.domainCode || g?.domain_code || '',
        domainName: g?.domainName || g?.domain_name || 'Domain Topic',
        readiness: Number(g?.readiness ?? 0),
        deficitMinutes: Number(g?.deficitMinutes ?? g?.deficit_minutes ?? 45),
        priority: String(g?.priority || 'NEEDS_WORK').toUpperCase() as 'CRITICAL' | 'NEEDS_WORK',
        coachingAction: g?.coachingAction || 'Review practice questions and execute remediation diagnostic task.',
      }];
    });
  }, [rawGapList]);

  const allCerts = useMemo(() => {
    const defaultTracks = ['aplus1', 'aplus2', 'netplus', 'secplus', 'nocti'];
    const certIds = new Set<string>(defaultTracks);
    for (const s of students) {
      if (Array.isArray(s?.certs)) {
        for (const c of s.certs) {
          if (c?.certId) certIds.add(c.certId);
        }
      }
    }
    return Array.from(certIds);
  }, [students]);

  const uniquePeriods = useMemo(() => {
    const periods = new Set<string>();
    for (const s of students) {
      if (s.period && s.period !== '—') periods.add(s.period);
    }
    return Array.from(periods).sort();
  }, [students]);

  const filteredStudents = useMemo(() => {
    return students.filter((s) => {
      const matchesSearch = !searchQuery || 
        s.displayName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        s.username.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesPeriod = !periodFilter || s.period === periodFilter;
      return matchesSearch && matchesPeriod;
    });
  }, [students, searchQuery, periodFilter]);

  // Executive KPI Calculations
  const totalStudents = students.length;
  const criticalGapsCount = safeGaps.filter(g => g.priority === 'CRITICAL').length;
  const needsWorkCount = safeGaps.filter(g => g.priority === 'NEEDS_WORK').length;
  
  const classAvgScore = useMemo(() => {
    let totalScore = 0;
    let count = 0;
    for (const s of students) {
      for (const c of s.certs) {
        if (c.readiness > 0) {
          totalScore += c.readiness;
          count++;
        }
      }
    }
    return count > 0 ? Math.round(totalScore / count) : 0;
  }, [students]);

  const totalLabMinutes = useMemo(() => {
    return students.reduce((acc, s) => acc + s.totalActiveMinutes, 0);
  }, [students]);

  const examReadyStudentsCount = useMemo(() => {
    return students.filter(s => s.certs.some(c => c.readiness >= 80)).length;
  }, [students]);

  // Export Skyward CSV
  const handleExportSkywardCSV = () => {
    const headers = ['Student ID', 'Username', 'Student Name', 'Period', 'Grade Level', 'Total Active Min', 'Overall Readiness %', 'Letter Grade', 'Skyward Status'];
    const rows = filteredStudents.map(s => {
      const avg = s.certs.length > 0 ? Math.round(s.certs.reduce((a, b) => a + b.readiness, 0) / s.certs.length) : 0;
      let letter = 'F';
      if (avg >= 90) letter = 'A';
      else if (avg >= 80) letter = 'B';
      else if (avg >= 70) letter = 'C';
      else if (avg >= 60) letter = 'D';

      return [
        `"${s.id || s.username}"`,
        `"${s.username}"`,
        `"${s.displayName}"`,
        `"${s.period}"`,
        s.grade || 12,
        s.totalActiveMinutes,
        `${avg}%`,
        `"${letter}"`,
        '"READY_FOR_SYNC"'
      ].join(',');
    });

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `CIS_Skyward_Gradebook_Export_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12 bg-gray-900/60 border border-gray-800 rounded-xl text-gray-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mr-3"></div>
        <span>Loading Class CIS Telemetry & Roster…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-950/40 border border-red-800/80 rounded-xl text-red-300 flex items-center gap-3">
        <span className="text-xl">⚠️</span>
        <span>{error}</span>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 text-gray-100 font-sans">
      {/* 1. Executive KPI Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Total Students */}
        <div className="bg-gray-900/70 border border-gray-800/90 rounded-xl p-4 flex flex-col justify-between shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase tracking-wider">
            <span>Enrolled Students</span>
            <span className="text-emerald-400">👥 Active</span>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-white">{totalStudents}</span>
            <span className="text-xs text-gray-400">across {uniquePeriods.length || 1} periods</span>
          </div>
        </div>

        {/* Class Readiness Index */}
        <div className="bg-gray-900/70 border border-gray-800/90 rounded-xl p-4 flex flex-col justify-between shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase tracking-wider">
            <span>Class Readiness</span>
            <span className="text-blue-400">📊 Avg Score</span>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-emerald-400">{classAvgScore}%</span>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800/60 text-emerald-300">
              {classAvgScore >= 80 ? 'STRONG' : classAvgScore >= 65 ? 'DEVELOPING' : 'NEEDS WORK'}
            </span>
          </div>
        </div>

        {/* Critical Gap Count */}
        <div className="bg-gray-900/70 border border-gray-800/90 rounded-xl p-4 flex flex-col justify-between shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase tracking-wider">
            <span>Critical Deficits</span>
            <span className="text-red-400">⚡ Action Needed</span>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-red-400">{criticalGapsCount}</span>
            <span className="text-xs text-amber-400">+{needsWorkCount} developing</span>
          </div>
        </div>

        {/* Total Lab Time */}
        <div className="bg-gray-900/70 border border-gray-800/90 rounded-xl p-4 flex flex-col justify-between shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase tracking-wider">
            <span>Hands-on Lab Time</span>
            <span className="text-indigo-400">⏱️ Active Time</span>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-indigo-300">{Math.round(totalLabMinutes / 60)}h</span>
            <span className="text-xs text-gray-400">{totalLabMinutes} total mins</span>
          </div>
        </div>

        {/* Exam Ready Count */}
        <div className="bg-gray-900/70 border border-gray-800/90 rounded-xl p-4 flex flex-col justify-between shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between text-gray-400 text-xs font-semibold uppercase tracking-wider">
            <span>Exam Ready</span>
            <span className="text-amber-400">🎓 Cert Ready</span>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-amber-300">{examReadyStudentsCount}</span>
            <span className="text-xs text-gray-400">score ≥ 80%</span>
          </div>
        </div>
      </div>

      {/* 2. Navigation Tabs & Global Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2 overflow-x-auto">
          <button
            type="button"
            onClick={() => setActiveTab('roster')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'roster'
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40'
                : 'bg-gray-900/60 text-gray-400 hover:text-white hover:bg-gray-800/70 border border-gray-800'
            }`}
          >
            📋 Class Roster ({students.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('gaps')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              activeTab === 'gaps'
                ? 'bg-red-600 text-white shadow-lg shadow-red-900/40'
                : 'bg-gray-900/60 text-gray-400 hover:text-white hover:bg-gray-800/70 border border-gray-800'
            }`}
          >
            <span>🚨 Gap Alerts</span>
            {criticalGapsCount > 0 && (
              <span className="px-2 py-0.5 text-xs font-mono rounded-full bg-red-950 border border-red-500/80 text-red-200">
                {criticalGapsCount}
              </span>
            )}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('matrix')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'matrix'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/40'
                : 'bg-gray-900/60 text-gray-400 hover:text-white hover:bg-gray-800/70 border border-gray-800'
            }`}
          >
            📊 Curriculum Domains ({CIS_DOMAIN_BENCHMARKS.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('skyward')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'skyward'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-900/40'
                : 'bg-gray-900/60 text-gray-400 hover:text-white hover:bg-gray-800/70 border border-gray-800'
            }`}
          >
            🏛️ Skyward SIS Sync
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('mitre')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'mitre'
                ? 'bg-amber-600 text-white shadow-lg shadow-amber-900/40'
                : 'bg-gray-900/60 text-gray-400 hover:text-white hover:bg-gray-800/70 border border-gray-800'
            }`}
          >
            🛡️ MITRE Defense Matrix
          </button>
        </div>

        {/* Global Export CSV Button */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleExportSkywardCSV}
            className="px-3.5 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-emerald-400 border border-gray-700 text-xs font-semibold flex items-center gap-2 transition-colors shadow-sm"
          >
            <span>📥 Export Skyward CSV</span>
          </button>
        </div>
      </div>

      {/* 3. Tab Contents */}

      {/* TAB 1: Class Roster */}
      {activeTab === 'roster' && (
        <div className="flex flex-col gap-4">
          {/* Filters Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3 bg-gray-900/50 border border-gray-800/80 rounded-xl">
            <div className="flex items-center gap-2 flex-1 max-w-sm">
              <span className="text-gray-400 text-sm">🔍</span>
              <input
                type="text"
                placeholder="Search student by name or username…"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-950/80 border border-gray-800 rounded-lg px-3 py-1.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div className="flex items-center gap-3">
              {uniquePeriods.length > 0 && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-400 font-medium">Period:</span>
                  <select
                    value={periodFilter}
                    onChange={(e) => setPeriodFilter(e.target.value)}
                    className="bg-gray-950/80 border border-gray-800 rounded-lg px-2.5 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="">All Periods</option>
                    {uniquePeriods.map(p => (
                      <option key={p} value={p}>{p}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>
          </div>

          {/* Roster Table */}
          <div className="overflow-x-auto rounded-xl border border-gray-800/90 bg-gray-900/60 shadow-xl backdrop-blur-md">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-950/60 text-gray-400 text-xs font-semibold uppercase tracking-wider">
                  <th className="py-3.5 px-4">Student</th>
                  <th className="py-3.5 px-3">Period</th>
                  {allCerts.map((certId) => (
                    <th key={certId} className="py-3.5 px-3 whitespace-nowrap">
                      {CERT_NAMES[certId] || certId}
                    </th>
                  ))}
                  <th className="py-3.5 px-3">Active (7d)</th>
                  <th className="py-3.5 px-3">Last Active</th>
                  <th className="py-3.5 px-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 font-sans">
                {filteredStudents.length === 0 ? (
                  <tr>
                    <td colSpan={allCerts.length + 5} className="py-8 text-center text-gray-500">
                      No students match your filter criteria.
                    </td>
                  </tr>
                ) : (
                  filteredStudents.map((student) => {
                    const studentCerts = Array.isArray(student.certs) ? student.certs : [];
                    const certMap = new Map(studentCerts.map((c) => [c.certId, c]));

                    return (
                      <tr key={student.username} className="hover:bg-gray-800/40 transition-colors">
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-2.5">
                            <div className="w-8 h-8 rounded-full bg-emerald-950/80 border border-emerald-600/40 text-emerald-400 flex items-center justify-center font-mono text-xs font-bold uppercase">
                              {student.displayName.charAt(0)}
                            </div>
                            <div>
                              <div className="font-medium text-gray-100">{student.displayName}</div>
                              <div className="text-xs text-gray-400 font-mono">@{student.username}</div>
                            </div>
                          </div>
                        </td>
                        <td className="py-3 px-3">
                          <span className="px-2 py-0.5 text-xs rounded bg-gray-800 text-gray-300 font-mono">
                            {student.period}
                          </span>
                        </td>
                        {allCerts.map((certId) => {
                          const c = certMap.get(certId);
                          return (
                            <td key={certId} className="py-3 px-3">
                              {c ? (
                                <ReadinessGauge value={c.readiness} tier={c.paTier} />
                              ) : (
                                <span className="text-xs text-gray-600 font-mono">—</span>
                              )}
                            </td>
                          );
                        })}
                        <td className="py-3 px-3">
                          <span className="font-mono text-xs text-indigo-300">
                            {student.totalActiveMinutes}m
                          </span>
                        </td>
                        <td className="py-3 px-3 text-xs text-gray-400">
                          {student.lastActive ? new Date(student.lastActive).toLocaleDateString() : '—'}
                        </td>
                        <td className="py-3 px-3 text-right">
                          <button
                            type="button"
                            onClick={() => setSelectedStudent(student)}
                            className="px-2.5 py-1 text-xs rounded bg-gray-800 hover:bg-gray-700 text-emerald-400 border border-gray-700 transition-colors"
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: Critical Gap Alerts */}
      {activeTab === 'gaps' && (
        <div className="flex flex-col gap-4">
          <div className="p-4 bg-gray-900/60 border border-gray-800 rounded-xl flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-gray-100">Live Competency Deficit Monitor</h3>
              <p className="text-xs text-gray-400">Students requiring targeted instructional intervention or lab remediation.</p>
            </div>
            <span className="px-3 py-1 text-xs font-mono rounded-lg bg-red-950/80 border border-red-800 text-red-300 font-semibold">
              {safeGaps.length} Action Items
            </span>
          </div>

          <div className="overflow-x-auto rounded-xl border border-gray-800 bg-gray-900/60">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-950/60 text-gray-400 text-xs font-semibold uppercase tracking-wider">
                  <th className="py-3 px-4">Student</th>
                  <th className="py-3 px-3">Certification</th>
                  <th className="py-3 px-3">Domain / Topic</th>
                  <th className="py-3 px-3">Readiness</th>
                  <th className="py-3 px-3">Priority</th>
                  <th className="py-3 px-3">Deficit (Est.)</th>
                  <th className="py-3 px-4">Remediation Action Plan</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60">
                {safeGaps.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-8 text-center text-emerald-400">
                      🎉 No critical gaps detected! All students are on track.
                    </td>
                  </tr>
                ) : (
                  safeGaps.map((gap, i) => (
                    <tr key={i} className="hover:bg-gray-800/40">
                      <td className="py-3 px-4 font-medium text-gray-100">
                        {gap.displayName} <span className="text-xs text-gray-400 font-mono">(@{gap.studentUsername})</span>
                      </td>
                      <td className="py-3 px-3 font-mono text-xs text-indigo-300">{gap.certId}</td>
                      <td className="py-3 px-3 text-gray-300">{gap.domainName}</td>
                      <td className="py-3 px-3">
                        <ReadinessGauge value={gap.readiness} tier={gap.priority === 'CRITICAL' ? 'CRITICAL' : 'NEEDS_WORK'} />
                      </td>
                      <td className="py-3 px-3">
                        <span
                          className={`px-2 py-0.5 text-xs font-semibold rounded ${
                            gap.priority === 'CRITICAL'
                              ? 'bg-red-950/80 border border-red-500/80 text-red-300'
                              : 'bg-amber-950/80 border border-amber-500/80 text-amber-300'
                          }`}
                        >
                          {gap.priority}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-mono text-xs text-amber-300">~{gap.deficitMinutes} mins</td>
                      <td className="py-3 px-4 text-xs text-gray-300">
                        {gap.coachingAction}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: Curriculum Domains Heatmap */}
      {activeTab === 'matrix' && (
        <div className="flex flex-col gap-4">
          <div className="p-4 bg-gray-900/60 border border-gray-800 rounded-xl">
            <h3 className="text-base font-bold text-gray-100">State CIS Competency Standards Matrix</h3>
            <p className="text-xs text-gray-400">Official PA Program of Study curriculum benchmark breakdown across all 28 domains.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {CIS_DOMAIN_BENCHMARKS.map((dom) => (
              <div key={dom.id} className="bg-gray-900/60 border border-gray-800 rounded-xl p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-mono text-indigo-400">{dom.id}</span>
                    <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px] font-bold uppercase">
                      {dom.certTrackId}
                    </span>
                  </div>
                  <h4 className="mt-1 font-semibold text-gray-100 text-sm">{dom.name}</h4>
                </div>
                <div className="mt-4 pt-3 border-t border-gray-800 flex items-center justify-between text-xs text-gray-400">
                  <span>Target Lab Hours:</span>
                  <span className="font-mono font-bold text-emerald-400">{Math.round(dom.expectedMinutes / 60)}h ({dom.expectedMinutes}m)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: Skyward SIS Sync */}
      {activeTab === 'skyward' && (
        <div className="flex flex-col gap-4">
          <div className="p-4 bg-gray-900/60 border border-gray-800 rounded-xl flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-gray-100">Skyward SIS Gradebook Integration</h3>
              <p className="text-xs text-gray-400">Class competency scores formatted for official district gradebook import.</p>
            </div>
            <button
              type="button"
              onClick={handleExportSkywardCSV}
              className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs flex items-center gap-2 shadow-lg shadow-purple-900/40"
            >
              <span>📥 Download Skyward CSV</span>
            </button>
          </div>

          <div className="overflow-x-auto rounded-xl border border-gray-800 bg-gray-900/60">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-950/60 text-gray-400 text-xs font-semibold uppercase tracking-wider">
                  <th className="py-3 px-4">Student ID / Skyward ID</th>
                  <th className="py-3 px-4">Student Name</th>
                  <th className="py-3 px-3">Period</th>
                  <th className="py-3 px-3">Grade</th>
                  <th className="py-3 px-3">Active Minutes</th>
                  <th className="py-3 px-3">Calculated %</th>
                  <th className="py-3 px-3">Letter Grade</th>
                  <th className="py-3 px-4">Sync Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60 font-mono text-xs">
                {filteredStudents.map((student) => {
                  const avg = student.certs.length > 0 ? Math.round(student.certs.reduce((a, b) => a + b.readiness, 0) / student.certs.length) : 0;
                  let letter = 'F';
                  if (avg >= 90) letter = 'A';
                  else if (avg >= 80) letter = 'B';
                  else if (avg >= 70) letter = 'C';
                  else if (avg >= 60) letter = 'D';

                  return (
                    <tr key={student.username} className="hover:bg-gray-800/40">
                      <td className="py-3 px-4 text-indigo-300">{student.id || student.username}</td>
                      <td className="py-3 px-4 font-sans text-gray-100 font-medium">{student.displayName}</td>
                      <td className="py-3 px-3 text-gray-300">{student.period}</td>
                      <td className="py-3 px-3 text-gray-300">{student.grade}</td>
                      <td className="py-3 px-3 text-gray-300">{student.totalActiveMinutes}m</td>
                      <td className="py-3 px-3 text-emerald-400 font-bold">{avg}%</td>
                      <td className="py-3 px-3">
                        <span className={`px-2 py-0.5 rounded font-bold ${
                          letter === 'A' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                          letter === 'B' ? 'bg-blue-950 text-blue-300 border border-blue-800' :
                          letter === 'C' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                          'bg-red-950 text-red-300 border border-red-800'
                        }`}>
                          {letter}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-emerald-400">● READY_FOR_SYNC</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 5: MITRE ATT&CK Enterprise Matrix */}
      {activeTab === 'mitre' && (
        <div className="flex flex-col gap-4">
          <div className="p-4 bg-gray-900/60 border border-gray-800 rounded-xl">
            <h3 className="text-base font-bold text-gray-100">MITRE ATT&CK Enterprise Defense Matrix</h3>
            <p className="text-xs text-gray-400">Class cybersecurity and defensive operations proficiency mapped across industry standard threat tactics.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {MITRE_TACTICS.map((tac) => (
              <div key={tac.id} className="p-3.5 bg-gray-900/60 border border-gray-800 rounded-xl flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-mono text-amber-400 font-bold">{tac.id}</span>
                    <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px] font-mono">
                      {tac.standard}
                    </span>
                  </div>
                  <h4 className="mt-1.5 font-semibold text-gray-100 text-sm">{tac.name}</h4>
                  <p className="mt-1 text-xs text-gray-400 font-mono">Mapped: {tac.domain}</p>
                </div>
                <div className="mt-3 pt-2 border-t border-gray-800 flex items-center justify-between text-xs">
                  <span className="text-gray-400">Class Proficiency:</span>
                  <span className="font-mono font-bold text-emerald-400">Covered</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. Student Detail Modal */}
      {selectedStudent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl max-w-2xl w-full p-6 shadow-2xl flex flex-col gap-5">
            <div className="flex items-center justify-between border-b border-gray-800 pb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-emerald-950 border border-emerald-500/50 text-emerald-400 flex items-center justify-center font-bold text-lg">
                  {selectedStudent.displayName.charAt(0)}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">{selectedStudent.displayName}</h3>
                  <div className="text-xs text-gray-400 font-mono">
                    @{selectedStudent.username} • {selectedStudent.period} • Grade {selectedStudent.grade}
                  </div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedStudent(null)}
                className="text-gray-400 hover:text-white text-xl p-1"
              >
                ✕
              </button>
            </div>

            {/* Certifications Progress */}
            <div className="flex flex-col gap-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-400">Certification Readiness</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {allCerts.map((certId) => {
                  const c = selectedStudent.certs.find(x => x.certId === certId);
                  return (
                    <div key={certId} className="p-3 bg-gray-950/60 border border-gray-800/80 rounded-xl flex items-center justify-between">
                      <div>
                        <div className="text-xs font-semibold text-gray-200">{CERT_NAMES[certId] || certId}</div>
                        <div className="text-[10px] text-gray-400 font-mono">{c?.paTier || 'NOT_STARTED'}</div>
                      </div>
                      <div className="text-right font-mono font-bold text-emerald-400">
                        {c?.readiness ? `${c.readiness}%` : '0%'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Telemetry Stats */}
            <div className="p-3 bg-gray-950/60 border border-gray-800 rounded-xl flex items-center justify-between text-xs">
              <div>
                <span className="text-gray-400">Active Lab Time: </span>
                <span className="font-mono font-bold text-indigo-300">{selectedStudent.totalActiveMinutes} minutes</span>
              </div>
              <div>
                <span className="text-gray-400">Last Activity: </span>
                <span className="font-mono text-gray-300">{selectedStudent.lastActive ? new Date(selectedStudent.lastActive).toLocaleString() : 'Never'}</span>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-gray-800">
              <a
                href={`/admin/student/${selectedStudent.username}`}
                className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold"
              >
                Full Student Profile →
              </a>
              <button
                type="button"
                onClick={() => setSelectedStudent(null)}
                className="px-4 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
