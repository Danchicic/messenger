import './App.css'
import {BrowserRouter} from "react-router-dom";
import AppRouter from "./components/AppRouter.jsx";
import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {setIsLogged} from "./redux/loginSlice.js";


function App() {

    return (
        <BrowserRouter>
            <AppRouter/>
        </BrowserRouter>

    )
}

export default App
