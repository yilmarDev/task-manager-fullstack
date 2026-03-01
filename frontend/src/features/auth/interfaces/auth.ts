export interface LoginTokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginTokenPayload {
  username: string;
  password: string;
}
