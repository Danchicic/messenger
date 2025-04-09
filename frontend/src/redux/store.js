import {configureStore} from "@reduxjs/toolkit"
import loginSlice from "./loginSlice.js";

const store = configureStore({
    reducer: {
        login: loginSlice
    }
})
export default store;