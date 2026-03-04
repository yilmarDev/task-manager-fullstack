'use client';

import { useState, useEffect } from 'react';
import { CalendarIcon, Check, ChevronsUpDown, Save } from 'lucide-react';
import { format } from 'date-fns';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { AssignedTask, AssignedTo, TaskStatus } from '../interfaces/tasks';
import type { User } from '@/features/users/interfaces/users';
import { useUsersQuery } from '@/features/users/hooks/useUsersQuery';
// import type { TaskStatus } from "@/shared/data"
// import { teamMembers, type Task, type TaskStatus, type User } from "@/lib/data"

interface EditTaskSheetProps {
  task: AssignedTask | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: (updatedTask: AssignedTask) => void;
}

const statusOptions: { value: TaskStatus; label: string }[] = [
  { value: 'pending', label: 'Pending' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
];

export function EditTaskSheet({
  task,
  open,
  onOpenChange,
  onSave,
}: EditTaskSheetProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<TaskStatus>('pending');
  const [dueDate, setDueDate] = useState<Date | undefined>();
  const [assignedUser, setAssignedUser] = useState<AssignedTo | null>(null);
  const [userSelectOpen, setUserSelectOpen] = useState(false);
  const [calendarOpen, setCalendarOpen] = useState(false);

  const usersGetter = useUsersQuery();

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
      setStatus(task.status);
      setDueDate(new Date(task.due_date));
      setAssignedUser(task.assigned_to);
    }
  }, [task]);

  const isValid = title.trim() && description.trim() && dueDate && assignedUser;

  function handleSave() {
    if (!isValid || !task || !dueDate || !assignedUser) return;

    // onSave({
    //   ...task,
    //   title: title.trim(),
    //   description: description.trim(),
    //   status,
    //   dueDate: format(dueDate, 'yyyy-MM-dd'),
    //   assignedTo: assignedUser,
    // });

    onOpenChange(false);
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="sm:max-w-[480px] overflow-y-auto p-0">
        <SheetHeader className="px-6 pt-6 pb-4 border-b border-border">
          <SheetTitle className="text-lg">Edit Task</SheetTitle>
          <SheetDescription>
            Update the task details below and save your changes.
          </SheetDescription>
        </SheetHeader>

        <div className="px-6 py-6 flex flex-col gap-5">
          {/* Title */}
          <div className="flex flex-col gap-2">
            <Label
              htmlFor="edit-title"
              className="text-sm font-medium text-foreground"
            >
              Title
            </Label>
            <Input
              id="edit-title"
              placeholder="Enter task title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="h-10"
            />
          </div>

          {/* Description */}
          <div className="flex flex-col gap-2">
            <Label
              htmlFor="edit-desc"
              className="text-sm font-medium text-foreground"
            >
              Description
            </Label>
            <Textarea
              id="edit-desc"
              placeholder="Describe the task in detail..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              className="resize-none"
            />
          </div>

          {/* Status */}
          <div className="flex flex-col gap-2">
            <Label className="text-sm font-medium text-foreground">
              Status
            </Label>
            <Select
              value={status}
              onValueChange={(val) => setStatus(val as TaskStatus)}
            >
              <SelectTrigger className="h-10">
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                {statusOptions.map((opt) => (
                  <SelectItem key={opt.value} value={opt.value}>
                    {opt.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Due Date */}
          <div className="flex flex-col gap-2">
            <Label className="text-sm font-medium text-foreground">
              Due Date
            </Label>
            <Popover open={calendarOpen} onOpenChange={setCalendarOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className={cn(
                    'w-full justify-start text-left font-normal h-10',
                    !dueDate && 'text-muted-foreground',
                  )}
                >
                  <CalendarIcon className="size-4 mr-2 text-muted-foreground" />
                  {dueDate ? format(dueDate, 'MMMM d, yyyy') : 'Pick a date'}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={dueDate}
                  onSelect={(date) => {
                    setDueDate(date);
                    setCalendarOpen(false);
                  }}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </div>

          {/* Assigned To */}
          <div className="flex flex-col gap-2">
            <Label className="text-sm font-medium text-foreground">
              Assigned To
            </Label>
            <Popover open={userSelectOpen} onOpenChange={setUserSelectOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  aria-expanded={userSelectOpen}
                  className={cn(
                    'w-full justify-between font-normal h-10',
                    !assignedUser && 'text-muted-foreground',
                  )}
                >
                  {assignedUser ? (
                    <span className="flex items-center gap-2">
                      <Avatar className="size-5">
                        <AvatarFallback className="bg-primary/10 text-primary text-[8px] font-semibold">
                          {assignedUser.name.slice(0, 2).toLocaleUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      {assignedUser.name}
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
                      {usersGetter.data &&
                        usersGetter.data.map((user) => (
                          <CommandItem
                            key={user.id}
                            value={user.name}
                            onSelect={() => {
                              setAssignedUser(user);
                              setUserSelectOpen(false);
                            }}
                            className="flex items-center gap-2.5 py-2.5"
                          >
                            <Avatar className="size-7">
                              <AvatarFallback className="bg-primary/10 text-primary text-[9px] font-semibold">
                                {user.name.slice(0, 2).toLocaleUpperCase()}
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
                                assignedUser?.id === user.id
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
          </div>
        </div>

        <SheetFooter className="px-6 py-4 border-t border-border">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            disabled={!isValid}
            className="bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Save className="size-4 mr-1.5" />
            Save Changes
          </Button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
