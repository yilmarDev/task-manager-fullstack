interface TokenPayload {
  sub: string;
  exp: number;
}

const TOKEN_KEY = 'Authorization';

export const getAccessToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const setAccessToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const removeAccessToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

export const decodeAccessToken = (token: string): TokenPayload | null => {
  try {
    const payload = token.split('.')[1];
    if (!payload) return null;
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decoded) as TokenPayload;
  } catch {
    return null;
  }
};

export const getUserIdFromToken = (): string | null => {
  const token = getAccessToken();
  if (!token) return null;

  const payload = decodeAccessToken(token);
  return payload?.sub ?? null;
};

export const isTokenExpired = (): boolean => {
  const token = getAccessToken();
  if (!token) return true;

  const payload = decodeAccessToken(token);
  if (!payload) return true;

  return Date.now() >= payload.exp * 1000;
};
