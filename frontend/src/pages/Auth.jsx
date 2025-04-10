import React, {useState} from 'react';
import {getCode, sendCode} from '../api/Auth.js';
import {IMaskInput} from 'react-imask';
import {useDispatch} from "react-redux";
import {setIsLogged} from "../redux/loginSlice.js";

const Auth = () => {
    const dispatch = useDispatch();
    const [isPhoneNumberSend, setIsPhoneNumberSend] = useState(false);
    const [phoneNumber, setPhoneNumber] = useState("");
    const [phoneNumberError, setPhoneNumberError] = useState("");
    const [code, setCode] = useState("");
    const [codeError, setCodeError] = useState("");

    async function sendPhoneNumber(event) {
        event.preventDefault();
        if (phoneNumber === "") {
            setPhoneNumberError("Номер телефона не может быть пуст");
        } else {
            let phoneNumberToApi = phoneNumber.replaceAll(" ", "").replace(')', '').replace('(', '').replaceAll('-', '');
            setPhoneNumber(phoneNumberToApi);
            if (phoneNumberToApi.length !== 12) {
                setPhoneNumberError("В телефоне должно быть 11 символов");
                return;
            }
            setIsPhoneNumberSend(true);
            try {
                await getCode(phoneNumberToApi);
            } catch (error) {
                switch (error.status) {
                    case 410:
                        setPhoneNumberError("Неверный номер телефона");
                        break;
                    case 403:
                        setPhoneNumberError("Неверный номер телефона");
                        break;
                }
            }
        }
    }

    async function handleCodeChange(value) {
        setCode(value);
        if (value.length === 7) {
            const codeToApi = value.replace(' ', '');
            try {
                const token = (await sendCode(codeToApi, phoneNumber)).data['access_token'];
                console.log("resp from api", token)
                dispatch(setIsLogged({isLogged: true, token}));
            } catch (error) {
                switch (error.status) {
                    case 410:
                        setCodeError("Неверный код подтверждения");
                        break;
                    case 403:
                        setCodeError("Неверный код подтверждения");
                        break;
                }
            }
        } else {
            setCodeError("");
        }
    }


    return (
        <div className="flex items-center flex-col h-10 overflow-hidden min-h-screen">
            <img
                src="https://images.genius.com/fb1941a3fba4348dcd9b81b8ca5b5292.1000x1000x1.jpg"
                alt="site-logo-img"
                style={{
                    width: "8rem",
                }}
            />
            <h3>Вход на сайт!</h3>
            {!isPhoneNumberSend && (
                <form action="api/auth/login" className="mt-5 flex flex-col" onSubmit={sendPhoneNumber}>
                    <p className="flex flex-col">
                        <IMaskInput
                            mask="+7 (000) 000-00-00"
                            value={phoneNumber}
                            onAccept={(value) => setPhoneNumber(value)}
                            name="phone_number"
                            placeholder="Номер телефона:"
                            inputType="text"
                            className="rounded p-1 border-2 border-emerald-100 focus:outline-none"
                        />
                        {phoneNumberError && <span className="text-red-500 text-sm w-47">{phoneNumberError}</span>}
                    </p>
                    <button type="submit" className="mt-2 text-emerald-500">Получить код</button>
                </form>
            )}
            {isPhoneNumberSend && (
                <>
                    <form action="api/auth/login" className="mt-5 flex flex-col" onSubmit={sendPhoneNumber}>
                        <p>
                            <IMaskInput
                                value={phoneNumber}
                                inputType="text"
                                className="rounded p-1 border-2 border-emerald-100 focus:outline-none bg-gray-100 text-gray-400"
                                disabled
                            />
                        </p>
                    </form>
                </>
            )}
            <div
                className={`flex flex-col gap-2  transition-all transform ${isPhoneNumberSend ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"} duration-500`}>
                <IMaskInput
                    mask="000 000"
                    value={code}
                    onAccept={(value) => handleCodeChange(value)}
                    name="verification_code"
                    placeholder="Введите код:"
                    inputType="text"
                    className="rounded p-1 border-2 border-emerald-100 focus:outline-none text-center"
                />
                {codeError && <span className="text-red-500 text-sm w-47">{codeError}</span>}
            </div>
        </div>
    );
};

export default Auth;