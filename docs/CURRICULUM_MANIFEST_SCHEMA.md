# Curriculum Manifest Schema — v1

**Status:** Approved architecture  
**Produced by:** P1-A session  
**Date:** 2026-03-04  
**Scope:** Schema design only — no ingest script in this document

---

## 1. Overview

A **curriculum manifest** is a single JSON file that describes an entire track: its metadata, modules, and every activity (lesson, lab, quiz, activity) within those modules. A curriculum author fills this out without knowing Astro, TypeScript, or MDX. The ingest script (`scripts/ingest-curriculum.mjs`, built in P1-B) reads the manifest and generates all required MDX files into `src/content/`.

### Core Principles

| Principle | How the schema satisfies it |
|---|---|
| **No Astro/TS knowledge needed** | Plain JSON with human-readable fields; no MDX syntax anywhere in the manifest |
| **track/moduleId inferred** | Hierarchical nesting — activities live inside modules, modules live inside the track. The ingest script derives `track` and `moduleId` from structure. |
| **Versionable** | Top-level `manifestVersion` field. Ingest script rejects unknown versions. |
| **Validation-ready** | Every required field from `config.ts` is either present in the manifest or has a safe default the ingest script can apply. |
| **Labs have real steps** | `steps` is required on labs with `minItems: 1`. No stub labs. |
| **External body content** | Lessons reference `.md` files via `bodyFile` for long-form content. |

---

## 2. Full JSON Schema

The schema below uses [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core) notation for precision. Authors do not need to understand JSON Schema — section 3 provides a complete example.

