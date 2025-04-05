import React, { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

interface Message {
  text: string;
  isUser: boolean;
}

const AI = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm your AI assistant. How can I help you monitor the border area today?",
      isUser: false,
    },
    {
      text: "What is the status of border 1?",
      isUser: true,
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      const newMessage = { text: inputMessage, isUser: true };
      setMessages((prev) => [...prev, newMessage]);

      if (inputMessage.toLowerCase().includes("hello")) {
        setTimeout(() => {
          setMessages((prev) => [
            ...prev,
            {
              text: "I'm analyzing the border surveillance data. All sectors are currently secure and under active monitoring.",
              isUser: false,
            },
          ]);
        }, 500);
      }

      setInputMessage("");
    }
  };

  return (
    <Card className="w-96 p-4 bg-secondary animate-slide-in rounded-xl">
      <h3 className="text-lg font-semibold mb-4 text-rose-500">
        AI Security Assistant
      </h3>
      <div className="h-[calc(100vh-24rem)] overflow-y-auto mb-12 space-y-4 pr-2">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-3 rounded-xl animate-fade-in ${
              message.isUser
                ? "bg-slate-700 text-white ml-auto"
                : "bg-stone-700"
            } max-w-[80%] ${message.isUser ? "ml-auto" : "mr-auto"}`}
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
          className="bg-white/10 dark:bg-gray-700/50 rounded-xl"
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <Button
          onClick={handleSendMessage}
          className="transition-all duration-300 rounded-xl"
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
};

export default AI;
