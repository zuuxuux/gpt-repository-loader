import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { callApi } from '@/lib/api'
    ;
import { User, Chat } from '@/lib/types';

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

/**
 * Creates a new chat for the given user_id
 */
async function createChat(userId: number): Promise<Chat> {
    const payload = { user_id: userId };
    return callApi('/chats', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }
  
  /**
   * getChatForUser - returns a chat for the specified user.
   *  - Currently fetches all chats, checks if there's an existing one for the user.
   *  - If none found, creates a new chat.
   *  - Returns that chat object.
   */
  export async function getChatForUser(userId: number): Promise<Chat> {
    try {
      // 1) Fetch all existing chats
      const allChats: Chat[] = await callApi('/chats');
  
      // 2) Check if there’s a chat for this user
      const existingChat = allChats.find((c) => c.user_id === userId);
  
      // 3) If found, return it; otherwise create a new chat
      if (existingChat) {
        return existingChat;
      } else {
        return createChat(userId);
      }
    } catch (error) {
      console.error('Error fetching chats:', error);
      // If fetching the chat list fails, just create a new chat
      return createChat(userId);
    }
  }