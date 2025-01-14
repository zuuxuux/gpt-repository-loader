export interface User {
    user_id: number;
    username: string;
    email: string;
    created_at?: string;
}

export interface Chat {
    chat_id: number;
    user_id: number;
    created_at?: string;
}

export type SenderType = 'user' | 'noovox';

export interface ChatMessage {
  message_id: number;
  chat_id: number;
  user_id: number;
  sender_type: SenderType;
  message_text: string;
  sent_at?: string;
}