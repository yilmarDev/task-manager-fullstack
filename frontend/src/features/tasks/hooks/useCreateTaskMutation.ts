import { useMutation } from '@tanstack/react-query';
import { createTask } from '../services/tasks';

export const useCreateTaskMutation = () => {
  const mutation = useMutation({
    mutationFn: createTask,
  });

  return mutation;
};
