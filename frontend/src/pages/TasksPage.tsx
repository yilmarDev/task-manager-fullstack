import { useCurrentUserQuery } from '@/features/auth/hooks/useCurrentUserQuery';
import { useLogout } from '@/features/auth/hooks/useLogout';
import { DashboardHeader } from '@/features/tasks/components/dashboardHeader';
import { DashboardSidebar } from '@/features/tasks/components/dashboardSidebar';
import { StatsCards } from '@/features/tasks/components/statsCards';
import { TaskList } from '@/features/tasks/components/taskList';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import type { Task } from '@/shared/data';
import { CreateTaskModal } from '@/features/tasks/components/createTaskModal';
import { initialTasks, type Task } from '@/shared/data';

export function TasksPage() {
  const navigate = useNavigate();
  const currentUserGetter = useCurrentUserQuery();
  const logout = useLogout();

  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [modalOpen, setModalOpen] = useState(false);

  function handleCreateTask(taskData: Omit<Task, 'id' | 'createdAt'>) {
    const newTask: Task = {
      ...taskData,
      id: `t${Date.now()}`,
      createdAt: new Date().toISOString().split('T')[0] || '',
    };
    setTasks((prev) => [newTask, ...prev]);
  }

  useEffect(() => {
    if (currentUserGetter.data)
      console.log('User data; ', currentUserGetter.data);
    if (currentUserGetter.error) {
      console.log('Error:  ', currentUserGetter.error);
      navigate('/login');
    }
  }, [currentUserGetter.data, currentUserGetter.error]);

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <DashboardSidebar />

      <div className="flex flex-col flex-1 min-w-0">
        <DashboardHeader onCreateTask={() => setModalOpen(true)} />

        <main className="flex-1 overflow-y-auto">
          <div className="max-w-5xl mx-auto px-4 lg:px-8 py-8">
            {/* Page title */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-foreground tracking-tight text-balance">
                Dashboard
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Track and manage your team&apos;s tasks in one place.
              </p>
            </div>

            {/* Stats */}
            <div className="mb-8">
              <StatsCards tasks={tasks} />
            </div>

            {/* Task list */}
            <TaskList tasks={tasks} onCreateTask={() => setModalOpen(true)} />
          </div>
        </main>
      </div>

      <CreateTaskModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        onCreateTask={handleCreateTask}
      />
    </div>
  );
}
