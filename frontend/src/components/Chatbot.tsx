import React, { useState, useRef, useEffect } from 'react';
import { chatWithBot, makeReservation, cancelReservation, checkAvailability } from '../services/api';
import { MenuComponent } from './Menu';
import { ReservationForm } from './ReservationForm';

interface Message {
    sender: 'user' | 'bot';
    text: string;
    type?: 'text' | 'component';
    component?: React.ReactNode;
}

export const Chatbot: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { sender: 'bot', text: 'Hello! I can show you the menu, check availability, or help you book a table. How can I help?' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!inputValue.trim()) return;

        const userMsg = inputValue;
        setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
        setInputValue('');
        setIsTyping(true);

        try {
            const botResponse = await chatWithBot(userMsg);
            const action = botResponse.action;

            let replyMessage: Message = { sender: 'bot', text: botResponse.message };

            if (action === 'fetch_menu') {
                replyMessage.component = <MenuComponent />;
                replyMessage.type = 'component';
            }
            else if (action === 'prompt_reservation') {
                replyMessage.component = (
                    <div className="bg-white p-2 rounded relative z-0 mt-2">
                        <ReservationForm
                            onSuccess={(id) => {
                                setMessages(prev => [...prev, { sender: 'bot', text: `Reservation confirmed! Your ID is #${id}` }]);
                            }}
                            onCancel={() => {
                                setMessages(prev => [...prev, { sender: 'bot', text: "Reservation cancelled." }]);
                            }}
                        />
                    </div>
                );
                replyMessage.type = 'component';
            }
            else if (action === 'prompt_availability') {
                replyMessage.text += " (Try: 'Check availability for 2 on 2026-02-14')";
            }
            else if (action === 'prompt_cancellation') {
                // handled by text for now
            }

            setMessages(prev => [...prev, replyMessage]);

        } catch (error) {
            setMessages(prev => [...prev, { sender: 'bot', text: "Sorry, I'm having trouble connecting to the server. Is it running?" }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50 max-w-3xl mx-auto border-x border-gray-200 shadow-xl">
            <div className="bg-white p-4 border-b border-gray-200 flex items-center justify-between sticky top-0 z-10">
                <h1 className="text-xl font-bold text-gray-800">🍽️ RestoBot</h1>
                <div className="text-xs text-green-600 font-semibold flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
                    Online
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                        <div className={`p-3 rounded-2xl max-w-[85%] shadow-sm ${msg.sender === 'user'
                                ? 'bg-primary text-white rounded-tr-none'
                                : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none'
                            }`}>
                            <p>{msg.text}</p>
                        </div>
                        {msg.component && (
                            <div className="mt-2 w-full max-w-xl animate-fade-in-up">
                                {msg.component}
                            </div>
                        )}
                    </div>
                ))}
                {isTyping && (
                    <div className="self-start bg-white border border-gray-100 p-3 rounded-2xl rounded-tl-none shadow-sm flex items-center space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="p-4 bg-white border-t border-gray-200">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Type 'Show menu' or 'Book a table'..."
                        className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition shadow-inner"
                    />
                    <button
                        type="submit"
                        className="bg-primary text-white rounded-full p-2 w-10 h-10 flex items-center justify-center hover:bg-secondary transition-colors shadow-md transform active:scale-95"
                    >
                        ➤
                    </button>
                </div>
            </form>
        </div>
    );
};
