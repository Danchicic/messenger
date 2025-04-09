import React from 'react';
import {Navigate, Route, Routes} from "react-router-dom";
import {userRoutes} from "../routes/index.js";

// import {AuthContext} from "../context/index.js";

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

    return (
        <>
            <Routes>
                {userRoutes.map((route, index) => (checkRouterByAuth(route, index, true)))}
            </Routes>
        </>
    );
};

export default AppRouter;