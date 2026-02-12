export interface User {
    id: string;
    email: string;
    name: string;
    role: "user" | "admin";
}

export interface Task {
    id: string;
    title: string;
    description?: string;
    is_completed: boolean;
    priority: number; // 1: Low, 2: Medium, 3: High
    tags?: string;
    created_at: string;
    updated_at: string;
    user_id: string;
}
