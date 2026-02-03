export type UserRole = 'client' | 'operator';

export interface User {
    id: number;
    role: UserRole;
    name?: string;
}
