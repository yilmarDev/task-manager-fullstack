'use client';

import { AlertTriangle } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import type { AssignedTask } from '../interfaces/tasks';

interface DeleteTaskDialogProps {
  task: AssignedTask | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: (taskId: string) => void;
}

export const DeleteTaskDialog = ({
  task,
  open,
  onOpenChange,
  onConfirm,
}: DeleteTaskDialogProps) => {
  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent className="sm:max-w-[440px]">
        <AlertDialogHeader>
          <div className="flex items-center gap-3 mb-1">
            <div className="flex items-center justify-center size-10 rounded-xl bg-destructive/10">
              <AlertTriangle className="size-5 text-destructive" />
            </div>
            <AlertDialogTitle className="text-lg font-semibold text-foreground">
              Confirm Deletion
            </AlertDialogTitle>
          </div>
          <AlertDialogDescription className="text-sm text-muted-foreground leading-relaxed">
            Are you sure you want to delete{' '}
            <span className="font-medium text-foreground">{task?.title}</span>?
            This action cannot be undone and the task will be permanently
            removed from the board.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter className="mt-2">
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={() => task && onConfirm(task.id)}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            Delete Task
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};
