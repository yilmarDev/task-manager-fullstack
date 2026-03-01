import { useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { removeAccessToken } from '../utils/token';

export const useLogout = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const logout = () => {
    removeAccessToken();
    queryClient.clear();
    navigate('/login', { replace: true });
  };

  return logout;
};
