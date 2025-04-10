import {createSlice} from '@reduxjs/toolkit'


const loginSlice = createSlice({
    name: "login",
    initialState: false,
    reducers: {
        setIsLogged: (state, action) => {
            // console.log("i get kak", action.payload)
            console.log("redux", state, action.payload);
            localStorage.setItem("token", action.payload.token)
            return action.payload.isLogged;
        }
    }
})
export const {setIsLogged} = loginSlice.actions;
export default loginSlice.reducer;