```jsonc
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://beattie-net-track.local/curriculum-manifest-v1.schema.json",
  "title": "BeattieNetTrack Curriculum Manifest",
  "description": "Defines a complete track with modules and activities for ingest into the LMS.",
  "type": "object",
  "required": ["manifestVersion", "track", "modules"],
  "additionalProperties": false,
  "properties": {

    "manifestVersion": {
      "type": "integer",
      "const": 1,
      "description": "Schema version. Must be 1 for this version. The ingest script will reject manifests with unknown versions."
    },

    "track": {
      "type": "object",
      "description": "Top-level track metadata. Generates one file: src/content/tracks/<slug>.mdx",
      "required": ["slug", "title"],
      "additionalProperties": false,
      "properties": {
        "slug": {
          "type": "string",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
          "description": "URL-safe identifier. Used as the track filename and in all route paths. Example: 'linux-fundamentals'"
        },
        "title": {
          "type": "string",
          "description": "Human-readable track title. Example: 'Linux Fundamentals'"
        },
        "description": {
          "type": "string",
          "description": "One-sentence track description.",
          "default": "Hands-on lab workspace."
        },
        "icon": {
          "type": "string",
          "description": "Emoji or icon string displayed in the track card. Example: '🐧'",
          "default": "📘"
        },
        "estimatedHours": {
          "type": "integer",
          "minimum": 1,
          "description": "Total estimated hours for the full track."
        },
        "level": {
          "type": "string",
          "enum": ["Beginner", "Intermediate", "Advanced"],
          "description": "Overall difficulty level for the track.",
          "default": "Beginner"
        },
        "order": {
          "type": "integer",
          "description": "Display order on the /tracks hub page. Lower = first.",
          "default": 0
        }
      }
    },

    "modules": {
      "type": "array",
      "minItems": 1,
      "description": "Ordered list of modules in this track. Each module becomes src/content/modules/<track-slug>/<moduleId>.mdx",
      "items": {
        "type": "object",
        "required": ["id", "title"],
        "additionalProperties": false,
        "properties": {

          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+\\.[a-z0-9]+\\.[a-z0-9-]+$",
            "description": "Canonical module ID using dot notation: <prefix>.<category>.<topic>. Example: 'lnx.cli.basics'. This becomes the moduleId in all child activities."
          },
          "title": {
            "type": "string",
            "description": "Human-readable module title."
          },
          "description": {
            "type": "string",
            "description": "Brief module description.",
            "default": ""
          },
          "order": {
            "type": "integer",
            "description": "Display order within the track. Defaults to array position (1-indexed) if omitted."
          },

          "lessons": {
            "type": "array",
            "description": "Lessons in this module. Each becomes src/content/lessons/<slug>.mdx",
            "default": [],
            "items": { "$ref": "#/$defs/lesson" }
          },

          "labs": {
            "type": "array",
            "description": "Labs in this module. Each becomes src/content/labs/<slug>.mdx",
            "default": [],
            "items": { "$ref": "#/$defs/lab" }
          },

          "quizzes": {
            "type": "array",
            "description": "Quizzes in this module. Each becomes src/content/quizzes/<track-slug>/<slug>.mdx",
            "default": [],
            "items": { "$ref": "#/$defs/quiz" }
          },

          "activities": {
            "type": "array",
            "description": "Generic activities (iframe/terminal/code) in this module. Each becomes src/content/activities/<slug>.mdx",
            "default": [],
            "items": { "$ref": "#/$defs/activity" }
          }
        }
      }
    }
  },

  "$defs": {

    "lesson": {
      "type": "object",
      "required": ["slug", "title"],
      "additionalProperties": false,
      "properties": {
        "slug": {
          "type": "string",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
          "description": "URL-safe lesson identifier. Must be unique across all lessons in the LMS."
        },
        "title": {
          "type": "string",
          "description": "Lesson title."
        },
        "description": {
          "type": "string",
          "description": "Brief lesson summary.",
          "default": "Lesson content."
        },
        "order": {
          "type": "integer",
          "description": "Display order within the module. Defaults to array position if omitted."
        },
        "difficulty": {
          "type": "string",
          "enum": ["Beginner", "Intermediate", "Advanced"],
          "default": "Intermediate"
        },
        "estMinutes": {
          "type": "integer",
          "minimum": 1,
          "description": "Estimated reading/completion time in minutes.",
          "default": 15
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "⚠️ REQUIRES config.ts UPDATE — tags is present in live frontmatter but not yet declared in the lessons schema in config.ts. Include here for future use; ingest will emit the field.",
          "default": []
        },
        "bodyFile": {
          "type": "string",
          "description": "Relative path (from manifest location) to a .md file containing the lesson body. If omitted, a placeholder body is generated. Example: 'content/intro-to-linux.md'"
        },
        "bodyInline": {
          "type": "string",
          "description": "Inline Markdown body content. Used for short lessons. If both bodyFile and bodyInline are set, bodyFile takes precedence."
        }
      }
    },

    "lab": {
      "type": "object",
      "required": ["slug", "title", "description", "steps"],
      "additionalProperties": false,
      "properties": {
        "slug": {
          "type": "string",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
          "description": "URL-safe lab identifier. Must be unique across all labs."
        },
        "title": {
          "type": "string",
          "description": "Lab title."
        },
        "description": {
          "type": "string",
          "description": "Brief lab description (required — config.ts enforces non-optional)."
        },
        "order": {
          "type": "integer",
          "description": "Display order within the module.",
          "default": 0
        },
        "difficulty": {
          "type": "string",
          "enum": ["Beginner", "Intermediate", "Advanced"],
          "default": "Beginner"
        },
        "estimatedMinutes": {
          "type": "integer",
          "minimum": 1,
          "description": "Estimated completion time.",
          "default": 20
        },
        "xp": {
          "type": "integer",
          "minimum": 0,
          "description": "XP awarded on completion.",
          "default": 25
        },
        "activity": {
          "type": "string",
          "enum": ["iframe", "terminal", "code"],
          "description": "Activity type that determines the workspace UI.",
          "default": "iframe"
        },
        "labPath": {
          "type": "string",
          "description": "Path to the lab workspace (relative to public/). Example: '/labs/network-terminal-basics/index.html'"
        },
        "labUrl": {
          "type": "string",
          "description": "External URL for the lab workspace. Use labPath for local labs, labUrl for external."
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "hints": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Global lab hints shown to the learner.",
          "default": []
        },
        "checklist": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Completion checklist items.",
          "default": []
        },
        "checkLabel": {
          "type": "string",
          "description": "Label for the check/validate button.",
          "default": "Check"
        },
        "submitLabel": {
          "type": "string",
          "description": "Label for the submit button.",
          "default": "Submit"
        },

        "steps": {
          "type": "array",
          "minItems": 1,
          "description": "Ordered lab steps. EVERY lab must have at least one step.",
          "items": {
            "type": "object",
            "required": ["id", "title", "prompt", "validator"],
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "description": "Unique step identifier within this lab. Example: 'step-1' or 'check-permissions'"
              },
              "title": {
                "type": "string",
                "description": "Step title shown to the learner."
              },
              "prompt": {
                "type": "string",
                "description": "The instruction or question for this step."
              },
              "inputLabel": {
                "type": "string",
                "description": "Label for the input field."
              },
              "placeholder": {
                "type": "string",
                "description": "Placeholder text in the input field."
              },
              "hint": {
                "type": "string",
                "description": "Hint shown on request."
              },
              "successMessage": {
                "type": "string",
                "description": "Message shown when the step is completed correctly."
              },
              "validator": {
                "type": "object",
                "required": ["type"],
                "description": "Validation rule for the learner's input.",
                "oneOf": [
                  {
                    "properties": {
                      "type": { "const": "exact" },
                      "value": { "type": "string", "description": "The exact expected answer." }
                    },
                    "required": ["type", "value"],
                    "additionalProperties": false
                  },
                  {
                    "properties": {
                      "type": { "const": "oneOf" },
                      "values": {
                        "type": "array",
                        "items": { "type": "string" },
                        "minItems": 1,
                        "description": "List of accepted answers (any match = correct)."
                      }
                    },
                    "required": ["type", "values"],
                    "additionalProperties": false
                  },
                  {
                    "properties": {
                      "type": { "const": "regex" },
                      "pattern": { "type": "string", "description": "Regex pattern to match against the answer." },
                      "flags": { "type": "string", "description": "Regex flags (e.g., 'i' for case-insensitive).", "default": "" }
                    },
                    "required": ["type", "pattern"],
                    "additionalProperties": false
                  }
                ]
              }
            }
          }
        }
      }
    },

    "quiz": {
      "type": "object",
      "required": ["slug", "title", "questions"],
      "additionalProperties": false,
      "properties": {
        "slug": {
          "type": "string",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
          "description": "URL-safe quiz identifier."
        },
        "title": {
          "type": "string"
        },
        "description": {
          "type": "string",
          "default": "Quiz workspace"
        },
        "order": {
          "type": "integer",
          "default": 0
        },
        "difficulty": {
          "type": "string",
          "enum": ["Beginner", "Intermediate", "Advanced"],
          "default": "Intermediate"
        },
        "estMinutes": {
          "type": "integer",
          "minimum": 1,
          "default": 15
        },
        "passThreshold": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100,
          "description": "Minimum score (%) to pass.",
          "default": 70
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "hints": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "checklist": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },

        "questions": {
          "type": "array",
          "minItems": 1,
          "description": "Quiz questions. Every quiz must have at least one question.",
          "items": {
            "type": "object",
            "required": ["id", "type", "prompt"],
            "properties": {
              "id": {
                "type": "string",
                "description": "Unique question ID within this quiz."
              },
              "type": {
                "type": "string",
                "enum": ["single", "multi", "short"],
                "description": "single = one correct answer, multi = multiple correct, short = free text."
              },
              "prompt": {
                "type": "string",
                "description": "The question text."
              },
              "explanation": {
                "type": "string",
                "description": "Explanation shown after answering (optional)."
              },
              "options": {
                "type": "array",
                "items": { "type": "string" },
                "minItems": 2,
                "description": "Answer options. Required for 'single' and 'multi' types."
              },
              "correctIndex": {
                "type": "integer",
                "minimum": 0,
                "description": "Zero-based index of the correct option. Required for 'single' type."
              },
              "correctIndices": {
                "type": "array",
                "items": { "type": "integer", "minimum": 0 },
                "minItems": 1,
                "description": "Zero-based indices of all correct options. Required for 'multi' type."
              },
              "acceptedAnswers": {
                "type": "array",
                "items": { "type": "string" },
                "minItems": 1,
                "description": "Accepted text answers. Required for 'short' type."
              }
            },
            "allOf": [
              {
                "if": { "properties": { "type": { "const": "single" } } },
                "then": { "required": ["options", "correctIndex"] }
              },
              {
                "if": { "properties": { "type": { "const": "multi" } } },
                "then": { "required": ["options", "correctIndices"] }
              },
              {
                "if": { "properties": { "type": { "const": "short" } } },
                "then": { "required": ["acceptedAnswers"] }
              }
            ]
          }
        }
      }
    },

    "activity": {
      "type": "object",
      "required": ["slug", "title"],
      "additionalProperties": false,
      "properties": {
        "slug": {
          "type": "string",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
        },
        "title": {
          "type": "string"
        },
        "description": {
          "type": "string",
          "default": "Workspace activity"
        },
        "order": {
          "type": "integer",
          "default": 0
        },
        "difficulty": {
          "type": "string",
          "enum": ["Beginner", "Intermediate", "Advanced"],
          "default": "Intermediate"
        },
        "estMinutes": {
          "type": "integer",
          "minimum": 1,
          "default": 15
        },
        "labPath": {
          "type": "string",
          "description": "Path to workspace (relative to public/)."
        },
        "labUrl": {
          "type": "string",
          "description": "External URL for the workspace."
        }
      }
    }
  }
}
```

