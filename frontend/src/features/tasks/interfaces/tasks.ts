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
  due_date: Date | string;
  created_at: Date | string;
  updated_at: Date | string;
}
