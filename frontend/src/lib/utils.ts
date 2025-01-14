import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { callApi } from '@/lib/api'
    ;
import { User } from '@/lib/types';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export async function createUser(username: string, email: string): Promise<User> {
    const payload = { username, email };
    return callApi('/users', {
        method: 'POST',
        body: JSON.stringify(payload),
    });
}

export async function getUser(username: string, email: string): Promise<User> {
    try {
        // 1) Fetch all existing users
        const allUsers: User[] = await callApi('/users');

        // 2) Check if we have a match by email
        const existing = allUsers.find((u) => u.email === email);

        // 3) If found, return it; otherwise create a new user
        if (existing) {
            return existing;
        } else {
            return createUser(username, email);
        }
    } catch (error) {
        // If fetching the user list fails, just try creating a new user
        console.error('Error fetching user list:', error);
        return createUser(username, email);
    }
}