---

## 3. Complete Sample Manifest

File: `manifests/linux-fundamentals.json`

This sample defines a **Linux Fundamentals** track with 2 modules, 3 lessons, 2 labs, and 2 quizzes.

```json
{
  "manifestVersion": 1,

  "track": {
    "slug": "linux-fundamentals",
    "title": "Linux Fundamentals",
    "description": "Master the Linux command line, file system, and basic administration.",
    "icon": "🐧",
    "estimatedHours": 6,
    "level": "Beginner",
    "order": 10
  },

  "modules": [
    {
      "id": "lnx.cli.basics",
      "title": "Command Line Basics",
      "description": "Navigate the terminal, manage files, and understand the shell.",
      "order": 1,

      "lessons": [
        {
          "slug": "intro-to-linux",
          "title": "Introduction to Linux",
          "description": "What Linux is, why it matters, and how it differs from other OSes.",
          "order": 1,
          "difficulty": "Beginner",
          "estMinutes": 10,
          "tags": ["linux", "overview", "open-source"],
          "bodyFile": "content/intro-to-linux.md"
        },
        {
          "slug": "navigating-the-filesystem",
          "title": "Navigating the File System",
          "description": "Learn pwd, ls, cd, and the Linux directory hierarchy.",
          "order": 2,
          "difficulty": "Beginner",
          "estMinutes": 15,
          "tags": ["linux", "filesystem", "cli"],
          "bodyFile": "content/navigating-the-filesystem.md"
        }
      ],

      "labs": [
        {
          "slug": "linux-cli-basics-lab",
          "title": "CLI Basics Lab",
          "description": "Practice essential terminal commands: pwd, ls, cd, mkdir, and rm.",
          "order": 3,
          "difficulty": "Beginner",
          "estimatedMinutes": 15,
          "xp": 30,
          "activity": "terminal",
          "tags": ["linux", "cli", "terminal"],
          "hints": [
            "Use 'man <command>' to read the manual for any command.",
            "Tab completion saves time — press Tab after typing partial names."
          ],
          "checklist": [
            "Completed all 4 steps",
            "Understood the difference between relative and absolute paths"
          ],
          "steps": [
            {
              "id": "pwd-check",
              "title": "Print Working Directory",
              "prompt": "What command prints your current directory?",
              "hint": "Three letters, stands for 'print working directory'.",
              "successMessage": "Correct! pwd shows where you are in the filesystem.",
              "validator": {
                "type": "exact",
                "value": "pwd"
              }
            },
            {
              "id": "ls-check",
              "title": "List Directory Contents",
              "prompt": "What command lists files in the current directory?",
              "hint": "Two letters. Try the basic form or the long listing.",
              "validator": {
                "type": "oneOf",
                "values": ["ls", "ls -l", "ls -la", "ls -a"]
              }
            },
            {
              "id": "mkdir-check",
              "title": "Create a Directory",
              "prompt": "Write the command to create a directory called 'projects'.",
              "hint": "The command name is short for 'make directory'.",
              "validator": {
                "type": "exact",
                "value": "mkdir projects"
              }
            },
            {
              "id": "cd-check",
              "title": "Change Directory",
              "prompt": "Write the command to move into the 'projects' directory you just created.",
              "validator": {
                "type": "exact",
                "value": "cd projects"
              }
            }
          ]
        }
      ],

      "quizzes": [
        {
          "slug": "cli-basics-checkpoint",
          "title": "CLI Basics Checkpoint",
          "description": "Test your knowledge of basic Linux commands.",
          "order": 4,
          "difficulty": "Beginner",
          "estMinutes": 5,
          "passThreshold": 70,
          "tags": ["linux", "cli", "checkpoint"],
          "questions": [
            {
              "id": "q1",
              "type": "single",
              "prompt": "Which command prints the current working directory?",
              "options": ["ls", "pwd", "cd", "echo"],
              "correctIndex": 1,
              "explanation": "pwd (print working directory) displays the full path of the current directory."
            },
            {
              "id": "q2",
              "type": "multi",
              "prompt": "Which of the following are valid ls flags? (Select all that apply)",
              "options": ["-l", "-a", "-z", "-h"],
              "correctIndices": [0, 1, 3],
              "explanation": "-l (long listing), -a (show hidden), and -h (human-readable sizes) are all valid. -z is not a standard ls flag."
            },
            {
              "id": "q3",
              "type": "short",
              "prompt": "What command removes an empty directory?",
              "acceptedAnswers": ["rmdir", "rm -d"],
              "explanation": "rmdir removes empty directories. rm -d also works on some systems."
            }
          ]
        }
      ]
    },

    {
      "id": "lnx.admin.users",
      "title": "Users & Permissions",
      "description": "Manage user accounts, groups, file ownership, and permission bits.",
      "order": 2,

      "lessons": [
        {
          "slug": "linux-users-and-groups",
          "title": "Users and Groups",
          "description": "Understand the Linux user model: UIDs, GIDs, /etc/passwd, and /etc/group.",
          "order": 1,
          "difficulty": "Intermediate",
          "estMinutes": 20,
          "tags": ["linux", "users", "groups", "permissions"],
          "bodyFile": "content/linux-users-and-groups.md"
        }
      ],

      "labs": [
        {
          "slug": "linux-permissions-lab",
          "title": "File Permissions Lab",
          "description": "Practice reading and setting Linux file permissions with chmod and chown.",
          "order": 2,
          "difficulty": "Intermediate",
          "estimatedMinutes": 20,
          "xp": 40,
          "activity": "terminal",
          "tags": ["linux", "permissions", "chmod", "chown"],
          "hints": [
            "Permission bits: r=4, w=2, x=1. Add them to set combined permissions.",
            "Use 'ls -l' to see current permissions on files."
          ],
          "steps": [
            {
              "id": "read-permissions",
              "title": "Read File Permissions",
              "prompt": "What command shows the permissions of a file named 'report.txt' in long format?",
              "hint": "Use ls with a flag that shows the long listing.",
              "validator": {
                "type": "oneOf",
                "values": ["ls -l report.txt", "ls -la report.txt"]
              }
            },
            {
              "id": "chmod-numeric",
              "title": "Set Permissions (Numeric)",
              "prompt": "Set report.txt to owner read/write, group read-only, others no access. Use numeric mode.",
              "hint": "Owner rw = 6, group r = 4, others none = 0.",
              "validator": {
                "type": "exact",
                "value": "chmod 640 report.txt"
              }
            },
            {
              "id": "chmod-symbolic",
              "title": "Add Execute Permission",
              "prompt": "Add execute permission for the owner on a file called 'deploy.sh' using symbolic mode.",
              "validator": {
                "type": "regex",
                "pattern": "^chmod\\s+u\\+x\\s+deploy\\.sh$",
                "flags": "i"
              }
            }
          ]
        }
      ],

      "quizzes": [
        {
          "slug": "permissions-checkpoint",
          "title": "Permissions Checkpoint",
          "description": "Test your understanding of Linux file permissions.",
          "order": 3,
          "difficulty": "Intermediate",
          "estMinutes": 5,
          "passThreshold": 70,
          "tags": ["linux", "permissions", "checkpoint"],
          "questions": [
            {
              "id": "pq1",
              "type": "single",
              "prompt": "What does the permission string 'rwxr-x---' mean in numeric notation?",
              "options": ["750", "640", "755", "700"],
              "correctIndex": 0,
              "explanation": "rwx=7, r-x=5, ---=0 → 750"
            },
            {
              "id": "pq2",
              "type": "short",
              "prompt": "What command changes file ownership to user 'admin' and group 'staff' for file 'data.csv'?",
              "acceptedAnswers": [
                "chown admin:staff data.csv",
                "chown admin.staff data.csv"
              ],
              "explanation": "chown user:group file changes both owner and group."
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 4. Field Reference (Quick Table)

### Track (top-level)

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `slug` | string | **Yes** | — | Kebab-case, unique across the LMS |
| `title` | string | **Yes** | — | |
| `description` | string | No | `"Hands-on lab workspace."` | |
| `icon` | string | No | `"📘"` | Emoji recommended |
| `estimatedHours` | integer | No | — | |
| `level` | enum | No | `"Beginner"` | Beginner / Intermediate / Advanced |
| `order` | integer | No | `0` | Position on /tracks hub |

### Module

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | string | **Yes** | — | Dot-notation: `prefix.category.topic` |
| `title` | string | **Yes** | — | |
| `description` | string | No | `""` | |
| `order` | integer | No | Array index (1-based) | |
| `lessons` | array | No | `[]` | |
| `labs` | array | No | `[]` | |
| `quizzes` | array | No | `[]` | |
| `activities` | array | No | `[]` | |

### Lesson

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `slug` | string | **Yes** | — | Unique across all lessons |
| `title` | string | **Yes** | — | |
| `description` | string | No | `"Lesson content."` | |
| `order` | integer | No | Array index | |
| `difficulty` | enum | No | `"Intermediate"` | |
| `estMinutes` | integer | No | `15` | |
| `tags` | string[] | No | `[]` | ⚠️ Requires config.ts update (see §6) |
| `bodyFile` | string | No | — | Path to .md file relative to manifest |
| `bodyInline` | string | No | — | Inline markdown body content |

### Lab

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `slug` | string | **Yes** | — | |
| `title` | string | **Yes** | — | |
| `description` | string | **Yes** | — | Required by config.ts |
| `steps` | array | **Yes** | — | Min 1 step. See Step schema below |
| `order` | integer | No | `0` | |
| `difficulty` | enum | No | `"Beginner"` | |
| `estimatedMinutes` | integer | No | `20` | |
| `xp` | integer | No | `25` | XP on completion |
| `activity` | enum | No | `"iframe"` | iframe / terminal / code |
| `labPath` | string | No | — | Local workspace path |
| `labUrl` | string | No | — | External workspace URL |
| `tags` | string[] | No | `[]` | |
| `hints` | string[] | No | `[]` | Global lab hints |
| `checklist` | string[] | No | `[]` | |
| `checkLabel` | string | No | `"Check"` | |
| `submitLabel` | string | No | `"Submit"` | |

### Lab Step

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | string | **Yes** | — | Unique within this lab |
| `title` | string | **Yes** | — | |
| `prompt` | string | **Yes** | — | Instruction to the learner |
| `validator` | object | **Yes** | — | See validator types below |
| `hint` | string | No | — | |
| `inputLabel` | string | No | — | |
| `placeholder` | string | No | — | |
| `successMessage` | string | No | — | |

### Validator Types

| Type | Required Fields | Description |
|---|---|---|
| `exact` | `value` (string) | Learner input must match exactly |
| `oneOf` | `values` (string[], min 1) | Learner input matches any value in the list |
| `regex` | `pattern` (string), optional `flags` | Learner input matches the regex pattern |

### Quiz

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `slug` | string | **Yes** | — | |
| `title` | string | **Yes** | — | |
| `questions` | array | **Yes** | — | Min 1 question |
| `description` | string | No | `"Quiz workspace"` | |
| `order` | integer | No | `0` | |
| `difficulty` | enum | No | `"Intermediate"` | |
| `estMinutes` | integer | No | `15` | |
| `passThreshold` | integer | No | `70` | 1–100 |
| `tags` | string[] | No | `[]` | |
| `hints` | string[] | No | `[]` | |
| `checklist` | string[] | No | `[]` | |

### Quiz Question

| Field | Type | Required | Conditional | Notes |
|---|---|---|---|---|
| `id` | string | **Yes** | — | Unique within this quiz |
| `type` | enum | **Yes** | — | single / multi / short |
| `prompt` | string | **Yes** | — | The question text |
| `explanation` | string | No | — | Shown after answering |
| `options` | string[] | — | Required for single & multi | Min 2 |
| `correctIndex` | integer | — | Required for single | Zero-based |
| `correctIndices` | integer[] | — | Required for multi | Zero-based, min 1 |
| `acceptedAnswers` | string[] | — | Required for short | Min 1 |

### Activity (generic)

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `slug` | string | **Yes** | — | |
| `title` | string | **Yes** | — | |
| `description` | string | No | `"Workspace activity"` | |
| `order` | integer | No | `0` | |
| `difficulty` | enum | No | `"Intermediate"` | |
| `estMinutes` | integer | No | `15` | |
| `labPath` | string | No | — | |
| `labUrl` | string | No | — | |

---

## 5. Design Decisions & Rationale

### D1: Single-track-per-manifest (not multi-track)

**Decision:** Each manifest file describes exactly one track.

**Rationale:**
- Keeps manifests small and focused — one file per track is easy to version-control and review.
- Avoids cross-track dependency ordering issues.
- Matches the mental model: "I'm building a Linux track" → I fill out one file.
- Multiple tracks = multiple manifests, each ingested independently.

### D2: Hierarchical nesting eliminates redundant track/moduleId

**Decision:** Activities are nested inside their module, modules are nested inside the track. The ingest script derives `track` and `moduleId` from position.

**Rationale:**
- CONSTITUTION §9 requires every activity to declare track and moduleId. The manifest structure *implies* them — the author never types them.
- Eliminates the most common source of errors: mismatched or typo'd track/moduleId values.
- The ingest script reads `track.slug` and `module.id` and injects them into every generated MDX frontmatter.

### D3: manifestVersion for schema evolution

**Decision:** Top-level `manifestVersion: 1` field is required.

**Rationale:**
- The ingest script validates the version before processing. Unknown versions are rejected immediately.
- Future schema changes increment the version. Old manifests continue to work with older ingest logic (or a migration shim).
- Cost: one extra required field. Benefit: safe schema evolution without silent breakage.

### D4: Module IDs use dot-notation (not slugs)

**Decision:** Module `id` follows `prefix.category.topic` pattern (e.g., `lnx.cli.basics`).

**Rationale:**
- Matches the existing convention throughout the codebase (`pct.hardware.components-identification`, `net.fundamentals.addressing`).
- Dot-notation carries semantic hierarchy without needing the module to know its track — the prefix is just a namespace.
- The same `id` is used as both the MDX filename and the `moduleId` value in activities.

### D5: bodyFile for lesson content, bodyInline for short content

**Decision:** Lessons support `bodyFile` (path to external .md) and `bodyInline` (embedded markdown). `bodyFile` takes precedence if both are set.

**Rationale:**
- Long-form lesson content does not belong inlined in JSON — it's awkward to edit and diff.
- External .md files can be authored in any Markdown editor and are easy to review.
- `bodyInline` accommodates short lessons (1-2 paragraphs) without requiring a separate file.
- If neither is provided, the ingest script generates a placeholder body.

### D6: steps required with minItems: 1 on labs

**Decision:** Labs must declare at least one step. Empty steps arrays are invalid.

**Rationale:**
- A lab with no steps has no interactive content — it's a broken activity.
- config.ts defines a rich step schema (id, title, prompt, validator). The manifest mirrors it exactly.
- This prevents stub labs from passing validation but being useless to learners.

### D7: Questions required with minItems: 1 on quizzes

**Decision:** Quizzes must declare at least one question.

**Rationale:** Same as D6 — a quiz with no questions is not a quiz.

### D8: Slug uniqueness is cross-collection, enforced by ingest

**Decision:** All slugs (lesson, lab, quiz, activity) must be globally unique — not just unique within the manifest.

**Rationale:**
- Astro content collections use slug as the filename. Two labs named `terminal-basics.mdx` would overwrite each other.
- The ingest script should check for existing files and error on collision (unless `--overwrite` is passed).
- The schema `pattern` enforces kebab-case format.

### D9: tags included but flagged as requiring config.ts update

**Decision:** `tags` is an optional string array on lessons, labs, and quizzes in the manifest. The ingest script emits tags in frontmatter.

**Rationale:**
- Tags appear in live content (e.g., `terminal-basics.mdx` has `tags: ["terminal", "shell", "commands"]`).
- However, `tags` is not declared in the lessons collection schema in config.ts (it *is* declared in labs and quizzes).
- The manifest includes tags now so authors can start tagging content. A follow-up config.ts patch adds `tags` to the lessons schema. The ingest script emits the field regardless — Astro's content collections pass through undeclared fields in content type 'content'.

### D10: No sections in manifest — generated from module structure

**Decision:** The track schema in config.ts supports a `sections` array (for grouping activities on the track page). The manifest does not include sections.

**Rationale:**
- Sections are a *view-layer* concern — how activities display on the track page — not a *content* concern.
- The ingest script auto-generates sections from the module structure: each module becomes a section, with its lessons/labs/quizzes listed in order.
- This keeps the manifest focused on content, not layout.
- If custom section ordering is needed later, a `sections` override can be added in manifestVersion 2.

### D11: order defaults to array position

**Decision:** If `order` is omitted on a module or activity, the ingest script uses the array index (1-based).

**Rationale:**
- Authors naturally order items by position in the array. Requiring a separate `order` field for every item is tedious.
- Explicit `order` values override the default for cases where insertion order matters.

---

## 6. Known Limitations & Tradeoffs

### L1: tags on lessons requires a config.ts update

The lessons collection in `src/content/config.ts` does not currently declare `tags`. The labs and quizzes collections do. Before tags on lessons take effect in builds:

**Required action:** Add `tags: z.array(z.string()).default([])` to the lessons schema in config.ts.

The manifest schema includes tags now to avoid a manifest version bump later. The ingest script should emit tags regardless; Astro will ignore unknown frontmatter fields in content collections without erroring.

### L2: No support for tour entries

The `tour` collection in config.ts (steps for the guided tour feature) is not included in this manifest schema. Tours are a specialized UI feature tied to specific component interactions — they are better authored manually than through a generic manifest.

**Future:** If tour authoring becomes common, add a `tourSteps` array to modules in manifestVersion 2.

### L3: No support for studyGuides

Study guides are a separate content type with different semantics (they reference quizzes and hours, not individual activities). Not included in this manifest.

### L4: Body content is Markdown, not MDX

Lesson body content referenced via `bodyFile` is plain Markdown. Authors cannot use Astro components (e.g., `<Callout>`) in their .md files — those are MDX features.

**Mitigation:** The ingest script can inject standard imports (e.g., Callout) at the top of generated MDX files. Authors who need components can edit the generated MDX directly after ingest.

**Future:** If component usage becomes common, add a `components` array to lessons in manifestVersion 2 that auto-generates import lines.

### L5: Single-track manifests only

Each manifest = one track. There is no "batch ingest multiple tracks from one file" capability.

**Mitigation:** This is intentional (see D1). Multiple tracks = multiple ingest runs. A shell loop handles batching if needed: `for f in manifests/*.json; do npm run ingest:curriculum -- --manifest "$f"; done`

### L6: No content deduplication

If two manifests reference lessons with the same slug, the second ingest will fail (file exists). There is no merge/dedup logic.

**Mitigation:** Slug collisions are caught at ingest time with a clear error message. Cross-manifest content sharing is not a current requirement.

### L7: Quiz questions do not support images or rich media

Questions are plain text (`prompt` is a string). There is no field for embedding images or media in questions.

**Future:** Add an optional `media` object to questions in manifestVersion 2 if needed.

---

## 7. Generated File Mapping

The ingest script (P1-B) will use this mapping:

| Manifest Location | Generated File Path |
|---|---|
| `track` | `src/content/tracks/<track.slug>.mdx` |
| `modules[i]` | `src/content/modules/<track.slug>/<module.id>.mdx` |
| `modules[i].lessons[j]` | `src/content/lessons/<lesson.slug>.mdx` |
| `modules[i].labs[j]` | `src/content/labs/<lab.slug>.mdx` |
| `modules[i].quizzes[j]` | `src/content/quizzes/<track.slug>/<quiz.slug>.mdx` |
| `modules[i].activities[j]` | `src/content/activities/<activity.slug>.mdx` |

The ingest script injects into each activity's frontmatter:
- `track: <track.slug>`
- `moduleId: <module.id>`

These are never specified by the author in the manifest.

---

## 8. Ingest Script Contract (for P1-B)

The ingest script must:

1. **Validate** `manifestVersion === 1` before processing
2. **Validate** all required fields are present
3. **Derive** `track` and `moduleId` from nesting — never require them in the manifest
4. **Default** `order` from array position when omitted
5. **Read** `bodyFile` relative to the manifest file location
6. **Emit** valid MDX frontmatter matching config.ts schemas exactly
7. **Auto-generate** the track's `modules` array and `sections` array from the module list
8. **Reject** slug collisions with existing files (unless `--overwrite` is passed)
9. **Support** `--dry-run` to preview output without writing
10. **Exit non-zero** on any validation failure
