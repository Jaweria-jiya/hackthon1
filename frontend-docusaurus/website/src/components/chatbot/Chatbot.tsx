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

        const currentInput = inputValue; 
        const userMessage = { id: Date.now(), text: currentInput, sender: 'user' };
        
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const backendURL = "https://jaw-eria-deploy-backend.hf.space";

            // ✅ YAHAN MISTAKE THI: Hum isse 'query_text' bhej rahe hain 
            // Taake FastAPI ka Pydantic model isse accept kar sake
            const res = await fetch(`${backendURL}/api/rag/query`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ query_text: currentInput }), 
            });

            if (!res.ok) {
                // Agar 422 error phir bhi aaye, toh hum niche 'query' try karenge
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();

            if (data && data.answer) {
                const botMessage = { id: Date.now() + 1, text: data.answer, sender: 'bot' };
                setMessages(prevMessages => [...prevMessages, botMessage]);
            } else {
                throw new Error("Invalid backend response shape");
            }

        } catch (err) {
            console.error("Failed to fetch or process chat response:", err);
            const errorMessage = { 
                id: Date.now() + 1, 
                text: 'Sorry, I encountered an error. Please try again.', 
                sender: 'bot' 
            };
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
