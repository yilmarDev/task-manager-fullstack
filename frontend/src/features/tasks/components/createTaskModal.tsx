'use client';

import { useState } from 'react';
import {
  CalendarIcon,
  Check,
  ChevronsUpDown,
  Loader2,
  Plus,
} from 'lucide-react';
import { format } from 'date-fns';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, Controller } from 'react-hook-form';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { useCreateTaskMutation } from '../hooks/useCreateTaskMutation';
import type { CreateTaskPayload } from '../interfaces/tasks';
import { useUsersQuery } from '@/features/users/hooks/useUsersQuery';
import type { User } from '@/features/users/interfaces/users';

const createTaskSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(100, 'Title must be 100 characters or less'),
  description: z
    .string()
    .min(1, 'Description is required')
    .max(500, 'Description must be 500 characters or less'),
  due_date: z.date({ error: 'Due date is required' }),
  assigned_to_id: z.string().min(1, 'Assignee is required'),
});

type CreateTaskFormValues = z.infer<typeof createTaskSchema>;

interface CreateTaskModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const CreateTaskModal = ({
  open,
  onOpenChange,
}: CreateTaskModalProps) => {
  const [userSelectOpen, setUserSelectOpen] = useState(false);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const usersGetter = useUsersQuery();
  const taskCreator = useCreateTaskMutation();

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, isValid },
  } = useForm<CreateTaskFormValues>({
    resolver: zodResolver(createTaskSchema),
    defaultValues: {
      title: '',
      description: '',
      assigned_to_id: '',
    },
    mode: 'onChange',
  });

  const resetForm = () => {
    reset();
    setSelectedUser(null);
  };

  const onSubmit = async (values: CreateTaskFormValues) => {
    const payload: CreateTaskPayload = {
      title: values.title.trim(),
      description: values.description.trim(),
      due_date: values.due_date,
      assigned_to_id: values.assigned_to_id,
    };

    await taskCreator.mutateAsync(payload);
    resetForm();
    onOpenChange(false);
  };

  const handleCancel = () => {
    resetForm();
    onOpenChange(false);
  };

  return (
    <Dialog
      open={open}
      onOpenChange={(value) => {
        if (!value) resetForm();
        onOpenChange(value);
      }}
    >
      <DialogContent className="sm:max-w-[520px] p-0 gap-0 overflow-hidden">
        <DialogHeader className="px-6 pt-6 pb-0">
          <DialogTitle className="text-lg font-semibold text-foreground">
            Create New Task
          </DialogTitle>
          <DialogDescription className="text-sm text-muted-foreground">
            Fill in the details below to add a new task to the board.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="px-6 py-5 flex flex-col gap-5">
            {/* Title */}
            <div className="flex flex-col gap-2">
              <Label
                htmlFor="title"
                className="text-sm font-medium text-foreground"
              >
                Title
              </Label>
              <Input
                id="title"
                placeholder="Enter task title..."
                className="h-10"
                {...register('title')}
              />
              {errors.title && (
                <p className="text-sm text-destructive">
                  {errors.title.message}
                </p>
              )}
            </div>

            {/* Description */}
            <div className="flex flex-col gap-2">
              <Label
                htmlFor="description"
                className="text-sm font-medium text-foreground"
              >
                Description
              </Label>
              <Textarea
                id="description"
                placeholder="Describe the task in detail..."
                rows={3}
                className="resize-none"
                {...register('description')}
              />
              {errors.description && (
                <p className="text-sm text-destructive">
                  {errors.description.message}
                </p>
              )}
            </div>

            {/* Due Date */}
            <div className="flex flex-col gap-2">
              <Label className="text-sm font-medium text-foreground">
                Due Date
              </Label>
              <Controller
                control={control}
                name="due_date"
                render={({ field }) => (
                  <Popover open={calendarOpen} onOpenChange={setCalendarOpen}>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        type="button"
                        className={cn(
                          'w-full justify-start text-left font-normal h-10',
                          !field.value && 'text-muted-foreground',
                        )}
                      >
                        <CalendarIcon className="size-4 mr-2 text-muted-foreground" />
                        {field.value
                          ? format(field.value, 'MMMM d, yyyy')
                          : 'Pick a date'}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={field.value}
                        onSelect={(date: Date | undefined) => {
                          field.onChange(date);
                          setCalendarOpen(false);
                        }}
                        disabled={(date: Date) =>
                          date < new Date(new Date().setHours(0, 0, 0, 0))
                        }
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                )}
              />
              {errors.due_date && (
                <p className="text-sm text-destructive">
                  {errors.due_date.message}
                </p>
              )}
            </div>

            {/* Assigned To */}
            <div className="flex flex-col gap-2">
              <Label className="text-sm font-medium text-foreground">
                Assigned To
              </Label>
              <Controller
                control={control}
                name="assigned_to_id"
                render={({ field }) => (
                  <Popover
                    open={userSelectOpen}
                    onOpenChange={setUserSelectOpen}
                  >
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        role="combobox"
                        type="button"
                        aria-expanded={userSelectOpen}
                        className={cn(
                          'w-full justify-between font-normal h-10',
                          !selectedUser && 'text-muted-foreground',
                        )}
                      >
                        {selectedUser ? (
                          <span className="flex items-center gap-2">
                            <Avatar className="size-5">
                              <AvatarFallback className="bg-primary/10 text-primary text-[8px] font-semibold">
                                {selectedUser.name.slice(0, 2)}
                              </AvatarFallback>
                            </Avatar>
                            {selectedUser.name}
                          </span>
                        ) : (
                          'Select a team member'
                        )}
                        <ChevronsUpDown className="size-4 shrink-0 opacity-50" />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent
                      className="w-[--radix-popover-trigger-width] p-0"
                      align="start"
                    >
                      <Command>
                        <CommandInput placeholder="Search team members..." />
                        <CommandList>
                          <CommandEmpty>No team member found.</CommandEmpty>
                          <CommandGroup>
                            {usersGetter.isFetching || usersGetter.isPending
                              ? 'Loading...'
                              : usersGetter.data?.map((user) => (
                                  <CommandItem
                                    key={user.id}
                                    value={user.name}
                                    onSelect={() => {
                                      field.onChange(user.id);
                                      setSelectedUser(user);
                                      setUserSelectOpen(false);
                                    }}
                                    className="flex items-center gap-2.5 py-2.5"
                                  >
                                    <Avatar className="size-7">
                                      <AvatarFallback className="bg-primary/10 text-primary text-[9px] font-semibold">
                                        {user.name.slice(0, 2)}
                                      </AvatarFallback>
                                    </Avatar>
                                    <div className="flex flex-col">
                                      <span className="text-sm font-medium text-foreground">
                                        {user.name}
                                      </span>
                                      <span className="text-xs text-muted-foreground">
                                        {user.role}
                                      </span>
                                    </div>
                                    <Check
                                      className={cn(
                                        'ml-auto size-4',
                                        field.value === user.id
                                          ? 'opacity-100'
                                          : 'opacity-0',
                                      )}
                                    />
                                  </CommandItem>
                                ))}
                          </CommandGroup>
                        </CommandList>
                      </Command>
                    </PopoverContent>
                  </Popover>
                )}
              />
              {errors.assigned_to_id && (
                <p className="text-sm text-destructive">
                  {errors.assigned_to_id.message}
                </p>
              )}
            </div>
          </div>

          <DialogFooter className="px-6 py-4 border-t border-border bg-muted/30">
            <Button
              variant="outline"
              type="button"
              onClick={handleCancel}
              className="mr-2"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={!isValid || taskCreator.isPending}
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              {taskCreator.isPending ? (
                <Loader2 className="size-4 mr-1.5 animate-spin" />
              ) : (
                <Plus className="size-4 mr-1.5" />
              )}
              {taskCreator.isPending ? 'Creating...' : 'Create Task'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
