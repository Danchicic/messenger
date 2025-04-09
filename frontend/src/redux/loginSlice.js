import {createSlice} from '@reduxjs/toolkit'


const loginSlice = createSlice({
    name: "login",
    initialState: false,
    reducers: {
        setIsLogged: (state, action) => {
            return action.payload;
        }
    }
})
export const {setIsLogged} = loginSlice.actions;
export default loginSlice.reducer;