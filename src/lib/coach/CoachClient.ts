import type { ContextSnapshot } from '../contextSnapshot';

export type CoachMessageInput = {
  message: string;
  context: ContextSnapshot;
};

export type CoachMessageOutput = {
  role: 'assistant';
  content: string;
  meta: {
    provider: 'stub';
    createdAt: number;
  };
};

export class CoachClient {
  async sendMessage(input: CoachMessageInput): Promise<CoachMessageOutput> {
    const routeHint = input.context.route.labSlug
      ? `lab:${input.context.route.labSlug}`
      : input.context.route.quizSlug
        ? `quiz:${input.context.route.quizSlug}`
        : input.context.route.lessonSlug
          ? `lesson:${input.context.route.lessonSlug}`
          : input.context.route.path;

    return {
      role: 'assistant',
      content: `Coach is coming soon. Stub received your message for ${routeHint}.`,
      meta: {
        provider: 'stub',
        createdAt: Date.now(),
      },
    };
  }
}
