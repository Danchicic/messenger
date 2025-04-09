import React, {useEffect, useState} from 'react';

const host = "http://127.0.0.1:8000"

const MainPage = () => {
    const [chats, setChats] = useState([])

    useEffect(() => {
        const getChats = async () => {
            let chats = await fetch(`${host}/chats`);
            chats = await chats.json()
            chats = chats['chats']
            console.log(chats)
            setChats(chats)
            return chats
        }
        getChats()


    }, [])
    // let chats = getChats()
    return (
        <>
            <h1>All chats</h1>
            {/*<button onClick={getChats}></button>*/}
            <div>
                {chats.map((chat) => (
                    <li key={chat.chat_name}>
                        <a href={`/chats/${chat.chat_name}`}>
                            {chat.chat_name}
                        </a>

                    </li>
                ))}
            </div>
        </>
    )
};

export default MainPage;