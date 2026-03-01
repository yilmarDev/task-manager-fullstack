import { CheckSquare } from 'lucide-react';
import React from 'react';

type Props = {};

export const LeftPanel = (props: Props) => {
  return (
    <div className="hidden lg:flex lg:w-[480px] xl:w-[540px] flex-col justify-between bg-sidebar text-sidebar-foreground p-10">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="flex size-9 items-center justify-center rounded-lg bg-sidebar-primary">
          <CheckSquare className="size-4.5 text-sidebar-primary-foreground" />
        </div>
        <span className="text-lg font-semibold tracking-tight">TaskFlow</span>
      </div>

      {/* Headline */}
      <div className="max-w-sm">
        <h2 className="text-3xl font-bold leading-tight tracking-tight text-balance">
          Manage tasks with clarity and focus.
        </h2>
        <p className="mt-4 text-sm leading-relaxed text-sidebar-foreground/60">
          TaskFlow helps teams organize, track, and ship work faster with a
          beautifully simple interface.
        </p>

        {/* Testimonial card */}
        <div className="mt-10 rounded-xl border border-sidebar-border bg-sidebar-accent/50 p-5">
          <p className="text-sm leading-relaxed text-sidebar-foreground/80 italic">
            &ldquo;TaskFlow transformed how our team collaborates. We shipped 2x
            faster in the first month.&rdquo;
          </p>
          <div className="mt-4 flex items-center gap-3">
            <div className="flex size-8 items-center justify-center rounded-full bg-sidebar-primary text-sidebar-primary-foreground text-xs font-semibold">
              SR
            </div>
            <div>
              <p className="text-sm font-medium text-sidebar-foreground">
                Sophia Rivera
              </p>
              <p className="text-xs text-sidebar-foreground/50">
                UX Designer, TaskFlow
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <p className="text-xs text-sidebar-foreground/40">
        &copy; {new Date().getFullYear()} TaskFlow. All rights reserved.
      </p>
    </div>
  );
};
