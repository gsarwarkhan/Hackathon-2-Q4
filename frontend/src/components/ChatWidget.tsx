"use client";

// [Task]: T-017
// [From]: specs/features/chatbot.md

import { useState, useRef, useEffect } from "react";
import { api } from "@/lib/api";
import { MessageSquare, X, Send, Bot, User, Mic, MicOff, Volume2 } from "lucide-react";

function ChatWidget({ onTaskAction }: { onTaskAction: () => void }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(true);
    const scrollRef = useRef<HTMLDivElement>(null);
    const recognitionRef = useRef<any>(null);

    useEffect(() => {
        // Initialize Speech Recognition
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = false;
            recognitionRef.current.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setInput(transcript);
                setIsListening(false);
                // Automatically send if voice is used? User experience choice.
                // For now just fill input.
            };
            recognitionRef.current.onend = () => setIsListening(false);
        }
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const speak = (text: string) => {
        if (!isSpeaking) return;
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);

        // Try to find a clear male voice
        const voices = synth.getVoices();
        const maleVoice = voices.find(v =>
            v.name.toLowerCase().includes('male') ||
            v.name.toLowerCase().includes('david') ||
            v.name.toLowerCase().includes('google uk english male')
        );

        if (maleVoice) utterance.voice = maleVoice;
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        synth.speak(utterance);
    };

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

            speak(data.response);

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

    const toggleListening = () => {
        if (isListening) {
            recognitionRef.current?.stop();
        } else {
            recognitionRef.current?.start();
            setIsListening(true);
        }
    };

    return (
        <div className="fixed bottom-12 right-12 z-[100]">
            {!isOpen ? (
                <button
                    onClick={() => setIsOpen(true)}
                    className="cinematic-button flex items-center gap-4 bg-indigo-600 shadow-[0_0_30px_var(--glow-indigo)] group"
                >
                    <div className="relative">
                        <MessageSquare size={24} className="text-white group-hover:scale-110 transition-transform" />
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-indigo-600 animate-pulse"></div>
                    </div>
                    <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white">AI Assistant</span>
                </button>
            ) : (
                <div className="ultra-glass w-[450px] h-[750px] flex flex-col overflow-hidden animate-slide-up bg-black/40 border-white/5 shadow-[0_20px_80px_rgba(0,0,0,0.8)]">
                    <header className="p-10 border-b border-white/5 flex justify-between items-center group">
                        <div className="flex items-center gap-5">
                            <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-[0_0_30px_var(--glow-indigo)] relative overflow-hidden">
                                <Bot size={32} className="text-white relative z-10" />
                                <div className="absolute inset-0 bg-white/10 animate-pulse"></div>
                            </div>
                            <div>
                                <h3 className="font-black text-white text-xl leading-none mb-2 tracking-tight">AI Todo Assistant</h3>
                                <div className="flex items-center gap-3">
                                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                                    <p className="text-[9px] uppercase tracking-[0.3em] text-slate-500 font-black">Hackathon Helper v3.0</p>
                                </div>
                            </div>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-3 hover:bg-white/5 rounded-2xl transition-colors text-slate-500 hover:text-white"
                        >
                            <X size={24} />
                        </button>
                    </header>

                    <div ref={scrollRef} className="flex-1 overflow-y-auto p-10 space-y-10 scrollbar-hide">
                        {messages.length === 0 && (
                            <div className="text-center py-32 space-y-8">
                                <div className="w-24 h-24 bg-white/5 rounded-[2rem] flex items-center justify-center mx-auto opacity-20 border border-white/10">
                                    <Bot size={48} className="text-white" />
                                </div>
                                <p className="text-slate-500 text-sm font-black uppercase tracking-[0.2em] italic max-w-[240px] mx-auto leading-relaxed">
                                    "How can I help you with your tasks today, Ghulam?"
                                </p>
                            </div>
                        )}
                        {messages.map((m, i) => (
                            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-slide-up`}>
                                <div className={`max-w-[85%] p-6 text-sm font-bold leading-relaxed shadow-2xl ${m.role === "user"
                                    ? "bg-indigo-600 text-white rounded-[2rem] rounded-tr-none shadow-indigo-500/20"
                                    : "ultra-glass text-slate-200 border-white/5 rounded-[2rem] rounded-tl-none bg-white/[0.03]"
                                    }`}>
                                    {m.content}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start animate-slide-up">
                                <div className="ultra-glass p-6 rounded-[2rem] rounded-tl-none border-white/5 flex gap-3 shadow-xl">
                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" />
                                </div>
                            </div>
                        )}
                    </div>

                    <form onSubmit={handleSend} className="p-10 border-t border-white/5 bg-black/20 space-y-6">
                        <div className="flex gap-4">
                            <input
                                type="text"
                                placeholder="Type a message..."
                                className="flex-1 cinematic-input text-sm font-black placeholder:opacity-30"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                            />
                            <div className="flex gap-3">
                                <button
                                    type="button"
                                    onClick={toggleListening}
                                    title={isListening ? "Cease processing" : "Initiate vocal capture"}
                                    className={`p-5 rounded-2xl transition-all duration-500 ${isListening ? 'bg-rose-600 text-white shadow-[0_0_30px_rgba(225,29,72,0.4)] animate-pulse' : 'bg-white/5 text-slate-500 hover:text-white hover:bg-white/10'}`}
                                >
                                    {isListening ? <MicOff size={24} /> : <Mic size={24} />}
                                </button>
                                <button
                                    type="submit"
                                    disabled={loading || !input.trim()}
                                    className="cinematic-button px-6"
                                >
                                    <Send size={24} className="text-white" />
                                </button>
                            </div>
                        </div>
                        <div className="flex justify-between items-center ultra-glass px-5 py-3 border-white/5 bg-transparent">
                            <button
                                type="button"
                                onClick={() => setIsSpeaking(!isSpeaking)}
                                className={`text-[9px] flex items-center gap-3 font-black uppercase tracking-[0.2em] transition-all duration-500 ${isSpeaking ? 'text-indigo-400' : 'text-slate-600'}`}
                            >
                                <Volume2 size={16} className={isSpeaking ? "animate-pulse" : ""} /> {isSpeaking ? "Aural Feedback Engaged" : "Aural Feedback Muted"}
                            </button>
                            <span className="text-[9px] text-slate-800 font-black uppercase tracking-[0.4em]">Engine Alpha-7</span>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
};

export default ChatWidget;
