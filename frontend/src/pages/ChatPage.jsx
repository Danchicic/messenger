import React, {useEffect, useRef, useState} from 'react';
import {useParams} from "react-router-dom";
import Input from "../components/UI/Input.jsx";
import FileIcon from "../components/ChatPage/FileIcon.jsx";

const host = "http://localhost:8000";
const ChatPage = () => {
    const params = useParams();
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [socket, setSocket] = useState(null);
    const messagesEndRef = useRef(null);

    const sendUserMessage = async () => {
        console.log(userInput);
        console.log('send message')
        socket.send(JSON.stringify({payload: {message: userInput}, type: "message"}));
        setUserInput("");
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
            let socketEvent = JSON.parse(e.data);
            console.log("ss", socketEvent);
            if (socketEvent.type === "file") {
                const {file_name, file_url} = socketEvent.payload;

                setMessages(prev => [
                    ...prev,
                    {
                        type: "file",
                        file_name,
                        file_url,
                    }
                ]);

                return;
            }
            let messagesList = socketEvent.payload.messages;
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

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file || !socket) return;

        // Чтение файла как ArrayBuffer
        const reader = new FileReader();
        reader.onload = (event) => {
            // Отправляем метаданные + бинарные данные
            const fileData = {
                name: file.name,
                data: Array.from(new Uint8Array(event.target.result)) // Конвертируем в массив чисел
            };
            socket.send(JSON.stringify({
                type: "file",
                payload: {file_data: fileData}
            }));
        };
        reader.readAsArrayBuffer(file);
    };

    return (
        <div>
            <h1>
                Messages here
            </h1>
            <ul className="flex gap-3 flex-col my-4 h-[50vh] w-[70vw] overflow-auto inset-shadow-indigo-200 p-5 px-8 border-blue-300 border-2">
                {messages.map((message, index) => (
                    <li key={index}>
                        {message.type === 'text' &&
                            <div className="flex gap-2 items-center">
                                <div className="bg-emerald-300 px-3 py-1 rounded-2xl">
                                    {message.message} - {message.type}
                                </div>
                                <div className="text-gray-400">
                                    user: {message.user_phone}
                                </div>
                            </div>
                        }
                        {message.type === 'file' &&
                            <div className="flex gap-2 items-center ">
                                <FileIcon className="text-blue-500"/>
                                <a
                                    href={`${host}${message.file_url}`}
                                    download={message.file_url}
                                    className="text-blue-600 hover:underline"
                                >
                                    ...{message.file_name.substring(5, 30)}...
                                </a>
                                <span className="text-gray-400 text-sm">(file from user:{message.user_phone}) </span>
                            </div>}

                    </li>
                ))}
                <div ref={messagesEndRef}/>

            </ul>

            <div className="flex gap-2 px-8">
                <Input type="text"
                       value={userInput}
                       onChange={(event) => setUserInput(event.target.value)}
                />
                <button onClick={sendUserMessage}>Send</button>
            </div>

            <div className="mt-5 ">
                <input
                    type="file"

                    onChange={handleFileUpload}
                    className="hidden"
                    id="fileInput"
                />
                <label
                    htmlFor="fileInput"
                    className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Download File
                </label>
            </div>
        </div>
    );
};

export default ChatPage;