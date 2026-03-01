export interface LoginTokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginTokenPayload {
  username: string;
  password: string;
}

export interface GetUserResponse {
  id: string;
  name: string;
  email: string;
  role: string;
  created_at: Date | string;
  updated_at: Date | string;
}
