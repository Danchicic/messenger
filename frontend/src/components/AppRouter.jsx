import React, {useEffect, useState} from 'react';
import {Navigate, Route, Routes} from "react-router-dom";
import {userRoutes} from "../routes/index.js";
import {useDispatch, useSelector} from "react-redux";
import {setIsLogged} from "../redux/loginSlice.js";
import {amILogged} from "../api/Auth.js";


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
    const dispatch = useDispatch();
    const [isAuthChecked, setIsAuthChecked] = useState(false); // Добавляем состояние
    const isLogged = useSelector((state) => state.login);


    useEffect(() => {
        const checkAuth = async () => {
            console.log('use effect')
            const authDataFromBack = await amILogged(dispatch);
            dispatch(setIsLogged(authDataFromBack));
            setIsAuthChecked(true);
        }

        checkAuth();
    }, [dispatch]);


    console.log("after am i logged", isLogged);
    console.log(userRoutes);
    if (!isAuthChecked) {
        return <div>Loading...</div>; // Или любой другой
    }
    return (
        <>
            <Routes>
                {userRoutes.map((route, index) => (checkRouterByAuth(route, index, isLogged)))}
            </Routes>
        </>
    );
};

export default AppRouter;