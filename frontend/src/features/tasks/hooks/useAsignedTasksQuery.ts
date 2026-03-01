import { useQuery } from '@tanstack/react-query';
import { getTasksList } from '../services/tasks';

export const useAsignedTasksQuery = () => {
  const query = useQuery({
    queryFn: () => getTasksList(),
    queryKey: ['assignedTasks'],
  });

  return query;
};
