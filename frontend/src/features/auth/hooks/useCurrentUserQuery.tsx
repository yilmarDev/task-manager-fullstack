import { useQuery } from '@tanstack/react-query';
import { getCurrentUser } from '../services/auth';

export const useCurrentUserQuery = () => {
  const query = useQuery({
    queryKey: ['currentUser'],
    queryFn: () => getCurrentUser(),
    refetchOnWindowFocus: false,
    retry: false,
    staleTime: 1000 * 60 * 5,
  });

  return query;
};
