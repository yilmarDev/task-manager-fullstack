import { useCurrentUserQuery } from '@/features/auth/hooks/useCurrentUserQuery';
import { useLogout } from '@/features/auth/hooks/useLogout';
import { Button } from '@/components/ui/button';
import { LogOut } from 'lucide-react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function TasksPage() {
  const navigate = useNavigate();
  const currentUserGetter = useCurrentUserQuery();
  const logout = useLogout();

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
      <div className="flex flex-col items-center gap-6">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <Button variant="outline" onClick={logout} className="gap-2">
          <LogOut className="size-4" />
          Log out
        </Button>
      </div>
    </div>
  );
}
