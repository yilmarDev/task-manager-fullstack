'use client';

import { Bell, Search, Menu, CheckSquare } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useCurrentUserQuery } from '@/features/auth/hooks/useCurrentUserQuery';

interface DashboardHeaderProps {
  onCreateTask: () => void;
  searchTerm: string;
  onSearchChange: (value: string) => void;
}

export function DashboardHeader({
  onCreateTask,
  searchTerm,
  onSearchChange,
}: DashboardHeaderProps) {
  const currentUser = useCurrentUserQuery();

  return (
    <header className="flex items-center justify-between border-b border-border bg-card px-4 lg:px-8 h-16 shrink-0">
      {/* Mobile logo */}
      <div className="flex items-center gap-3 lg:hidden">
        <Button variant="ghost" size="icon" className="text-muted-foreground">
          <Menu className="size-5" />
          <span className="sr-only">Toggle menu</span>
        </Button>
        <div className="flex items-center gap-2">
          <div className="flex size-7 items-center justify-center rounded-md bg-primary">
            <CheckSquare className="size-3.5 text-primary-foreground" />
          </div>
          <span className="font-semibold text-foreground">TaskFlow</span>
        </div>
      </div>

      {/* Search */}
      <div className="hidden md:flex items-center gap-2 max-w-sm flex-1">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <Input
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-9 bg-muted/50 border-transparent focus:bg-background focus:border-input text-foreground h-9"
          />
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-2">
        <Button
          disabled={!currentUser.data || currentUser.data.role !== 'owner'}
          onClick={onCreateTask}
          size="sm"
          className="hidden sm:flex h-9 bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Create Task
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="relative text-muted-foreground hover:text-foreground"
        >
          <Bell className="size-[18px]" />
          <span className="absolute top-1.5 right-1.5 size-2 rounded-full bg-primary" />
          <span className="sr-only">Notifications</span>
        </Button>
        <Avatar className="size-8 lg:hidden">
          <AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold">
            {currentUser.data?.name.slice(0, 2) || ''}
          </AvatarFallback>
        </Avatar>
      </div>
    </header>
  );
}
