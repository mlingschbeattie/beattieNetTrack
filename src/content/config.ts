import { defineCollection, z } from 'astro:content';

const difficultySchema = z.preprocess(
  (value) => {
    if (typeof value !== 'string') return 'Intermediate';
    const lower = value.toLowerCase();
    if (lower === 'easy' || lower === 'beginner') return 'Beginner';
    if (lower === 'medium' || lower === 'intermediate') return 'Intermediate';
    if (lower === 'hard' || lower === 'advanced') return 'Advanced';
    return 'Intermediate';
  },
  z.enum(['Beginner', 'Intermediate', 'Advanced'])
);

const tracks = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default('Hands-on lab workspace.'),
    slug: z.string().optional(),
    order: z.number().int().default(0),
    hidden: z.boolean().optional().default(false),
    level: z.string().optional(),
    icon: z.string().optional(),
    estimatedHours: z.number().int().optional(),
    modules: z.array(z.string()).default([]),
    sections: z
      .array(
        z.object({
          title: z.string(),
          lessons: z
            .array(
              z.preprocess(
                (value) => {
                  if (typeof value === 'string') {
                    return { type: 'lesson', slug: value };
                  }
                  return value;
                },
                z.object({
                  type: z.enum(['lesson', 'lab', 'quiz']),
                  slug: z.string(),
                })
              )
            )
            .default([]),
        })
      )
      .default([]),
  }),
});

const modules = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default(''),
    slug: z.string().optional(),
    track: z.string(),
    moduleId: z.string(),
    order: z.number().int().default(0),
  }),
});

const domainMappingSchema = z
  .array(z.object({ domainId: z.string(), weight: z.number().min(0).max(1) }))
  .optional()
  .default([]);

const labs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    slug: z.string().optional(),
    hidden: z.boolean().optional().default(false),
    type: z.literal('lab').optional().default('lab'),
    order: z.number().int().default(0),
    estimatedMinutes: z.preprocess(
      (value) => (typeof value === 'number' ? value : 20),
      z.number().int().default(20)
    ),
    difficulty: difficultySchema,
    xp: z.number().int().default(25),
    steps: z
      .array(
        z.object({
          id: z.string(),
          title: z.string(),
          prompt: z.string(),
          inputLabel: z.string().optional(),
          placeholder: z.string().optional(),
          hint: z.string().optional(),
          validator: z.discriminatedUnion('type', [
            z.object({
              type: z.literal('exact'),
              value: z.string(),
            }),
            z.object({
              type: z.literal('oneOf'),
              values: z.array(z.string()).min(1),
            }),
            z.object({
              type: z.literal('regex'),
              pattern: z.string(),
              flags: z.string().optional(),
            }),
          ]),
          successMessage: z.string().optional(),
        })
      )
      .default([]),

    // Backward-compatible workspace metadata
    track: z.string().trim().min(1, 'track is required for mapped activities'),
    moduleId: z.string().trim().min(1, 'moduleId is required for mapped activities'),
    module: z.string().optional(),
    estMinutes: z.number().int().optional(),
    tags: z.array(z.string()).default([]),
    activity: z.enum(['iframe', 'terminal', 'code']).optional().default('iframe'),
    labPath: z.string().optional(),
    labUrl: z.string().optional(),
    checkLabel: z.string().optional().default('Check'),
    submitLabel: z.string().optional().default('Submit'),
    hints: z.array(z.string()).default([]),
    checklist: z.array(z.string()).default([]),
    domains: domainMappingSchema,
  }),
});

