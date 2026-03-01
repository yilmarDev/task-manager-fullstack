export type GetUsersResponse = User[];

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  created_at: Date;
  updated_at: Date;
}
