import React, {useEffect} from 'react';
import {Navigate, Route, Routes} from "react-router-dom";
import {userRoutes} from "../routes/index.js";
import {useDispatch, useSelector} from "react-redux";
import {setIsLogged} from "../redux/loginSlice.js";

const host = "http://127.0.0.1:8000"

function checkRouterByAuth(route, index, isAuth) {
    if (route.path.includes("auth") && isAuth) {
        // if logged user want to auth twice
        return <Route key={index} path={route.path} element={<Navigate to="/"/>} exact={route.exact}/>;
    } else if (route.public || (!route.public && isAuth)) {
        //routes for logged user, public + private, exclude auth routers
        return <Route key={index} path={route.path} element={<route.component/>} exact={route.exact}/>;
    } else if (!route.public && !isAuth) {
        //routes for unlogged user
        return <Route key={index} path={route.path} element={<Navigate to="/auth/login"/>} exact={route.exact}/>;
    }
}

const AppRouter = () => {
    const isLogged = useSelector((state) => state.login);
    const dispatch = useDispatch();
    console.log(isLogged);

    useEffect(() => {
        const amILogged = async () => {
            let resp = await fetch(`${host}/auth/protected`, {
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("access_token")
                }
            });

            if (resp.ok) {
                // check that access token is normal
                dispatch(setIsLogged({isLogged: true, token: await resp.json()['access_token']}));
            } else {
                // try to refresh
                let resp = await fetch(`${host}/auth/refresh_token`);
                if (resp.ok) {
                    dispatch(setIsLogged({isLogged: true, token: await resp.json()['access_token']}));
                } else {
                    // we need to login
                    dispatch(setIsLogged({isLogged: false, token: ""}));
                }
            }

        }
        amILogged();
    }, [])
    return (
        <>
            <Routes>
                {userRoutes.map((route, index) => (checkRouterByAuth(route, index, isLogged)))}
            </Routes>
        </>
    );
};

export default AppRouter;