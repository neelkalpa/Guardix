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
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    try {
      // Add user message
      const userMessage = { text: inputMessage, isUser: true };
      setMessages(prev => [...prev, userMessage]);
      setInputMessage("");
      setIsLoading(true);

      // API call with UTF-8 safe configuration
      const response = await fetch("http://localhost:6000/describe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Accept": "application/json; charset=utf-8"
        },
        body: JSON.stringify({
          prompt: inputMessage.normalize("NFC") // Unicode normalization
        }),
      });

      // Enhanced error handling
      if (!response.ok) {
        const errorText = await response.text();
        try {
          const errorData = JSON.parse(errorText);
          throw new Error(errorData.error || `HTTP ${response.status} Error`);
        } catch {
          throw new Error(`Server response: ${errorText.slice(0, 100)}`);
        }
      }

      // Process response with UTF-8 safety
      const data = await response.json();
      const sanitizedResponse = data.response
        .normalize("NFC")
        .replace(/[\u0000-\u001F\u007F-\u009F]/g, ""); // Remove control chars

      setMessages(prev => [
        ...prev,
        { text: sanitizedResponse, isUser: false },
      ]);
    } catch (error) {
      console.error("API Error:", error);
      setMessages(prev => [
        ...prev,
        { 
          text: error instanceof Error 
               ? `System Alert: ${error.message}`
               : "Security systems unreachable. Try again.",
          isUser: false 
        },
      ]);
    } finally {
      setIsLoading(false);
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
                : "bg-stone-700 text-gray-100"
            } max-w-[80%] ${message.isUser ? "ml-auto" : "mr-auto"}`}
          >
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className="p-3 rounded-xl bg-stone-700 text-gray-300 mr-auto max-w-[80%] animate-pulse">
            Analyzing surveillance feeds...
          </div>
        )}
      </div>
      <div className="flex gap-2">
        <Input
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value.normalize("NFC"))}
          placeholder="Type security query..."
          className="bg-white/10 dark:bg-gray-700/50 rounded-xl focus-visible:ring-rose-500"
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          disabled={isLoading}
        />
        <Button
          onClick={handleSendMessage}
          className="transition-all duration-300 rounded-xl bg-rose-600 hover:bg-rose-700"
          disabled={isLoading}
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
};

export default AI;
