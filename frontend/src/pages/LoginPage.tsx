import { LeftPanel } from '@/components/login/LeftPanel';
import { LoginForm } from '@/components/login/LoginForm';

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
