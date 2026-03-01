'use client';

import { ListTodo, Clock, Eye, CheckCircle2 } from 'lucide-react';
import type { Task } from '@/shared/data';

interface StatsCardsProps {
  tasks: Task[];
}

const statConfig = [
  {
    label: 'To Do',
    status: 'todo' as const,
    icon: ListTodo,
    colorClass: 'text-muted-foreground bg-muted',
  },
  {
    label: 'In Progress',
    status: 'in-progress' as const,
    icon: Clock,
    colorClass: 'text-primary bg-primary/10',
  },
  {
    label: 'In Review',
    status: 'in-review' as const,
    icon: Eye,
    colorClass: 'text-amber-600 bg-amber-50',
  },
  {
    label: 'Completed',
    status: 'completed' as const,
    icon: CheckCircle2,
    colorClass: 'text-emerald-600 bg-emerald-50',
  },
];

export function StatsCards({ tasks }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {statConfig.map((stat) => {
        const count = tasks.filter((t) => t.status === stat.status).length;
        return (
          <div
            key={stat.status}
            className="bg-card rounded-xl border border-border p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-muted-foreground">
                {stat.label}
              </span>
              <div
                className={`flex items-center justify-center size-9 rounded-lg ${stat.colorClass}`}
              >
                <stat.icon className="size-[18px]" />
              </div>
            </div>
            <p className="text-2xl font-bold text-foreground tracking-tight">
              {count}
            </p>
          </div>
        );
      })}
    </div>
  );
}
