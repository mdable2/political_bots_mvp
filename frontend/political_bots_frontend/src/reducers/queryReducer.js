import { QUERY_TEXT } from "../constants";

const initialState = {
    query: ""
};

const queryReducer = (state = initialState, action) => {
    switch(action.type) {
        case QUERY_TEXT:
            return {
                ...state,
                query: action.payload
            };
        default:
            return state;
    }
}



export default queryReducer;