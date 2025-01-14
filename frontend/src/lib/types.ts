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