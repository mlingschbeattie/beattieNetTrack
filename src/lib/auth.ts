export type AuthUser = {
  username: string;
  name: string;
  email: string;
  groups: string[];
  isTeacher: boolean;
  isAdmin: boolean;
};

/**
 * Extracts authenticated user identity from HTTP headers injected by Caddy + Authelia
 * (e.g. Remote-User, Remote-Name, Remote-Email, Remote-Groups).
 */
export function getAuthUser(headers: Headers): AuthUser | null {
  const username = headers.get('remote-user') || headers.get('x-forwarded-user');
  if (!username) return null;

  const rawName = headers.get('remote-name') || headers.get('x-forwarded-name');
  // Fallback: capitalize username if no display name header exists (e.g. 'jsmith' -> 'Jsmith')
  const name = rawName || username.charAt(0).toUpperCase() + username.slice(1);
  const email = headers.get('remote-email') || headers.get('x-forwarded-email') || `${username}@beattietech.local`;
  const groupsHeader = headers.get('remote-groups') || headers.get('x-forwarded-groups') || '';
  const groups = groupsHeader
    .split(',')
    .map((g) => g.trim().toLowerCase())
    .filter(Boolean);
  const isTeacher = groups.includes('teachers') || groups.includes('admins');
  const isAdmin = groups.includes('admins');

  return {
    username,
    name,
    email,
    groups,
    isTeacher,
    isAdmin,
  };
}
