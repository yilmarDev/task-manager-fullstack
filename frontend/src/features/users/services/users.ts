import { apiConn } from '@/shared/api';
import type { GetUsersResponse } from '../interfaces/users';

export const getUsers = async (): Promise<GetUsersResponse> => {
  const { data } = await apiConn.get<GetUsersResponse>(`/users`);
  return data;
};
