"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [mounted, setMounted] = useState(false);
    const router = useRouter();

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            await api.register({ name, email, password });
            router.push("/login?registered=true");
        } catch (err: any) {
            setError(err.message || "Failed to register");
        } finally {
            setLoading(false);
        }
    };

    if (!mounted) return (
        <main className="min-h-screen flex items-center justify-center bg-[#020617]">
            <div className="text-white text-[10px] font-black uppercase tracking-[0.5em] animate-pulse">
                Booting Register Protocol...
            </div>
        </main>
    );

    return (
        <main className="min-h-screen flex items-center justify-center p-6 bg-transparent">
            <div className="absolute inset-0 bg-blue-500/5 blur-[120px] -z-10 animate-aurora-shift"></div>

            <div className="ultra-glass p-16 w-full max-w-lg border-white/5 bg-white/[0.02] shadow-[0_40px_100px_rgba(0,0,0,0.6)] animate-slide-up">
                <header className="mb-12 text-center">
                    <div className="inline-flex items-center gap-3 px-4 py-1.5 ultra-glass rounded-full mb-6 border-emerald-500/20">
                        <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></div>
                        <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-emerald-300">New Account</span>
                    </div>
                    <h1 className="text-5xl font-black mb-4 tracking-tight text-white">
                        Create <span className="text-emerald-400">Profile</span>
                    </h1>
                    <p className="text-slate-400 font-medium text-sm">Join the ecosystem today</p>
                </header>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && (
                        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-xs font-bold flex items-center gap-2">
                            <span className="w-2 h-2 bg-rose-500 rounded-full"></span>
                            {error}
                        </div>
                    )}
                    <div className="space-y-2">
                        <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Full Name</label>
                        <input
                            type="text"
                            required
                            placeholder="John Doe"
                            className="w-full cinematic-input font-medium"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Email Address</label>
                        <input
                            type="email"
                            required
                            placeholder="you@example.com"
                            className="w-full cinematic-input font-medium"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Password</label>
                        <input
                            type="password"
                            required
                            placeholder="••••••••••••"
                            className="w-full cinematic-input font-medium"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full cinematic-button py-4 text-xs tracking-[0.2em]"
                    >
                        <span className="relative z-10">{loading ? "Creating Profile..." : "Sign Up"}</span>
                    </button>
                </form>

                <footer className="mt-10 text-center space-y-4">
                    <p className="text-xs text-slate-500 font-bold">
                        Already have an account?
                    </p>
                    <Link href="/login" className="inline-block text-emerald-400 font-bold uppercase tracking-widest text-xs hover:text-white transition-colors">
                        Sign In
                    </Link>
                </footer>
            </div>
        </main>
    );
}
