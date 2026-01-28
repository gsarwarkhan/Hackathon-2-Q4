// [Task]: T-006
// [From]: specs/architecture.md

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const api = {
    async getTasks(status?: string) {
        const url = new URL(`${API_BASE_URL}/tasks/`);
        if (status) url.searchParams.append("status", status);

        const res = await fetch(url.toString());
        if (!res.ok) throw new Error("Failed to fetch tasks");
        return res.json();
    },

    async createTask(data: any) {
        const res = await fetch(`${API_BASE_URL}/tasks/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to create task");
        return res.json();
    },

    async updateTask(id: string, data: any) {
        const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to update task");
        return res.json();
    },

    async deleteTask(id: string) {
        const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
            method: "DELETE",
        });
        if (!res.ok) throw new Error("Failed to delete task");
        return res.json();
    },
};
