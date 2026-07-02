import { useEffect, useRef, useState } from "react";

const SUGGESTIONS = [
  "My monitor won't turn on",
  "I can't connect to the office Wi-Fi",
  "Outlook keeps asking for my password",
];

const WELCOME = {
  role: "assistant",
  text:
    "Hi! I'm Zack's IT Help Desk assistant. Describe the problem you're " +
    "having and I'll walk you through a fix. The first answer can take a " +
    "few extra seconds while I warm up.",
};

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 150, 300].map((delay) => (
        <span
          key={delay}
          className="h-2 w-2 rounded-full bg-slate-400 animate-bounce"
          style={{ animationDelay: `${delay}ms` }}
        />
      ))}
    </div>
  );
}

function Bubble({ role, text, isError }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap shadow-sm ${
          isUser
            ? "bg-blue-600 text-white rounded-br-md"
            : isError
              ? "bg-red-50 text-red-700 border border-red-200 rounded-bl-md"
              : "bg-white text-slate-800 border border-slate-200 rounded-bl-md"
        }`}
      >
        {text}
      </div>
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(text) {
    const query = text.trim();
    if (!query || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", text: data.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          isError: true,
          text: "Sorry — something went wrong reaching the help desk. Please try again in a moment.",
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  const showSuggestions = messages.length === 1 && !loading;

  return (
    <div className="min-h-dvh bg-slate-100 flex flex-col">
      <header className="bg-white border-b border-slate-200 px-4 py-3 shadow-sm">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <div className="h-9 w-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold">
            IT
          </div>
          <div>
            <h1 className="text-sm font-semibold text-slate-800">
              Zack's IT Help Desk
            </h1>
            <p className="text-xs text-slate-500">
              Troubleshooting assistant &middot; powered by RAG
            </p>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-2xl mx-auto flex flex-col gap-3">
          {messages.map((m, i) => (
            <Bubble key={i} role={m.role} text={m.text} isError={m.isError} />
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-md shadow-sm">
                <TypingIndicator />
              </div>
            </div>
          )}

          {showSuggestions && (
            <div className="flex flex-wrap gap-2 mt-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="text-xs px-3 py-2 rounded-full border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 hover:border-slate-400 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </main>

      <footer className="bg-white border-t border-slate-200 px-4 py-3">
        <form
          className="max-w-2xl mx-auto flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
        >
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            placeholder={loading ? "Thinking..." : "Describe your issue..."}
            className="flex-1 rounded-full border border-slate-300 px-4 py-2.5 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-50 disabled:text-slate-400"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="rounded-full bg-blue-600 text-white px-5 py-2.5 text-sm font-medium hover:bg-blue-700 disabled:bg-slate-300 transition-colors"
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}
