import { apiConn } from '@/shared/api';
import type {
  GetUserResponse,
  LoginTokenPayload,
  LoginTokenResponse,
} from '../interfaces/auth';
import { getUserIdFromToken } from '../utils/token';

export const getUserToken = async (
  credentials: LoginTokenPayload,
): Promise<LoginTokenResponse> => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  const { data } = await apiConn.post<LoginTokenResponse>(
    `/auth/login`,
    formData,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    },
  );

  return data;
};

export const getCurrentUser = async (): Promise<GetUserResponse | null> => {
  const id = getUserIdFromToken();
  if (!id) return null;

  const { data } = await apiConn.get<GetUserResponse>(`/users/${id}`);
  return data;
};
