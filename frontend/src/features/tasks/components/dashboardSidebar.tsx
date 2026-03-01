'use client';

import {
  LayoutDashboard,
  CheckSquare,
  Users,
  Settings,
  BarChart3,
  LogOut,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';
import { useState } from 'react';
import { useLogout } from '@/features/auth/hooks/useLogout';
import { useCurrentUserQuery } from '@/features/auth/hooks/useCurrentUserQuery';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', active: true },
  { icon: CheckSquare, label: 'Tasks', active: false },
  { icon: Users, label: 'Team', active: false },
  { icon: BarChart3, label: 'Analytics', active: false },
  { icon: Settings, label: 'Settings', active: false },
];

export function DashboardSidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const logout = useLogout();
  const currentUsr = useCurrentUserQuery();

  return (
    <aside
      className={cn(
        'hidden lg:flex flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border transition-all duration-300',
        collapsed ? 'w-[72px]' : 'w-[260px]',
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 h-16 shrink-0">
        <div className="flex size-8 items-center justify-center rounded-lg bg-sidebar-primary">
          <CheckSquare className="size-4 text-sidebar-primary-foreground" />
        </div>
        {!collapsed && (
          <span className="text-base font-semibold tracking-tight text-sidebar-foreground">
            TaskFlow
          </span>
        )}
      </div>

      <Separator className="bg-sidebar-border" />

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4">
        <ul className="flex flex-col gap-1">
          {navItems.map((item) => (
            <li key={item.label}>
              <button
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors w-full',
                  item.active
                    ? 'bg-sidebar-accent text-sidebar-primary'
                    : 'text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground',
                )}
              >
                <item.icon className="size-[18px] shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Collapse toggle */}
      <div className="px-3 pb-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setCollapsed(!collapsed)}
          className="w-full justify-center text-sidebar-foreground/50 hover:text-sidebar-foreground hover:bg-sidebar-accent"
        >
          {collapsed ? (
            <ChevronRight className="size-4" />
          ) : (
            <>
              <ChevronLeft className="size-4" />
              <span className="ml-2 text-xs">Collapse</span>
            </>
          )}
        </Button>
      </div>

      <Separator className="bg-sidebar-border" />

      {/* User Profile */}
      <div className="px-3 py-4">
        <div
          className={cn(
            'flex items-center gap-3',
            collapsed && 'justify-center',
          )}
        >
          <Avatar className="size-9 shrink-0 ring-2 ring-sidebar-primary/30">
            <AvatarFallback className="bg-sidebar-primary text-sidebar-primary-foreground text-xs font-semibold">
              {currentUsr.data?.name ? currentUsr.data.name.slice(0, 2) : ''}
            </AvatarFallback>
          </Avatar>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-sidebar-foreground truncate">
                {currentUsr.data?.name}
              </p>
              <p className="text-xs text-sidebar-foreground/50 truncate">
                {currentUsr.data?.role}
              </p>
            </div>
          )}
          {!collapsed && (
            <Button
              variant="ghost"
              size="icon"
              className="size-8 text-sidebar-foreground/40 hover:text-sidebar-foreground hover:bg-sidebar-accent shrink-0"
              onClick={() => logout()}
            >
              <LogOut className="size-4" />
              <span className="sr-only">Sign out</span>
            </Button>
          )}
        </div>
      </div>
    </aside>
  );
}
