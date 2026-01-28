"use client";

// [Task]: T-007
// [From]: specs/features/task-crud.md

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Plus, Trash2, CheckCircle2, Circle } from "lucide-react";

export default function Home() {
    const [tasks, setTasks] = useState<any[]>([]);
    const [newTitle, setNewTitle] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const data = await api.getTasks();
            setTasks(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAddTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTitle.strip()) return;
        try {
            await api.createTask({ title: newTitle });
            setNewTitle("");
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    const toggleTask = async (id: string, current: boolean) => {
        try {
            await api.updateTask(id, { is_completed: !current });
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    const deleteTask = async (id: string) => {
        try {
            await api.deleteTask(id);
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <main className="min-h-screen bg-slate-50 p-8 text-slate-900">
            <div className="max-w-4xl mx-auto">
                <header className="mb-12">
                    <h1 className="text-4xl font-bold text-indigo-700 mb-2">🌳 Evolution of Todo</h1>
                    <p className="text-slate-500">Master your tasks with precision.</p>
                </header>

                <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
                    <form onSubmit={handleAddTask} className="flex gap-4">
                        <input
                            type="text"
                            placeholder="Seed a new task..."
                            className="flex-1 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            value={newTitle}
                            onChange={(e) => setNewTitle(e.target.value)}
                        />
                        <button
                            type="submit"
                            className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-semibold flex items-center gap-2 hover:bg-indigo-700 transition"
                        >
                            <Plus size={20} /> Add Task
                        </button>
                    </form>
                </section>

                <section className="space-y-4">
                    {loading ? (
                        <p className="text-center text-slate-400">Growing your forest...</p>
                    ) : tasks.length === 0 ? (
                        <div className="text-center py-20 bg-slate-100 rounded-2xl border-2 border-dashed border-slate-200">
                            <p className="text-slate-400">No tasks found. Time to seed!</p>
                        </div>
                    ) : (
                        tasks.map((task) => (
                            <div
                                key={task.id}
                                className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-4 group hover:shadow-md transition"
                            >
                                <button
                                    onClick={() => toggleTask(task.id, task.is_completed)}
                                    className="text-slate-400 hover:text-indigo-600"
                                >
                                    {task.is_completed ? (
                                        <CheckCircle2 className="text-emerald-500" />
                                    ) : (
                                        <Circle />
                                    )}
                                </button>
                                <div className="flex-1">
                                    <h3 className={`font-semibold ${task.is_completed ? "line-through text-slate-400" : "text-slate-700"}`}>
                                        {task.title}
                                    </h3>
                                    {task.priority && (
                                        <span className="text-xs font-bold text-amber-500 uppercase tracking-wider">
                                            Priority: {task.priority === 3 ? "High" : task.priority === 2 ? "Medium" : "Low"}
                                        </span>
                                    )}
                                </div>
                                <button
                                    onClick={() => deleteTask(task.id)}
                                    className="opacity-0 group-hover:opacity-100 text-rose-400 hover:text-rose-600 transition"
                                >
                                    <Trash2 size={20} />
                                </button>
                            </div>
                        ))
                    )}
                </section>
            </div>
        </main>
    );
}
