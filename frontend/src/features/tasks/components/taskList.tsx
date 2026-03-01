'use client';

import { Plus, ListFilter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { Task, TaskStatus } from '@/shared/data';
import { useEffect, useState } from 'react';
import { TaskCard } from './taskCard';
import { useAsignedTasksQuery } from '../hooks/useAsignedTasksQuery';
import type { AssignedTask } from '../interfaces/tasks';

interface TaskListProps {
  tasks: AssignedTask[];
  onCreateTask: () => void;
}

const filters: { label: string; value: TaskStatus | 'all' }[] = [
  { label: 'All Tasks', value: 'all' },
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'in_progress' },
  // { label: 'In Review', value: 'in-review' },
  { label: 'Completed', value: 'completed' },
];

export function TaskList({tasks, onCreateTask }: TaskListProps) {
  // const [tasks, setTasks] = useState<AssignedTask[]>();
  const [activeFilter, setActiveFilter] = useState<TaskStatus | 'all'>('all');

  // const tasksGetter = useAsignedTasksQuery();

  const filteredTasks =
    activeFilter === 'all'
      ? tasks
      : tasks?.filter((t) => t.status === activeFilter);

  // useEffect(() => {
  //   if (tasksGetter.data) {
  //     console.log('Tasks list:', tasksGetter.data);
  //     setTasks(tasksGetter.data);
  //   }
  //   if (tasksGetter.error) console.log('Tasks error: ', tasksGetter.error);
  // }, [tasksGetter.data, tasksGetter.error]);

  return (
    <div>
      {/* Section header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
        <div className="flex items-center gap-2.5">
          <ListFilter className="size-[18px] text-muted-foreground" />
          <h2 className="text-lg font-semibold text-foreground">Tasks</h2>
          <span className="text-sm text-muted-foreground">
            ({filteredTasks?.length})
          </span>
        </div>
        <Button
          onClick={onCreateTask}
          className="sm:hidden bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Plus className="size-4 mr-1.5" />
          New Task
        </Button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-1.5 mb-5 overflow-x-auto pb-1">
        {filters.map((filter) => (
          <button
            key={filter.value}
            onClick={() => setActiveFilter(filter.value)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
              activeFilter === filter.value
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            {filter.label}
          </button>
        ))}
      </div>

      {/* Task cards */}
      <div className="flex flex-col gap-3">
        {filteredTasks?.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="flex items-center justify-center size-12 rounded-xl bg-muted mb-4">
              <ListFilter className="size-5 text-muted-foreground" />
            </div>
            <p className="text-sm font-medium text-foreground mb-1">
              No tasks found
            </p>
            <p className="text-sm text-muted-foreground">
              Try adjusting your filter or create a new task.
            </p>
          </div>
        ) : (
          filteredTasks?.map((task) => <TaskCard key={task.id} task={task} />)
        )}
      </div>
    </div>
  );
}
