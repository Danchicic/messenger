import axios from "axios";

const host = "http://localhost:8000"

export const amILogged = async () => {
    console.log("start check logging")
    try {
        // check that access token is normal

        let resp = await axios.get(`${host}/auth/protected`, {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            },
            withCredentials: true,
        });
        console.log("ak", resp.data);
        return {isLogged: true, token: localStorage.getItem("token")}
    } catch {
        // try to refresh
        try {
            console.log("try to refresh")
            let resp = await axios.get(`${host}/auth/refresh_token`, {
                withCredentials: true,
                "headers": {
                    'accept': 'application/json'
                }
            });
            const token = resp.data.access_token;
            return {isLogged: true, token}
        } catch {
            return {isLogged: false, token: ""}
            // we need to login

        }

    }
}


export async function sendCode(code, phoneNumber) {
    return await axios.get(
        "http://localhost:8000/auth/verify_code",
        {
            withCredentials: true,
            params: {
                code: code,
                phone_number: phoneNumber
            }
        });
}

export async function getCode(phoneNumber) {
    return await axios.post(
        "http://localhost:8000/auth/auth", new URLSearchParams({
            phone_number: phoneNumber
        }),
        {
            withCredentials: true,
            "headers": {
                'accept': 'application/json'
            }
        }
    )
}

