import { useMutation } from '@tanstack/react-query';
import { getUserToken } from '../services/auth';
import type { LoginTokenPayload, LoginTokenResponse } from '../interfaces/auth';

export const useGetUserTokenQuery = () => {
  const mutation = useMutation<LoginTokenResponse, Error, LoginTokenPayload>({
    mutationFn: (credentials: LoginTokenPayload) => getUserToken(credentials),
  });

  return mutation;
};
