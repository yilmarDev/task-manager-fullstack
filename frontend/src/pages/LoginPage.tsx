import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

import { LeftPanel } from '@/features/auth/components/LeftPanel';
import { LoginForm } from '@/features/auth/components/LoginForm';
import { getAccessToken, isTokenExpired } from '@/features/auth/utils/token';

export const LoginPage = () => {
  const [checking, setChecking] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (getAccessToken() && !isTokenExpired()) {
      navigate('/tasks', { replace: true });
    } else {
      setChecking(false);
    }
  }, [navigate]);

  if (checking) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Loader2 className="size-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background">
      {/* Left decorative panel -- hidden on mobile */}
      <LeftPanel />

      {/* Right form panel */}
      <LoginForm />
    </div>
  );
};
