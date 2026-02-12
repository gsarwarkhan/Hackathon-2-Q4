// [Task]: T-006
// [From]: specs/architecture.md

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

const getHeaders = () => {
    const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
    return {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
    };
};

export const api = {
    async register(data: any) {
        const res = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Registration failed");
        }
        return res.json();
    },

    async login(data: any) {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Login failed");
        }
        const result = await res.json();
        if (typeof window !== "undefined") {
            localStorage.setItem("token", result.access_token);
            localStorage.setItem("user", JSON.stringify(result.user));
        }
        return result;
    },

    async getTasks(status?: string) {
        const url = new URL(`${API_BASE_URL}/tasks/`);
        if (status) url.searchParams.append("status", status);

        const res = await fetch(url.toString(), {
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error("Failed to fetch tasks");
        return res.json();
    },

    async createTask(data: any) {
        const res = await fetch(`${API_BASE_URL}/tasks/`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to create task");
        return res.json();
    },

    async updateTask(id: string, data: any) {
        const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: "PATCH",
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to update task");
        return res.json();
    },

    async deleteTask(id: string) {
        const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: "DELETE",
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error("Failed to delete task");
        return res.json();
    },

    async chat(message: string, history: any[] = []) {
        const userStr = typeof window !== "undefined" ? localStorage.getItem("user") : null;
        const user = userStr ? JSON.parse(userStr) : { id: "guest-user" };

        const res = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({
                message,
                history,
                user_id: user.id
            }),
        });
        if (!res.ok) throw new Error("Failed to get chat response");
        return res.json();
    },

    async getAdminUsers() {
        const res = await fetch(`${API_BASE_URL}/admin/users`, {
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error("Unauthorized or failed to fetch admin stats");
        return res.json();
    },

    logout() {
        if (typeof window !== "undefined") {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
        }
    }
};
