"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
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
            await api.login({ email, password });
            router.push("/");
        } catch (err: any) {
            setError(err.message || "Failed to login");
        } finally {
            setLoading(false);
        }
    };

    if (!mounted) return (
        <main className="min-h-screen flex items-center justify-center bg-[#020617]">
            <div className="text-white text-xs font-bold uppercase tracking-[0.3em] animate-pulse">
                Loading Secure System...
            </div>
        </main>
    );

    return (
        <main className="min-h-screen flex items-center justify-center p-6 bg-transparent">
            <div className="absolute inset-0 bg-indigo-500/5 blur-[120px] -z-10 animate-aurora-shift"></div>

            <div className="ultra-glass p-20 w-full max-w-xl border-white/5 bg-black/40 shadow-[0_40px_120px_rgba(0,0,0,0.8)] animate-slide-up relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-3xl -z-10"></div>

                <header className="mb-14 text-center">
                    <div className="inline-flex items-center gap-4 px-6 py-2 ultra-glass rounded-full mb-10 border-indigo-500/20 bg-indigo-500/5">
                        <div className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></div>
                        <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-indigo-300">Secure Access</span>
                    </div>
                    <h1 className="text-5xl font-black mb-6 tracking-tight text-white">
                        Welcome <span className="text-indigo-400">Back</span>
                    </h1>
                    <p className="text-slate-400 font-medium text-sm">Enter your credentials to continue</p>
                </header>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && (
                        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-xs font-bold flex items-center gap-2">
                            <span className="w-2 h-2 bg-rose-500 rounded-full"></span>
                            {error}
                        </div>
                    )}
                    <div className="space-y-2">
                        <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Email Address</label>
                        <input
                            type="email"
                            required
                            placeholder="governor@digital-ark.com"
                            className="w-full cinematic-input font-bold"
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
                        <span className="relative z-10">{loading ? "Signing in..." : "Sign In"}</span>
                    </button>
                </form>

                <footer className="mt-10 text-center space-y-4">
                    <p className="text-xs text-slate-500 font-bold">
                        Don't have an account?
                    </p>
                    <Link href="/register" className="inline-block text-indigo-400 font-bold uppercase tracking-widest text-xs hover:text-white transition-colors">
                        Create Account
                    </Link>
                </footer>
            </div >
        </main >
    );
}
