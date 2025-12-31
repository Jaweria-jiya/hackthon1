import React, { useState, useEffect, useRef } from 'react';
import styles from './Chatbot.module.css';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { id: 1, text: 'Hello! How can I help you with the book?', sender: 'bot' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const chatBodyRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Scroll to the bottom of the chat body when messages change
        if (chatBodyRef.current) {
            chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
        }
    }, [messages]);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (inputValue.trim() === '' || isLoading) return;

        const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // ✅ Updated fetch for production using environment variable
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/rag/query`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query_text: inputValue,
                }),
            });

            if (!res.ok) {
                // Handle HTTP errors like 500, 404 etc.
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();

            // Optional: log answer for debugging
            console.log(data.answer);

            // Validate the response shape
            if (!data || typeof data.answer !== 'string') {
                throw new Error("Invalid backend response shape");
            }
            
            // Use the correct 'data.answer' to create the bot message
            const botMessage = { id: Date.now() + 1, text: data.answer, sender: 'bot' };
            setMessages(prevMessages => [...prevMessages, botMessage]);

        } catch (err) {
            console.error("Failed to fetch or process chat response:", err);
            const errorMessage = { id: Date.now() + 1, text: 'Sorry, I encountered an error. Please try again.', sender: 'bot' };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <div className={styles.floatingButton} onClick={toggleChat}>
                Chat
            </div>

            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <h3>AI Assistant</h3>
                        <button onClick={toggleChat} className={styles.closeButton}>×</button>
                    </div>
                    <div className={styles.chatBody} ref={chatBodyRef}>
                        {messages.map(message => (
                            <div key={message.id} className={`${styles.message} ${styles[message.sender]}`}>
                                {message.text.split('\n').map((line, index) => (
                                    <span key={index}>{line}<br/></span>
                                ))}
                            </div>
                        ))}
                        {isLoading && <div className={`${styles.message} ${styles.bot}`}>Thinking...</div>}
                    </div>
                    <form onSubmit={handleSendMessage} className={styles.chatFooter}>
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Ask a question..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading}>Send</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
