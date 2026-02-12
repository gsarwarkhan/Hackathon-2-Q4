"use client";

import { CheckCircle2, Circle, Trash2 } from "lucide-react";
import { Task } from "@/types";

interface TaskCardProps {
    task: Task;
    idx: number;
    onToggle: (id: string, currentStatus: boolean) => void;
    onDelete: (id: string) => void;
}

export default function TaskCard({ task, idx, onToggle, onDelete }: TaskCardProps) {
    return (
        <div
            style={{ animationDelay: `${idx * 100}ms` }}
            className={`hologram-card group p-10 flex flex-col justify-between h-[320px] transition-all duration-700 hover:scale-[1.02] animate-slide-up ${task.is_completed ? "opacity-30 border-white/0" : "border-white/10"}`}
        >
            <div className="flex justify-between items-start">
                <button
                    onClick={() => onToggle(task.id, task.is_completed)}
                    className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-500 ${task.is_completed ? "bg-emerald-500 text-white shadow-[0_0_30px_#10b981]" : "bg-white/5 text-slate-500 hover:text-white hover:bg-white/10 border border-white/5"}`}
                >
                    {task.is_completed ? <CheckCircle2 size={32} /> : <Circle size={32} />}
                </button>
                <button
                    onClick={() => onDelete(task.id)}
                    className="opacity-0 group-hover:opacity-100 w-10 h-10 rounded-xl flex items-center justify-center text-slate-600 hover:text-rose-500 hover:bg-rose-500/10 transition-all"
                >
                    <Trash2 size={24} />
                </button>
            </div>

            <div className="space-y-6">
                <h3 className={`text-2xl font-black leading-tight tracking-tight ${task.is_completed ? "line-through text-slate-600" : "text-white"}`}>
                    {task.title}
                </h3>
                <div className="flex items-center justify-between pt-6 border-t border-white/5">
                    <div className="flex items-center gap-3">
                        <div className={`w-2 h-2 rounded-full animate-pulse ${task.priority === 3 ? "bg-rose-500" : task.priority === 2 ? "bg-amber-500" : "bg-emerald-500"}`}></div>
                        <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">
                            {task.priority === 3 ? "Critical" : task.priority === 2 ? "Strategic" : "Standard"}
                        </span>
                    </div>
                    <span className="text-[9px] text-slate-700 font-bold font-mono">NODE_{task.id.slice(0, 4)}</span>
                </div>
            </div>
        </div>
    );
}
