'use client';

import { useState } from 'react';
import { CalendarIcon, Check, ChevronsUpDown, Plus } from 'lucide-react';
import { format } from 'date-fns';
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
import { teamMembers, type Task, type User } from '@/shared/data';

interface CreateTaskModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreateTask: (task: Omit<Task, 'id' | 'createdAt'>) => void;
}

export const CreateTaskModal = ({
  open,
  onOpenChange,
  onCreateTask,
}: CreateTaskModalProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState<Date | undefined>();
  const [assignedUser, setAssignedUser] = useState<User | null>(null);
  const [userSelectOpen, setUserSelectOpen] = useState(false);
  const [calendarOpen, setCalendarOpen] = useState(false);

  const isValid = title.trim() && description.trim() && dueDate && assignedUser;

  function handleSubmit() {
    if (!isValid || !dueDate || !assignedUser) return;

    onCreateTask({
      title: title.trim(),
      description: description.trim(),
      status: 'todo',
      dueDate: format(dueDate, 'yyyy-MM-dd'),
      assignedTo: assignedUser,
    });

    setTitle('');
    setDescription('');
    setDueDate(undefined);
    setAssignedUser(null);
    onOpenChange(false);
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[520px] p-0 gap-0 overflow-hidden">
        <DialogHeader className="px-6 pt-6 pb-0">
          <DialogTitle className="text-lg font-semibold text-foreground">
            Create New Task
          </DialogTitle>
          <DialogDescription className="text-sm text-muted-foreground">
            Fill in the details below to add a new task to the board.
          </DialogDescription>
        </DialogHeader>

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
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="h-10"
            />
          </div>

          {/* Description */}
          <div className="flex flex-col gap-2">
            <Label
              htmlFor="desc"
              className="text-sm font-medium text-foreground"
            >
              Description
            </Label>
            <Textarea
              id="desc"
              placeholder="Describe the task in detail..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="resize-none"
            />
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
                  onSelect={(date: Date | undefined) => {
                    setDueDate(date);
                    setCalendarOpen(false);
                  }}
                  disabled={(date: Date) =>
                    date < new Date(new Date().setHours(0, 0, 0, 0))
                  }
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
                          {assignedUser.avatar}
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
                      {teamMembers.map((user) => (
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
                              {user.avatar}
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

        <DialogFooter className="px-6 py-4 border-t border-border bg-muted/30">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            className="mr-2"
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!isValid}
            className="bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Plus className="size-4 mr-1.5" />
            Create Task
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
