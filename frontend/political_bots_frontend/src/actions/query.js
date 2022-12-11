import { QUERY_TEXT } from "../constants";

export function changeQueryText(query) {
    return {
        type: QUERY_TEXT,
        payload: query
    }
}