'use client';

import { CalendarDays, Clock } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import type { Task, TaskStatus } from '@/shared/data';
import { format, parseISO } from 'date-fns';

const statusConfig: Record<TaskStatus, { label: string; className: string }> = {
  todo: {
    label: 'To Do',
    className:
      'bg-muted text-muted-foreground border-transparent hover:bg-muted',
  },
  'in-progress': {
    label: 'In Progress',
    className:
      'bg-primary/10 text-primary border-transparent hover:bg-primary/15',
  },
  'in-review': {
    label: 'In Review',
    className:
      'bg-amber-50 text-amber-700 border-transparent hover:bg-amber-100',
  },
  completed: {
    label: 'Completed',
    className:
      'bg-emerald-50 text-emerald-700 border-transparent hover:bg-emerald-100',
  },
};

interface TaskCardProps {
  task: Task;
}

export function TaskCard({ task }: TaskCardProps) {
  const config = statusConfig[task.status];

  return (
    <div className="group bg-card rounded-xl border border-border p-5 transition-all hover:shadow-md hover:border-primary/20">
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        {/* Left content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2.5 mb-1.5">
            <h3 className="font-semibold text-foreground text-[15px] leading-snug truncate">
              {task.title}
            </h3>
            <Badge className={config.className}>{config.label}</Badge>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2">
            {task.description}
          </p>
        </div>

        {/* Assigned user */}
        <div className="flex items-center gap-2 shrink-0 sm:ml-4">
          <Avatar className="size-7">
            <AvatarFallback className="bg-primary/10 text-primary text-[10px] font-semibold">
              {task.assignedTo.avatar}
            </AvatarFallback>
          </Avatar>
          <span className="text-xs font-medium text-muted-foreground sm:hidden">
            {task.assignedTo.name}
          </span>
        </div>
      </div>

      {/* Meta */}
      <div className="flex items-center gap-4 mt-4 pt-4 border-t border-border">
        <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
          <CalendarDays className="size-3.5" />
          <span>Due {format(parseISO(task.dueDate), 'MMM d, yyyy')}</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
          <Clock className="size-3.5" />
          <span>Created {format(parseISO(task.createdAt), 'MMM d, yyyy')}</span>
        </div>
        <div className="hidden sm:flex items-center gap-1.5 ml-auto">
          <Avatar className="size-5">
            <AvatarFallback className="bg-primary/10 text-primary text-[8px] font-semibold">
              {task.assignedTo.avatar}
            </AvatarFallback>
          </Avatar>
          <span className="text-xs text-muted-foreground">
            {task.assignedTo.name}
          </span>
        </div>
      </div>
    </div>
  );
}
