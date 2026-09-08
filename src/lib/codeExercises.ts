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
  'tech-plus-first-program': {
    slug: 'tech-plus-first-program',
    title: 'Your First Program: Grade Average',
    description: 'Use a variable, a loop, and output to work out a class average.',
    language: 'javascript',
    starterCode: `// Five test scores from a class.
const scores = [72, 85, 90, 64, 79];

let total = 0;
for (const score of scores) {
  total = total + score;
}

// TODO: work out the average and print "Average: <number>"
// Hint: divide total by scores.length, then use console.log
`,
    expectedOutput: 'Average: 78',
    hints: [
      'The loop has already added every score into total. You need the average next.',
      'scores.length gives you how many scores there are — 5 in this case.',
      'Print with console.log(`Average: ${average}`) using backticks.',
    ],
  },

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
};
