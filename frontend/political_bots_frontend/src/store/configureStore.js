import { legacy_createStore as createStore, combineReducers } from 'redux';
import queryReducer from '../reducers/queryReducer';

const rootReducer = combineReducers(
    { query: queryReducer }
);

const configureStore = () => {
    return createStore(rootReducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
    );
}

export default configureStore;