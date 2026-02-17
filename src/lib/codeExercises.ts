export type CodeExercise = {
  slug: string;
  title: string;
  description: string;
  language: 'javascript';
  starterCode: string;
  expectedOutput: string;
  hints: string[];
};

export const codeExercises: Record<string, CodeExercise> = {
  'code-basics': {
    slug: 'code-basics',
    title: 'Code Basics: Packet Counter',
    description: 'Write JavaScript that prints a packet counter summary.',
    language: 'javascript',
    starterCode: `const packets = [12, 15, 20, 18];\nconst total = packets.reduce((sum, value) => sum + value, 0);\n\n// TODO: print \"Total packets: <number>\"\n`,
    expectedOutput: 'Total packets: 65',
    hints: [
      'Use console.log to print output.',
      'Template literals make output easier: `Total packets: ${total}`.',
    ],
  },
  'tour-code-challenge': {
    slug: 'tour-code-challenge',
    title: 'Tour Code Challenge',
    description: 'Print the sum of two values to pass this challenge.',
    language: 'javascript',
    starterCode: `const a = 7;\nconst b = 5;\n// TODO: print the sum`,
    expectedOutput: '12',
    hints: ['Try console.log(a + b).'],
  },
};
