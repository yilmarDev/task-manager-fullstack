import { useState } from 'react';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, Controller } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/components/ui/use-toast';
import { useNavigate } from 'react-router-dom';

import { ArrowRight, CheckSquare, Eye, EyeOff, Lock, Mail } from 'lucide-react';
import { useUserTokenQuery } from '../hooks/useUserTokenQuery';

type Props = {};

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  remember: z.boolean().optional(),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export const LoginForm = (props: Props) => {
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();
  const loginTokenMutation = useUserTokenQuery();
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
      remember: false,
    },
  });

  const onSubmit = async (values: LoginFormValues) => {
    try {
      const data = await loginTokenMutation.mutateAsync({
        username: values.email,
        password: values.password,
      });

      console.log('Token info', data);
      localStorage.setItem('Authorization', data.access_token);

      toast({
        title: 'Welcome back! 🎉',
        description: 'You have logged in successfully.',
        variant: 'success',
      });

      navigate('/tasks');
    } catch (error) {
      console.error('Login error::::::', error);
      toast({
        title: 'Login failed',
        description: 'Invalid email or password. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <>
      <div className="flex flex-1 flex-col items-center justify-center px-6 py-12 sm:px-12">
        {/* Mobile logo */}
        <div className="mb-8 flex items-center gap-3 lg:hidden">
          <div className="flex size-9 items-center justify-center rounded-lg bg-primary">
            <CheckSquare className="size-4.5 text-primary-foreground" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-foreground">
            TaskFlow
          </span>
        </div>

        <div className="w-full max-w-100">
          {/* Heading */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold tracking-tight text-foreground text-balance">
              Welcome back
            </h1>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
              Enter your credentials to access your dashboard.
            </p>
          </div>

          {/* Auth card */}
          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <form
              onSubmit={handleSubmit(onSubmit)}
              className="flex flex-col gap-5"
            >
              {/* Email */}
              <div className="flex flex-col gap-2">
                <Label htmlFor="email">Email address</Label>
                <div className="relative">
                  <Mail className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                  <input
                    id="email"
                    type="email"
                    autoComplete="email"
                    placeholder="you@company.com"
                    {...register('email')}
                    className="flex h-10 w-full rounded-lg border border-input bg-transparent pl-10 pr-3 text-sm text-foreground placeholder:text-muted-foreground/60 shadow-xs transition-all outline-none focus:border-ring focus:ring-[3px] focus:ring-ring/50"
                  />
                  {errors.email && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.email.message}
                    </p>
                  )}
                </div>
              </div>

              {/* Password */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password">Password</Label>
                  <button
                    type="button"
                    className="text-xs font-medium text-primary hover:text-primary/80 transition-colors"
                  >
                    Forgot password?
                  </button>
                </div>
                <div className="relative">
                  <Lock className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    placeholder="Enter your password"
                    {...register('password')}
                    className="flex h-10 w-full rounded-lg border border-input bg-transparent pl-10 pr-10 text-sm text-foreground placeholder:text-muted-foreground/60 shadow-xs transition-all outline-none focus:border-ring focus:ring-[3px] focus:ring-ring/50"
                  />
                  {errors.password && (
                    <p className="mt-1 text-xs text-red-500">
                      {errors.password.message}
                    </p>
                  )}
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    aria-label={
                      showPassword ? 'Hide password' : 'Show password'
                    }
                  >
                    {showPassword ? (
                      <EyeOff className="size-4" />
                    ) : (
                      <Eye className="size-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Remember me */}
              {/* <div className="flex items-center gap-2.5">
                <Controller
                  control={control}
                  name="remember"
                  render={({ field }) => (
                    <Checkbox
                      id="remember"
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  )}
                />
                <Label
                  htmlFor="remember"
                  className="text-sm font-normal text-muted-foreground cursor-pointer"
                >
                  Remember me for 30 days
                </Label>
              </div> */}

              {/* Submit */}
              <Button
                type="submit"
                disabled={loginTokenMutation.isPending}
                className="h-10 w-full rounded-lg text-sm font-semibold"
              >
                {loginTokenMutation.isPending ? (
                  <span className="flex items-center gap-2">
                    <span className="size-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                    Signing in...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    Sign in
                    <ArrowRight className="size-4" />
                  </span>
                )}
              </Button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <Separator />
              <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-card px-3 text-xs text-muted-foreground">
                or continue with
              </span>
            </div>

            {/* Social buttons */}
            <div className="flex gap-3">
              <Button
                type="button"
                variant="outline"
                className="flex-1 h-10 rounded-lg text-sm font-medium"
              >
                <svg
                  className="size-4 mr-2"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
                    fill="#4285F4"
                  />
                  <path
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    fill="#34A853"
                  />
                  <path
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                    fill="#EA4335"
                  />
                </svg>
                Google
              </Button>
              <Button
                type="button"
                variant="outline"
                className="flex-1 h-10 rounded-lg text-sm font-medium"
              >
                <svg
                  className="size-4 mr-2"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.866-.013-1.7-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z" />
                </svg>
                GitHub
              </Button>
            </div>
          </div>

          {/* Sign up link */}
          <p className="mt-6 text-center text-sm text-muted-foreground">
            {"Don't have an account? "}
            <button
              type="button"
              className="font-semibold text-primary hover:text-primary/80 transition-colors"
            >
              Sign up
            </button>
          </p>
        </div>
      </div>
    </>
  );
};
