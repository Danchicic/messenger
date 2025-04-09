import MainPage from "../pages/MainPage.jsx";
import ChatPage from "../pages/ChatPage.jsx";
// import NotFound404 from "../pages/NotFound404.jsx";

const privateRoutes = [
    {path: "/chats/:chat_name", component: ChatPage, exact: true},

]

const publicRoutes = [
    {path: "/", component: MainPage, exact: true},
    // {path: "*", component: NotFound404, exact: false},
]
privateRoutes.forEach(
    (route) =>
        route.public = false
)
publicRoutes.forEach(route => route.public = true);
export const userRoutes = privateRoutes.concat(publicRoutes);
