export type TaskStatus = 'todo' | 'in-progress' | 'in-review' | 'completed';

export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  role: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  dueDate: string;
  createdAt: string;
  assignedTo: User;
}

export const currentUser: User = {
  id: 'u1',
  name: 'Alexandra Chen',
  email: 'alex.chen@taskflow.io',
  avatar: 'AC',
  role: 'Product Manager',
};

export const teamMembers: User[] = [
  currentUser,
  {
    id: 'u2',
    name: 'Marcus Johnson',
    email: 'marcus.j@taskflow.io',
    avatar: 'MJ',
    role: 'Frontend Developer',
  },
  {
    id: 'u3',
    name: 'Sophia Rivera',
    email: 'sophia.r@taskflow.io',
    avatar: 'SR',
    role: 'UX Designer',
  },
  {
    id: 'u4',
    name: 'James Wilson',
    email: 'james.w@taskflow.io',
    avatar: 'JW',
    role: 'Backend Developer',
  },
  {
    id: 'u5',
    name: 'Priya Patel',
    email: 'priya.p@taskflow.io',
    avatar: 'PP',
    role: 'QA Engineer',
  },
  {
    id: 'u6',
    name: 'Oliver Kim',
    email: 'oliver.k@taskflow.io',
    avatar: 'OK',
    role: 'DevOps Engineer',
  },
];

export const initialTasks: Task[] = [
  {
    id: 't1',
    title: 'Design system token audit',
    description:
      'Review and update all design tokens to ensure consistency across the component library. Document any breaking changes.',
    status: 'in-progress',
    dueDate: '2026-03-05',
    createdAt: '2026-02-20',
    assignedTo: teamMembers[2] || currentUser,
  },
  {
    id: 't2',
    title: 'API rate limiting implementation',
    description:
      'Implement rate limiting on all public API endpoints using a sliding window algorithm. Include proper 429 response handling.',
    status: 'todo',
    dueDate: '2026-03-10',
    createdAt: '2026-02-22',
    assignedTo: teamMembers[3] || currentUser,
  },
  {
    id: 't3',
    title: 'Onboarding flow user testing',
    description:
      'Conduct usability testing with 8 participants for the new onboarding wizard. Compile findings into a report with recommendations.',
    status: 'in-review',
    dueDate: '2026-03-01',
    createdAt: '2026-02-18',
    assignedTo: teamMembers[2] || currentUser,
  },
  {
    id: 't4',
    title: 'Database migration to v3 schema',
    description:
      'Migrate all production tables to the new v3 schema. Ensure zero-downtime deployment with proper rollback procedures.',
    status: 'completed',
    dueDate: '2026-02-25',
    createdAt: '2026-02-10',
    assignedTo: teamMembers[5] || currentUser,
  },
  {
    id: 't5',
    title: 'Performance monitoring dashboard',
    description:
      'Build a real-time performance monitoring dashboard showing key metrics like p95 latency, error rates, and throughput.',
    status: 'todo',
    dueDate: '2026-03-15',
    createdAt: '2026-02-25',
    assignedTo: teamMembers[1] || currentUser,
  },
  {
    id: 't6',
    title: 'End-to-end test suite expansion',
    description:
      'Add comprehensive E2E tests for the checkout flow, user settings, and team management modules using Playwright.',
    status: 'in-progress',
    dueDate: '2026-03-08',
    createdAt: '2026-02-21',
    assignedTo: teamMembers[4] || currentUser,
  },
];
