"use client";

import React from 'react';
import { Power, Radio, Zap, Activity, Cpu, Scan, ArrowUpRight, ShieldCheck } from 'lucide-react';

const UserGuide: React.FC = () => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 animate-slide-up">
            {/* Primary Hero Cell */}
            <div className="md:col-span-2 lg:col-span-2 ultra-glass p-12 flex flex-col justify-between group overflow-hidden border-indigo-500/20">
                <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-30 transition-opacity">
                    <Scan size={120} className="text-white" />
                </div>
                <div>
                    <div className="w-12 h-12 bg-indigo-500 rounded-2xl flex items-center justify-center mb-8 shadow-[0_0_20px_var(--glow-indigo)]">
                        <Cpu className="text-white w-6 h-6" />
                    </div>
                    <h2 className="text-4xl font-black text-white tracking-tighter mb-4 leading-none">
                        Neural Governance <br />
                        <span className="aurora-text">Interface</span>
                    </h2>
                    <p className="text-slate-400 font-medium text-lg leading-relaxed max-w-sm">
                        Synchronize your cognitive objectives with the Evolution AI through natural language or holographic input.
                    </p>
                </div>
                <div className="mt-12 flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.3em] text-indigo-400">
                    System Online <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-ping"></div>
                </div>
            </div>

            {/* Voice Module */}
            <div className="ultra-glass p-10 flex flex-col justify-between hover:border-emerald-500/30 transition-colors border-white/5">
                <div className="w-10 h-10 bg-emerald-500/10 text-emerald-400 rounded-xl flex items-center justify-center mb-6">
                    <Radio size={20} />
                </div>
                <div>
                    <h3 className="text-xl font-black text-white mb-2">Vocal Uplink</h3>
                    <p className="text-sm text-slate-500 leading-normal font-bold">
                        Activate your mic to issue direct strategic mandates to the core.
                    </p>
                </div>
            </div>

            {/* Speed Module */}
            <div className="ultra-glass p-10 flex flex-col justify-between hover:border-blue-500/30 transition-colors border-white/5">
                <div className="w-10 h-10 bg-blue-500/10 text-blue-400 rounded-xl flex items-center justify-center mb-6">
                    <Zap size={20} />
                </div>
                <div>
                    <h3 className="text-xl font-black text-white mb-2">Zero Latency</h3>
                    <p className="text-sm text-slate-500 leading-normal font-bold">
                        Instant task sprouting with our optimized v3.0 logic engine.
                    </p>
                </div>
            </div>

            {/* Admin Module */}
            <div className="lg:col-span-2 ultra-glass p-10 flex items-center justify-between group border-white/5">
                <div className="flex items-center gap-8">
                    <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center group-hover:bg-indigo-500/10 transition-colors">
                        <Activity className="text-slate-500 group-hover:text-indigo-400 w-8 h-8 transition-colors" />
                    </div>
                    <div>
                        <h3 className="text-2xl font-black text-white mb-1">Intelligence Statistics</h3>
                        <p className="text-sm text-slate-500 font-bold uppercase tracking-[0.1em]">Visit the systems console for user trends</p>
                    </div>
                </div>
                <ArrowUpRight className="text-slate-800 group-hover:text-white transition-colors" size={32} />
            </div>

            {/* Security Module */}
            <div className="lg:col-span-2 ultra-glass p-10 flex items-center gap-8 border-white/5">
                <div className="p-4 bg-white/5 rounded-2xl">
                    <ShieldCheck className="text-emerald-400 w-6 h-6" />
                </div>
                <div className="flex-1">
                    <h3 className="text-lg font-black text-white leading-none mb-1">Encrypted Governance</h3>
                    <p className="text-xs text-slate-600 font-bold uppercase tracking-widest leading-none">Military-grade persistence protocols enabled.</p>
                </div>
            </div>
        </div>
    );
};

export default UserGuide;
