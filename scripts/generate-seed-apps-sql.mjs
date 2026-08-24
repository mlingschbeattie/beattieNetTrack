import fs from 'node:fs';

const sqlPath = 'c:/Users/mlingsch/cluster/packages/db/scripts/seed-apps.sql';

const sqlContent = `-- Seed / refresh the hub.app_registry table with all canonical apps
INSERT INTO hub.app_registry (id, title, description, url, icon, color, nav_position, status, event_types)
VALUES
  ('lms', 'Beattie LMS', 'Learning management system — course content, tracks, and assignments', 'https://lms.beattietech.local', 'book-open', '#6366f1', 1, 'active', '["lms.lesson_viewed", "lms.assignment_submitted", "lms.lab_started", "lms.lab_completed", "lms.lab_beacon"]'::jsonb),
  ('cis', 'CIS Portal', 'CompTIA (A+, Net+, Sec+) & NOCTI certification tracking', 'https://cis.beattietech.local', 'award', '#3b82f6', 2, 'active', '["cis.objective_completed", "cis.exam_passed", "cis.exam_answer"]'::jsonb),
  ('chat', 'Beattie Chat', 'Private AI chat assistant powered by Ollama cluster', 'https://chat.beattietech.local', 'message-square', '#8b5cf6', 3, 'active', '["chat.message_sent"]'::jsonb),
  ('traceback', 'Traceback', 'Sigma Threat Response hands-on cyber ops simulator', 'https://traceback.beattietech.local', 'crosshair', '#f97316', 4, 'active', '["traceback.run_started", "traceback.run_completed", "traceback.run_abandoned"]'::jsonb),
  ('labs', 'Cyber Labs & ATT&CK', 'Hands-on firewall, packet inspection, and malware analysis labs', 'https://labs.beattietech.local', 'terminal', '#ef4444', 5, 'active', '["labs.lab_completed", "labs.quiz_submitted"]'::jsonb),
  ('quests', 'Quest Crusher', 'Jeopardy-style CTE review game', 'https://quests.beattietech.local', 'zap', '#f59e0b', 6, 'active', '["quests.answer_correct", "quests.answer_incorrect", "quests.game_complete"]'::jsonb),
  ('game', 'Run Brady Run', 'Rhythm platformer game', 'https://game.beattietech.local', 'gamepad-2', '#10b981', 7, 'active', '["game.level_complete", "game.score_submitted", "game.run_completed"]'::jsonb),
  ('journal', 'Work Journal', 'CTE work tracking and competency logging', 'https://journal.beattietech.local', 'notebook-pen', '#06b6d4', 8, 'active', '["journal.entry_created", "journal.entry_submitted", "journal.entry_reviewed"]'::jsonb),
  ('shop', 'Sub Shop', 'Student credit marketplace', 'https://shop.beattietech.local', 'shopping-bag', '#ec4899', 9, 'active', '["shop.purchase", "shop.item_listed"]'::jsonb),
  ('ai', 'AI Studio', 'Portal to AI tools and model playground', 'https://ai.beattietech.local', 'sparkles', '#a855f7', 10, 'active', '[]'::jsonb),
  ('pcap-hunt', 'PCAP Hunt', 'Threat hunting simulation and packet submission workflow', 'https://pcap.beattietech.local', 'shield', '#22c55e', 11, 'active', '["pcap.session_started", "pcap.finding_submitted", "pcap.session_submitted"]'::jsonb),
  ('cipher', 'Cipher Challenge', 'Student encryption and decryption activity', 'https://cipher.beattietech.local', 'lock', '#14b8a6', 12, 'active', '["cipher.challenge_complete", "cipher.hint_used"]'::jsonb),
  ('techsupport', 'Tech Support Simulator', 'Enterprise helpdesk, multi-OS troubleshooting, and AI user roleplay', 'https://techsupport.beattietech.local', 'headphones', '#0ea5e9', 13, 'active', '["techsupport.ticket_solved", "techsupport.security_violation", "techsupport.session_complete"]'::jsonb),
  ('cyberlab', 'CyberLab: Ethical Hacker', 'Penetration testing sandbox, MITRE ATT&CK matrix, and AI mentor', 'https://cyberlab.beattietech.local', 'shield-alert', '#ef4444', 14, 'active', '["cyberlab.scenario_completed", "cyberlab.quiz_passed", "cyberlab.mitre_unlocked"]'::jsonb),
  ('cyterm', 'CyberTerminal CIS', 'Interactive Linux security terminal simulator and attack scenarios', 'https://cyterm.beattietech.local', 'terminal', '#10b981', 15, 'active', '["cyterm.command_unlocked", "cyterm.flag_captured", "cyterm.scenario_completed"]'::jsonb),
  ('nexus', 'PC Build Simulator 3D', 'Interactive 3D hardware assembly, cable management, and benchmarking', 'https://nexus.beattietech.local', 'cpu', '#8b5cf6', 16, 'active', '["nexus.build_complete", "nexus.benchmark_passed", "nexus.wire_connected"]'::jsonb)
ON CONFLICT (id) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  url = EXCLUDED.url,
  icon = EXCLUDED.icon,
  color = EXCLUDED.color,
  nav_position = EXCLUDED.nav_position,
  status = EXCLUDED.status,
  event_types = EXCLUDED.event_types,
  updated_at = now();
`;

fs.writeFileSync(sqlPath, sqlContent);
console.log('Created seed-apps.sql');
