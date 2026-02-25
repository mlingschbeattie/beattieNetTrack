import type { FsDir, FsNode } from './types';

const isDir = (node: FsNode | undefined): node is FsDir => Boolean(node && node.type === 'dir');

export const cloneFsNode = (node: FsNode): FsNode => {
  if (node.type === 'file') {
    return { type: 'file', content: node.content };
  }

  const children: Record<string, FsNode> = {};
  for (const [name, child] of Object.entries(node.children)) {
    children[name] = cloneFsNode(child);
  }
  return { type: 'dir', children };
};

export const tokenize = (input: string): string[] => input.trim().split(/\s+/).filter(Boolean);

export const normalizeAbsolutePath = (path: string): string => {
  const parts = path.split('/');
  const stack: string[] = [];

  for (const rawPart of parts) {
    const part = rawPart.trim();
    if (part.length === 0 || part === '.') continue;
    if (part === '..') {
      if (stack.length > 0) stack.pop();
      continue;
    }
    stack.push(part);
  }

  return `/${stack.join('/')}`.replace(/\/+/g, '/');
};

export const resolvePath = (cwd: string, path: string): string => {
  const base = path.startsWith('/') ? path : `${cwd}/${path}`;
  return normalizeAbsolutePath(base);
};

export const pathSegments = (path: string): string[] => normalizeAbsolutePath(path).split('/').filter(Boolean);

export const basename = (path: string): string => {
  const segments = pathSegments(path);
  return segments.length === 0 ? '/' : segments[segments.length - 1] ?? '/';
};

export const getNodeAtPath = (root: FsNode, absolutePath: string): FsNode | undefined => {
  const path = normalizeAbsolutePath(absolutePath);
  if (path === '/') return root;
  if (root.type !== 'dir') return undefined;

  let current: FsNode | undefined = root;
  for (const segment of pathSegments(path)) {
    if (!current || current.type !== 'dir') return undefined;
    current = current.children[segment];
  }
  return current;
};

export const listDirEntries = (node: FsNode): string[] => {
  if (node.type !== 'dir') return [];
  return Object.keys(node.children).sort((a, b) => a.localeCompare(b));
};

const getParentDir = (root: FsNode, absolutePath: string): { parent: FsDir; name: string } | undefined => {
  const normalized = normalizeAbsolutePath(absolutePath);
  if (normalized === '/') return undefined;

  const segments = pathSegments(normalized);
  const name = segments.pop();
  if (!name) return undefined;

  const parentPath = segments.length === 0 ? '/' : `/${segments.join('/')}`;
  const parentNode = getNodeAtPath(root, parentPath);
  if (!parentNode || parentNode.type !== 'dir') return undefined;

  return { parent: parentNode, name };
};

export const mkdirAtPath = (root: FsNode, absolutePath: string): { fs: FsNode; created: boolean; exists: boolean } => {
  const cloned = cloneFsNode(root);
  const parentInfo = getParentDir(cloned, absolutePath);
  if (!parentInfo) {
    return { fs: cloned, created: false, exists: false };
  }

  if (parentInfo.parent.children[parentInfo.name]) {
    return { fs: cloned, created: false, exists: true };
  }

  parentInfo.parent.children[parentInfo.name] = { type: 'dir', children: {} };
  return { fs: cloned, created: true, exists: false };
};

export const touchAtPath = (root: FsNode, absolutePath: string): { fs: FsNode; ok: boolean } => {
  const cloned = cloneFsNode(root);
  const parentInfo = getParentDir(cloned, absolutePath);
  if (!parentInfo) {
    return { fs: cloned, ok: false };
  }

  if (!parentInfo.parent.children[parentInfo.name]) {
    parentInfo.parent.children[parentInfo.name] = { type: 'file', content: '' };
  }

  return { fs: cloned, ok: true };
};

export const asDir = (node: FsNode | undefined): FsDir | undefined => (isDir(node) ? node : undefined);