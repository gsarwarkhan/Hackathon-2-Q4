"use client";

// [Task]: T-017
// [From]: specs/features/chatbot.md

import { useState, useRef, useEffect } from "react";
import { api } from "@/lib/api";
import { MessageSquare, X, Send, Bot, User } from "lucide-react";

export default function ChatWidget({ onTaskAction }: { onTaskAction: () => void }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const data = await api.chat(input, messages);
            const botMessage = { role: "assistant", content: data.response };
            setMessages((prev) => [...prev, botMessage]);

            // If the message contains indicators of task mutation, refresh the dashboard
            if (data.response.toLowerCase().includes("added") ||
                data.response.toLowerCase().includes("deleted") ||
                data.response.toLowerCase().includes("marked") ||
                data.response.toLowerCase().includes("updated")) {
                onTaskAction();
            }
        } catch (err) {
            console.error(err);
            setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I had trouble processing that." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-8 right-8 z-50">
            {!isOpen ? (
                <button
                    onClick={() => setIsOpen(true)}
                    className="bg-indigo-600 text-white p-4 rounded-full shadow-lg hover:bg-indigo-700 transition-all hover:scale-110"
                >
                    <MessageSquare size={24} />
                </button>
            ) : (
                <div className="bg-white w-80 h-96 rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden">
                    <header className="bg-indigo-600 p-4 text-white flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <Bot size={20} />
                            <span className="font-semibold">Bonsai AI</span>
                        </div>
                        <button onClick={() => setIsOpen(false)}><X size={20} /></button>
                    </header>

                    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                        {messages.length === 0 && (
                            <p className="text-slate-400 text-center text-sm py-10">
                                Ask me to add tasks or list what's pending!
                            </p>
                        )}
                        {messages.map((m, i) => (
                            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${m.role === "user"
                                        ? "bg-indigo-600 text-white rounded-tr-none"
                                        : "bg-white text-slate-700 shadow-sm border border-slate-100 rounded-tl-none"
                                    }`}>
                                    {m.content}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-white p-3 rounded-2xl rounded-tl-none shadow-sm border border-slate-100 animate-pulse">
                                    <div className="flex gap-1">
                                        <div className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <div className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <div className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    <form onSubmit={handleSend} className="p-4 border-t border-slate-100 bg-white flex gap-2">
                        <input
                            type="text"
                            placeholder="Type your command..."
                            className="flex-1 text-sm bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                        >
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
}
