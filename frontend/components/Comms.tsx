"use client";

import { useEffect, useRef } from "react";

export interface CommMessage {
  id: string;
  sender: string;
  text: string;
  timestamp: string;
  type: "center" | "soldier" | "system";
}

export default function TeamComms({ messages }: { messages: CommMessage[] }) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const getMessageStyle = (type: CommMessage["type"]) => {
    switch (type) {
      case "center":
        return "text-yellow-400 font-bold";
      case "soldier":
        return "text-cyan-400";
      case "system":
        return "text-slate-500 italic";
      default:
        return "text-white";
    }
  };

  return (
    <div className="flex flex-col h-full w-full bg-slate-900 border-2 border-slate-700 rounded-lg overflow-hidden font-mono text-sm shadow-lg">
      <div className="bg-slate-800 text-slate-300 p-3 border-b border-slate-700 font-bold uppercase tracking-wider flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span>SECURE NETWORK</span>
        </div>
        <span className="text-xs text-slate-500">FREQ: 144.05 MHz</span>
      </div>

      <div
        className="flex-1 overflow-y-auto p-4 space-y-4 
          /* Firefox */
          style={{ scrollbarWidth: 'thin', scrollbarColor: '#475569 transparent' }}
          /* Chrome, Edge, Safari */
          [&::-webkit-scrollbar]:w-1.5
          [&::-webkit-scrollbar-track]:bg-transparent
          [&::-webkit-scrollbar-thumb]:bg-slate-700
          [&::-webkit-scrollbar-thumb]:rounded-full
          hover:[&::-webkit-scrollbar-thumb]:bg-slate-500"
      >
        {messages.length === 0 ? (
          <div className="text-slate-600 italic">
            Listening on secure channel...
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className="flex flex-col">
              <div className="flex items-baseline space-x-2 mb-1">
                <span className="text-slate-500 text-xs">
                  [{msg.timestamp}]
                </span>
                <span
                  className={`uppercase tracking-wide ${getMessageStyle(msg.type)}`}
                >
                  {msg.sender}:
                </span>
              </div>
              <div className="text-slate-200 pl-16 leading-relaxed">
                {msg.text}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
