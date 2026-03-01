import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createTask } from '../services/tasks';

export const useCreateTaskMutation = () => {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignedTasks'] });
    },
  });

  return mutation;
};
