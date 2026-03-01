import { useQuery } from '@tanstack/react-query';
import { getUsers } from '../services/users';

export const useUsersQuery = () => {
  const query = useQuery({
    queryFn: () => getUsers(),
    queryKey: ['users'],
    refetchOnWindowFocus: false,
  });

  return query;
};
