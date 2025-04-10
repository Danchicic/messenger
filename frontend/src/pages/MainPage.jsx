import React, {useEffect, useState} from 'react';

const host = "http://127.0.0.1:8000"

const MainPage = () => {
    const [chats, setChats] = useState([])
    const [chatName, setChatName] = useState('')

    useEffect(() => {
        const getChats = async () => {
            let chats = await fetch(`${host}/chats`);
            chats = await chats.json()
            chats = chats['chats']
            console.log("cc", chats)
            setChats(chats)
            return chats
        }
        getChats()


    }, [])
    // let chats = getChats()
    return (
        <>
            <h1>All chats</h1>
            <input type="text" onChange={(event) => setChatName(event.target.value)}/>
            <button> Create new chat</button>
            {/*<button onClick={getChats}></button>*/}
            <div>
                {Object.keys(chats).map((chat) => (
                    <li key={chats[chat]}>
                        <a href={`/chats/${chat}`}>
                            {chat}
                        </a>
                    </li>
                ))}
            </div>
        </>
    )
};

export default MainPage;