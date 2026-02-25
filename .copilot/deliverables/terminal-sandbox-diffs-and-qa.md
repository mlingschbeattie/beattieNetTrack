# Terminal Sandbox: Diffs and QA

This file consolidates the unified diff and QA checks produced in the last change set.

## Unified Diff

The unified diff produced is included below.

```diff
diff --git a/src/content/config.ts b/src/content/config.ts
index 37e43f5..5f1e770 100644
--- a/src/content/config.ts
+++ b/src/content/config.ts
@@ -61,63 +61,145 @@ const modules = defineCollection({
	 }),
 });
 
-const labs = defineCollection({
-  type: 'content',
-  schema: z.object({
-    title: z.string(),
-    description: z.string(),
-    slug: z.string().optional(),
-    type: z.literal('lab').optional().default('lab'),
-    order: z.number().int().default(0),
-    estimatedMinutes: z.preprocess(
-      (value) => (typeof value === 'number' ? value : 20),
-      z.number().int().default(20)
-    ),
-    difficulty: difficultySchema,
-    xp: z.number().int().default(25),
-    steps: z
-      .array(
-        z.object({
-          id: z.string(),
-          title: z.string(),
-          prompt: z.string(),
-          inputLabel: z.string().optional(),
-          placeholder: z.string().optional(),
-          hint: z.string().optional(),
-          validator: z.discriminatedUnion('type', [
-            z.object({
-              type: z.literal('exact'),
-              value: z.string(),
-            }),
-            z.object({
-              type: z.literal('oneOf'),
-              values: z.array(z.string()).min(1),
-            }),
-            z.object({
-              type: z.literal('regex'),
-              pattern: z.string(),
-              flags: z.string().optional(),
-            }),
-          ]),
-          successMessage: z.string().optional(),
-        })
-      )
-      .default([]),
-    
-    // Backward-compatible workspace metadata
-    track: z.string().trim().min(1, 'track is required for mapped activities'),
-    moduleId: z.string().trim().min(1, 'moduleId is required for mapped activities'),
-    module: z.string().optional(),
-    estMinutes: z.number().int().optional(),
-    tags: z.array(z.string()).default([]),
-    activity: z.enum(['iframe', 'terminal', 'code']).optional().default('iframe'),
-    labPath: z.string().optional(),
-    labUrl: z.string().optional(),
-    checkLabel: z.string().optional().default('Check'),
-    submitLabel: z.string().optional().default('Submit'),
-    hints: z.array(z.string()).default([]),
-    checklist: z.array(z.string()).default([]),
-  }),
-});
+const fsNodeSchema: z.ZodType<any> = z.lazy(() =>
+  z.union([
+    z.object({
+      type: z.literal('dir'),
+      children: z.record(fsNodeSchema),
+    }),
+    z.object({
+      type: z.literal('file'),
+      content: z.string(),
+    }),
+  ])
+);
+
+const terminalSpecSchema = z.object({
+  version: z.literal(1),
+  prompt: z.string(),
+  initialCwd: z.string(),
+  fs: fsNodeSchema,
+  allowedCommands: z.array(z.string()).default([]),
+  objectives: z
+    .array(
+      z.discriminatedUnion('kind', [
+        z.object({
+          id: z.string(),
+          label: z.string(),
+          kind: z.literal('fs'),
+          pass: z.discriminatedUnion('type', [
+            z.object({
+              type: z.literal('pathExists'),
+              path: z.string(),
+              nodeType: z.enum(['dir', 'file']),
+            }),
+            z.object({
+              type: z.literal('fileContains'),
+              path: z.string(),
+              substring: z.string(),
+            }),
+          ]),
+        }),
+        z.object({
+          id: z.string(),
+          label: z.string(),
+          kind: z.literal('cwd'),
+          pass: z.object({
+            type: z.literal('cwdIs'),
+            path: z.string(),
+          }),
+        }),
+        z.object({
+          id: z.string(),
+          label: z.string(),
+          kind: z.literal('history'),
+          pass: z.discriminatedUnion('type', [
+            z.object({
+              type: z.literal('historyIncludes'),
+              value: z.string(),
+            }),
+            z.object({
+              type: z.literal('historyMatches'),
+              pattern: z.string(),
+              flags: z.string().optional(),
+            }),
+          ]),
+        }),
+      ])
+    )
+    .default([]),
+});
+
 
+const labs = defineCollection({
+  type: 'content',
+  schema: z
+    .object({
+      title: z.string(),
+      description: z.string(),
+      slug: z.string().optional(),
+      type: z.literal('lab').optional().default('lab'),
+      order: z.number().int().default(0),
+      estimatedMinutes: z.preprocess(
+        (value) => (typeof value === 'number' ? value : 20),
+        z.number().int().default(20)
+      ),
+      difficulty: difficultySchema,
+      tier: z.enum(['guided', 'state-machine', 'sandbox']).default('guided'),
+      engine: z.enum(['steps', 'sim-sandbox-terminal']).default('steps'),
+      xp: z.number().int().default(25),
+      steps: z
+        .array(
+          z.object({
+            id: z.string(),
+            title: z.string(),
+            prompt: z.string(),
+            inputLabel: z.string().optional(),
+            placeholder: z.string().optional(),
+            hint: z.string().optional(),
+            validator: z.discriminatedUnion('type', [
+              z.object({
+                type: z.literal('exact'),
+                value: z.string(),
+              }),
+              z.object({
+                type: z.literal('oneOf'),
+                values: z.array(z.string()).min(1),
+              }),
+              z.object({
+                type: z.literal('regex'),
+                pattern: z.string(),
+                flags: z.string().optional(),
+              }),
+            ]),
+            successMessage: z.string().optional(),
+          })
+        )
+        .default([]),
+      terminalSpec: terminalSpecSchema.optional(),
+
+      // Backward-compatible workspace metadata
+      track: z.string().trim().min(1, 'track is required for mapped activities'),
+      moduleId: z.string().trim().min(1, 'moduleId is required for mapped activities'),
+      module: z.string().optional(),
+      estMinutes: z.number().int().optional(),
+      tags: z.array(z.string()).default([]),
+      activity: z.enum(['iframe', 'terminal', 'code']).optional().default('iframe'),
+      labPath: z.string().optional(),
+      labUrl: z.string().optional(),
+      checkLabel: z.string().optional().default('Check'),
+      submitLabel: z.string().optional().default('Submit'),
+      hints: z.array(z.string()).default([]),
+      checklist: z.array(z.string()).default([]),
+    })
+    .superRefine((value, ctx) => {
+      if (value.engine === 'sim-sandbox-terminal' && !value.terminalSpec) {
+        ctx.addIssue({
+          code: z.ZodIssueCode.custom,
+          path: ['terminalSpec'],
+          message: 'terminalSpec is required when engine is sim-sandbox-terminal.',
+        });
+      }
+    }),
+});
@@
```

> Note: the full diff is available at [.copilot/deliverables/terminal-sandbox-reference-lab.diff](.copilot/deliverables/terminal-sandbox-reference-lab.diff).

## QA Log

The QA log from running `npm run test:ci` follows.

```log
(see .copilot/deliverables/terminal-sandbox-reference-lab-qa.log)
```

> Note: the full QA log is available at [.copilot/deliverables/terminal-sandbox-reference-lab-qa.log](.copilot/deliverables/terminal-sandbox-reference-lab-qa.log).

---

If you want, I can inline the full diff and QA logs into this Markdown file (it will grow large). Right now the file links to the two deliverable artifacts saved in `.copilot/deliverables`.
