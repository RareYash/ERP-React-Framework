import { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "../services/api";
import "./ChatWidget.css";

const WELCOME_MSG = {
    role: "model",
    text: "👋 Hi! I'm your AI teaching assistant. Ask me about your students, their reviews, grades, or sentiments. I can also add reviews for you!\n\nTry: *\"How is Aarav doing?\"* or *\"Who needs attention?\"*",
};

export default function ChatWidget() {
    const [open, setOpen] = useState(false);
    const [messages, setMessages] = useState([WELCOME_MSG]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    useEffect(() => {
        if (open) inputRef.current?.focus();
    }, [open]);

    async function handleSend(e) {
        e?.preventDefault();
        const text = input.trim();
        if (!text || loading) return;

        const userMsg = { role: "user", text };
        const updatedMessages = [...messages, userMsg];
        setMessages(updatedMessages);
        setInput("");
        setLoading(true);

        try {
            // Build history (skip the welcome message)
            const history = updatedMessages
                .filter((_, i) => i > 0) // skip welcome
                .slice(-20) // keep last 20 messages for context
                .map((m) => ({ role: m.role, text: m.text }));

            const data = await sendChatMessage(text, history);
            const botMsg = { role: "model", text: data.reply };
            if (data.action_taken) {
                botMsg.action = data.action_taken;
            }
            setMessages((prev) => [...prev, botMsg]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                { role: "model", text: `❌ Error: ${err.message}. Make sure the backend is running and GEMINI_API_KEY is set in .env` },
            ]);
        } finally {
            setLoading(false);
        }
    }

    function renderMarkdown(text) {
        // Simple markdown: **bold**, *italic*, \n → <br>
        let html = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.+?)\*/g, "<em>$1</em>")
            .replace(/`(.+?)`/g, '<code>$1</code>')
            .replace(/\n/g, "<br/>");
        return html;
    }

    return (
        <>
            {/* Floating Action Button */}
            <button
                className={`chat-fab ${open ? "chat-fab-hidden" : ""}`}
                onClick={() => setOpen(true)}
                aria-label="Open chat assistant"
            >
                <span className="chat-fab-icon">🤖</span>
                <span className="chat-fab-pulse" />
            </button>

            {/* Chat Window */}
            {open && (
                <div className="chat-window animate-slide-up">
                    {/* Header */}
                    <div className="chat-header">
                        <div className="chat-header-info">
                            <span className="chat-header-avatar">🤖</span>
                            <div>
                                <h4>AI Teaching Assistant</h4>
                                <span className="chat-header-status">Powered by Gemini 2.5 Pro</span>
                            </div>
                        </div>
                        <button className="chat-close" onClick={() => setOpen(false)}>✕</button>
                    </div>

                    {/* Messages */}
                    <div className="chat-messages">
                        {messages.map((msg, i) => (
                            <div key={i} className={`chat-bubble ${msg.role === "user" ? "chat-user" : "chat-bot"}`}>
                                {msg.role !== "user" && <span className="chat-bubble-avatar">🤖</span>}
                                <div className="chat-bubble-content">
                                    <div
                                        className="chat-bubble-text"
                                        dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.text) }}
                                    />
                                    {msg.action && (
                                        <div className="chat-action-badge">✅ {msg.action}</div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="chat-bubble chat-bot">
                                <span className="chat-bubble-avatar">🤖</span>
                                <div className="chat-bubble-content">
                                    <div className="chat-typing">
                                        <span></span><span></span><span></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={bottomRef} />
                    </div>

                    {/* Input */}
                    <form className="chat-input-area" onSubmit={handleSend}>
                        <input
                            ref={inputRef}
                            type="text"
                            className="chat-input"
                            placeholder="Ask about your students…"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={loading}
                        />
                        <button type="submit" className="chat-send" disabled={loading || !input.trim()}>
                            ➤
                        </button>
                    </form>
                </div>
            )}
        </>
    );
}
