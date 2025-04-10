import axios from "axios";

const host = "http://localhost:8000"

export const createNewChat = async (newChatName) => {
    await axios.post(`${host}/create_chat`,
        '',
        {
            params: {
                "chat_name": newChatName,
            },
            headers: {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded'
            }
        })
}