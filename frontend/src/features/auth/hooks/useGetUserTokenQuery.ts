import { useQuery } from '@tanstack/react-query';
import { getUserToken } from '../services/auth';
import type { LoginTokenPayload } from '../interfaces/auth';

export const useGetUserTokenQuery = (credentials: LoginTokenPayload) => {
  const query = useQuery({
    queryKey: ['userToken', credentials.username],
    queryFn: () => getUserToken(credentials),
    // refetchOnWindowFocus: false,
    // staleTime: 10000 * 60,
    // retry: false,
    // enabled: !!credentials.username && !!credentials.password,
  });

  return query;
};
