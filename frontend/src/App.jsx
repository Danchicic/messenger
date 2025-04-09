import './App.css'
import {BrowserRouter} from "react-router-dom";
import AppRouter from "./components/AppRouter.jsx";
import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {setIsLogged} from "./redux/loginSlice.js";

const host = "http://127.0.0.1:8000"

function App() {
    const isLogged = useSelector((state) => state.login);
    const dispatch = useDispatch();
    console.log(isLogged);

    useEffect(() => {
        const amILogged = async () => {
            let resp = await fetch(`${host}/auth/protected`);
            if (resp.ok) {
                dispatch(setIsLogged(true));
            } else {
                dispatch(setIsLogged(false));
            }

        }
        amILogged();
    }, [])
    return (
        <BrowserRouter>
            <AppRouter/>
        </BrowserRouter>

    )
}

export default App
