import { useCurrentUserQuery } from '@/features/auth/hooks/useCurrentUserQuery';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function TasksPage() {
  const navigate = useNavigate();
  const currentUserGetter = useCurrentUserQuery();

  useEffect(() => {
    if (currentUserGetter.data)
      console.log('User data; ', currentUserGetter.data);
    if (currentUserGetter.error) {
      console.log('Error:  ', currentUserGetter.error);
      navigate('/login');
    }
  }, [currentUserGetter.data, currentUserGetter.error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 text-slate-100">
      <h1 className="text-3xl font-bold">Tasks</h1>
    </div>
  );
}
