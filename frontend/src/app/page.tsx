"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Plus, User as UserIcon, LayoutDashboard, LogOut, ShieldCheck } from "lucide-react";
import UserGuide from "@/components/UserGuide";
import ChatWidget from "@/components/ChatWidget";
import TaskCard from "@/components/TaskCard";
import { useRouter } from "next/navigation";
import { Task, User } from "@/types";

export default function Home() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTitle, setNewTitle] = useState("");
    const [loading, setLoading] = useState(true);
    const [userData, setUserData] = useState<User | null>(null);
    const [mounted, setMounted] = useState(false);
    const router = useRouter();

    useEffect(() => {
        console.log("HOME: Mount Protocol Initiated");
        setMounted(true);

        const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
        const userStr = typeof window !== "undefined" ? localStorage.getItem("user") : null;

        console.log("HOME: Auth Trace", { token: !!token, user: !!userStr });

        if (!token || !userStr) {
            console.log("HOME: Redirecting to login...");
            router.push("/login");
            return;
        }

        try {
            if (userStr) setUserData(JSON.parse(userStr));
            fetchTasks();
        } catch (e) {
            console.error("HOME: State Corruption", e);
            localStorage.removeItem("token");
            localStorage.removeItem("user");
            router.push("/login");
        }
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
        if (!newTitle.trim()) return;
        try {
            await api.createTask({ title: newTitle });
            setNewTitle("");
            fetchTasks();
        } catch (err) {
            console.error(err);
        }
    };

    const toggleTask = async (id: string, currentStatus: boolean) => {
        try {
            await api.updateTask(id, { is_completed: !currentStatus });
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

    if (!mounted) {
        return (
            <main className="min-h-screen flex items-center justify-center bg-[#020617]">
                <div className="text-white text-[10px] font-black uppercase tracking-[0.5em] animate-pulse">
                    Synchronizing Strategic Net...
                </div>
            </main>
        );
    }

    return (
        <main className="min-h-screen px-6 py-20 lg:px-24 xl:px-32 selection:bg-indigo-500/30">
            <div className="max-w-[1400px] mx-auto">

                {/* Cinematic Intro Section */}
                <header className="relative mb-32 flex flex-col items-center text-center animate-float-glow">
                    <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-500/20 rounded-full blur-[120px] -z-10"></div>

                    <div className="inline-flex items-center gap-3 px-6 py-2 ultra-glass rounded-full mb-8 border-indigo-500/20">
                        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse shadow-[0_0_10px_#10b981]"></div>
                        <span className="text-[10px] font-black uppercase tracking-[0.3em] text-indigo-300">Operational Excellence v3.0</span>
                    </div>

                    <h1 className="text-7xl md:text-9xl font-black tracking-tight leading-[0.85] mb-8">
                        Created by <br />
                        <span className="aurora-text">Ghulam Sarwar Khan</span>
                    </h1>

                    <div className="flex flex-wrap justify-center gap-8 text-[11px] font-black uppercase tracking-[0.4em] text-slate-500 py-4">
                        <span className="hover:text-indigo-400 cursor-default transition-colors">Evolution Todo Agent</span>
                        <span className="opacity-20">/</span>
                        <span className="hover:text-emerald-400 cursor-default transition-colors">Strategic Intelligence</span>
                        <span className="opacity-20">/</span>
                        <span className="hover:text-blue-400 cursor-default transition-colors">Automated Governance</span>
                    </div>

                    <p className="max-w-3xl text-xl text-slate-400 font-medium leading-relaxed mt-4">
                        A state-of-the-art interface for visionary leaders. Harmonize your strategic objectives through neural-link interaction and holographic task orchestration.
                    </p>
                </header>

                {/* Integrated Bento Intelligence Guide */}
                <div className="mb-32">
                    <UserGuide />
                </div>

                {/* Operations Control Center */}
                <div className="mb-32 space-y-24">
                    {/* Neural Input Section */}
                    <section className="relative max-w-5xl mx-auto">
                        <div className="absolute inset-0 bg-blue-500/5 blur-[100px] -z-10"></div>
                        <form onSubmit={handleAddTask} className="ultra-glass p-10 flex flex-col md:flex-row gap-6 border-white/5 bg-white/[0.02]">
                            <div className="flex-1 relative group">
                                <Plus className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors" size={24} />
                                <input
                                    type="text"
                                    placeholder="Input your next strategic mandate..."
                                    className="w-full cinematic-input pl-16 text-lg font-bold"
                                    value={newTitle}
                                    onChange={(e) => setNewTitle(e.target.value)}
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={!newTitle.trim()}
                                className="cinematic-button"
                            >
                                <span className="relative z-10">Integrate mandate</span>
                            </button>
                        </form>

                        <div className="flex justify-between items-center mt-8 px-4">
                            <div className="flex items-center gap-4">
                                <div className="ultra-glass px-5 py-2 rounded-full border-white/5 flex items-center gap-3">
                                    <UserIcon size={14} className="text-indigo-400" />
                                    <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">{userData?.name}</span>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                {userData?.role === 'admin' && (
                                    <button
                                        onClick={() => router.push("/admin")}
                                        className="text-[10px] font-black uppercase tracking-widest text-emerald-400 hover:text-emerald-300 transition-colors flex items-center gap-2"
                                    >
                                        <LayoutDashboard size={14} /> Systems Console
                                    </button>
                                )}
                                <button
                                    onClick={() => {
                                        api.logout();
                                        router.push("/login");
                                    }}
                                    className="text-[10px] font-black uppercase tracking-widest text-rose-500 hover:text-rose-400 transition-colors flex items-center gap-2"
                                >
                                    <LogOut size={14} /> Termination
                                </button>
                            </div>
                        </div>
                    </section>

                    {/* Holographic Objective Grid */}
                    <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                        {loading ? (
                            <div className="col-span-full py-40 flex flex-col items-center gap-8">
                                <div className="w-16 h-16 border-t-2 border-indigo-500 rounded-full animate-spin"></div>
                                <h3 className="aurora-text text-sm uppercase tracking-[0.5em]">Synchronizing Neural Net</h3>
                            </div>
                        ) : tasks.length === 0 ? (
                            <div className="col-span-full py-40 ultra-glass text-center border-dashed border-white/10 bg-transparent flex flex-col items-center gap-6">
                                <ShieldCheck size={48} className="text-slate-800" />
                                <p className="text-slate-500 text-sm font-black uppercase tracking-[0.3em] italic">No active objectives detected</p>
                            </div>
                        ) : (
                            tasks.map((task, idx) => (
                                <TaskCard
                                    key={task.id}
                                    task={task}
                                    idx={idx}
                                    onToggle={toggleTask}
                                    onDelete={deleteTask}
                                />
                            ))
                        )}
                    </section>
                </div>
            </div>

            <ChatWidget onTaskAction={fetchTasks} />
        </main>
    );
}
