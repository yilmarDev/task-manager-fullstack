import { apiConn } from '@/shared/api';
import type {
  CreateTaskPayload,
  CreateTaskResponse,
  GetAssignedTasksResponse,
} from '../interfaces/tasks';

export const createTask = async (
  payload: CreateTaskPayload,
): Promise<CreateTaskResponse> => {
  const { data } = await apiConn.post<CreateTaskResponse>(`tasks`, payload);
  return data;
};

export const getTasksList = async (): Promise<GetAssignedTasksResponse> => {
  const { data } =
    await apiConn.get<GetAssignedTasksResponse>(`tasks/assigned`);
  return data;
};
