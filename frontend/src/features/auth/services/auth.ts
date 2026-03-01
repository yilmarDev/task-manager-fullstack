import { apiConn } from '@/shared/api';
import type { LoginTokenPayload, LoginTokenResponse } from '../interfaces/auth';

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
