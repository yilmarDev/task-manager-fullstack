import { LeftPanel } from '@/features/auth/components/LeftPanel';
import { LoginForm } from '@/features/auth/components/LoginForm';

export const LoginPage = () => {
  return (
    <div className="flex min-h-screen bg-background">
      {/* Left decorative panel -- hidden on mobile */}
      <LeftPanel />

      {/* Right form panel */}
      <LoginForm />
    </div>
  );
};
