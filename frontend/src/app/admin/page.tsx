"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { Users, Shield, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function AdminPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const router = useRouter();

    useEffect(() => {
        const userStr = localStorage.getItem("user");
        if (!userStr) {
            router.push("/login");
            return;
        }
        const user = JSON.parse(userStr);
        if (user.role !== "admin") {
            setError("Access denied. Admin role required.");
            setLoading(false);
            return;
        }
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const data = await api.getAdminUsers();
            setUsers(data);
        } catch (err: any) {
            setError(err.message || "Failed to fetch users");
        } finally {
            setLoading(false);
        }
    };

    if (error) {
        return (
            <main className="min-h-screen flex items-center justify-center bg-slate-50">
                <div className="text-center p-8 bg-white rounded-2xl shadow-lg border border-rose-100">
                    <Shield className="mx-auto text-rose-500 mb-4" size={48} />
                    <h1 className="text-2xl font-bold text-slate-800 mb-2">Access Denied</h1>
                    <p className="text-slate-500 mb-6">{error}</p>
                    <Link href="/" className="text-indigo-600 font-semibold hover:underline flex items-center justify-center gap-2">
                        <ArrowLeft size={18} /> Back to Home
                    </Link>
                </div>
            </main>
        );
    }

    return (
        <main className="min-h-screen bg-slate-50 p-8">
            <div className="max-w-6xl mx-auto">
                <header className="flex justify-between items-center mb-12">
                    <div>
                        <h1 className="text-4xl font-bold text-slate-900 flex items-center gap-3">
                            <Shield className="text-indigo-600" /> Admin Dashboard
                        </h1>
                        <p className="text-slate-500">System user summary and management</p>
                    </div>
                    <Link href="/" className="bg-white border border-slate-200 px-4 py-2 rounded-xl text-slate-600 hover:bg-slate-50 transition flex items-center gap-2">
                        <ArrowLeft size={18} /> Exit Admin
                    </Link>
                </header>

                <section className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                    <div className="p-6 border-b border-slate-100 flex items-center gap-2 font-semibold text-slate-700">
                        <Users size={20} className="text-indigo-600" /> All Registered Users ({users.length})
                    </div>

                    {loading ? (
                        <div className="p-20 text-center text-slate-400">Loading user registry...</div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="bg-slate-50 text-slate-500 text-sm uppercase tracking-wider">
                                    <tr>
                                        <th className="px-6 py-4 font-semibold">User Info</th>
                                        <th className="px-6 py-4 font-semibold">Role</th>
                                        <th className="px-6 py-4 font-semibold">Tasks Created</th>
                                        <th className="px-6 py-4 font-semibold">Joined Date</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {users.map((u) => (
                                        <tr key={u.id} className="hover:bg-slate-50 transition">
                                            <td className="px-6 py-4">
                                                <div className="font-semibold text-slate-800">{u.name || "N/A"}</div>
                                                <div className="text-sm text-slate-500">{u.email}</div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`px-2 py-1 rounded-md text-xs font-bold uppercase ${u.role === 'admin' ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-600'
                                                    }`}>
                                                    {u.role}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-slate-700 font-medium">
                                                {u.task_count}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-slate-500">
                                                {new Date(u.created_at).toLocaleDateString()}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </section>
            </div>
        </main>
    );
}
