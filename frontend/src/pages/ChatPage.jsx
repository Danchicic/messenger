import React, {useEffect, useRef, useState} from 'react';
import {useParams} from "react-router-dom";
import axios from "axios";

const ChatPage = () => {
    const params = useParams();
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [socket, setSocket] = useState(null);
    const messagesEndRef = useRef(null);

    const sendUserMessage = async () => {
        console.log(userInput);
        console.log('send message')
        socket.send(userInput);
    }


    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({behavior: "smooth"});
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        const localSocket = new WebSocket(`ws://localhost:8000/ws/${params.chat_name}`)

        localSocket.onopen = () => {
            localSocket.send(localStorage.getItem("token"))
        }
        localSocket.onmessage = (e) => {
            let messagesList = JSON.parse(e.data);
            console.log("ws data", messagesList);
            // console.log(typeof messagesList);
            // console.log(messagesList[0]);
            if (messagesList.length === 1) {
                setMessages((prev) => [...prev, messagesList[0]]);
            } else {
                setMessages(messagesList);
            }

        }
        setSocket(localSocket);
        return () => {
            localSocket.close(); // Важно закрывать соединение при размонтировании!
        };

    }, [params.chat_name]);
    console.log('msg2', messages);

    return (
        <div>
            <h1>
                Messages here
            </h1>
            <ul className="flex gap-3 flex-col my-4 h-[50vh] overflow-auto inset-shadow-indigo-200 p-5 px-8 border-blue-300 border-2">
                {messages.map((message, index) => (
                    <li key={index}>
                        <div className="flex gap-2">
                            <div className="bg-emerald-300 px-3 py-1 rounded-2xl">
                                {message.message}
                            </div>
                            <div className="text-gray-400">
                                user: {message.user_phone}
                            </div>
                        </div>
                    </li>
                ))}
                <div ref={messagesEndRef}/>

            </ul>

            <div className="flex gap-2 px-8">
                <input type="text"
                       onChange={(event) => setUserInput(event.target.value)}
                       className="w-60 px-1 py-2 rounded-md border-1 outline-blue-500 border-blue-500 "/>
                <button onClick={sendUserMessage}>Send</button>
            </div>
        </div>
    );
};

export default ChatPage;