const quizzes = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default('Quiz workspace'),
    slug: z.string().optional(),
    type: z.literal('quiz').optional().default('quiz'),
    track: z.string().trim().min(1, 'track is required for mapped activities'),
    moduleId: z.string().trim().min(1, 'moduleId is required for mapped activities'),
    module: z.string().optional(),
    order: z.number().int().default(0),
    difficulty: difficultySchema.optional().default('Intermediate'),
    estMinutes: z.number().int().optional().default(15),
    passThreshold: z.number().int().min(1).max(100).default(70),
    tags: z.array(z.string()).default([]),
    quizJsonPath: z.string().optional(),
    hints: z.array(z.string()).default([]),
    checklist: z.array(z.string()).default([]),
    domains: domainMappingSchema,
    questions: z
      .array(
        z.discriminatedUnion('type', [
          z.object({
            id: z.string(),
            type: z.literal('single'),
            prompt: z.string(),
            options: z.array(z.string()).min(2),
            correctIndex: z.number().int().min(0),
            explanation: z.string().optional(),
          }),
          z.object({
            id: z.string(),
            type: z.literal('multi'),
            prompt: z.string(),
            options: z.array(z.string()).min(2),
            correctIndices: z.array(z.number().int().min(0)).min(1),
            explanation: z.string().optional(),
          }),
          z.object({
            id: z.string(),
            type: z.literal('short'),
            prompt: z.string(),
            acceptedAnswers: z.array(z.string()).min(1),
            explanation: z.string().optional(),
          }),
        ])
      )
      .default([]),
  }),
});

const activities = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default('Workspace activity'),
    slug: z.string().optional(),
    type: z.literal('activity').optional().default('activity'),
    track: z.string().trim().min(1, 'track is required for mapped activities'),
    moduleId: z.string().trim().min(1, 'moduleId is required for mapped activities'),
    order: z.number().int().default(0),
    difficulty: difficultySchema.optional().default('Intermediate'),
    estMinutes: z.number().int().optional().default(15),
    labPath: z.string().optional(),
    labUrl: z.string().optional(),
    domains: domainMappingSchema,
  }),
});

const sectionCheck = z.object({
  prompt: z.string(),
  options: z.array(z.string()).length(4),
  correct: z.number().int().min(0).max(3),
});

const lessonSection = z.object({
  id: z.string(),
  title: z.string(),
  keyPoints: z.array(z.string()).min(2).max(4),
  check: z.array(sectionCheck).length(2),
});

const lessons = defineCollection({
  type: 'content',
  schema: z
    .object({
      title: z.string(),
      description: z.string().optional().default('Legacy page - being upgraded.'),
      slug: z.string().optional(),
      track: z.string().optional(),
      moduleId: z.string().optional(),
      module: z.string().optional(),
      order: z.number().int().optional(),
      difficulty: difficultySchema.optional().default('Intermediate'),
      estMinutes: z.number().int().optional().default(15),
      estimatedMinutes: z.number().int().optional(),
      tags: z.array(z.string()).default([]),
      legacyUrl: z.string().optional(),
      domains: domainMappingSchema,
      sections: z.array(lessonSection).optional(),
    })
    .superRefine((data, ctx) => {
      const track = (data.track ?? '').trim();
      if (!track) return;
      const moduleId = (data.moduleId ?? '').trim();
      const module = (data.module ?? '').trim();
      if (!moduleId && !module) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ['moduleId'],
          message: 'When track is set, either moduleId or module is required.',
        });
      }
    }),
});

const tour = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional().default('Tour step'),
    slug: z.string().optional(),
    track: z.string(),
    moduleId: z.string(),
    order: z.number().int(),
    kind: z.enum(['intro', 'terminal', 'quiz', 'code', 'complete']),
    next: z.string().optional(),
    ctaLabel: z.string().optional(),
    terminalScenario: z.string().optional(),
    quizSlug: z.string().optional(),
    codeExercise: z.string().optional(),
  }),
});

const studyGuides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    track: z.string(),
    quizzes: z.number().int(),
    hours: z.union([z.number(), z.string()]),
    order: z.number().int(),
    isDraft: z.boolean().optional().default(false),
  }),
});

export const collections = {
  tracks,
  modules,
  labs,
  quizzes,
  activities,
  lessons,
  tour,
  studyGuides,
};
