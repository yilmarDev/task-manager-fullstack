export interface CreateTaskPayload {
  title: string;
  description: string;
  due_date: Date;
  assigned_to_id: string;
}

export interface CreateTaskResponse {
  id: string;
  title: string;
  description: string;
  status: string;
  owner_id: string;
  assigned_to_id: string;
  due_date: string;
  created_at: string;
  updated_at: string;
}

export type GetAssignedTasksResponse = AssignedTask[];

export interface AssignedTask {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  owner: AssignedTo;
  assigned_to: AssignedTo;
  due_date: string;
  created_at: string;
  updated_at: string;
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed';
export interface AssignedTo {
  id: string;
  name: string;
  email: string;
}
