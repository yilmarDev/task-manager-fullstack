import { apiConn } from '@/shared/api';
import type {
  CreateTaskPayload,
  CreateTaskResponse,
} from '../interfaces/tasks';

export const createTask = async (
  payload: CreateTaskPayload,
): Promise<CreateTaskResponse> => {
  const { data } = await apiConn.post<CreateTaskResponse>(`/tasks`, payload);
  return data;
};
