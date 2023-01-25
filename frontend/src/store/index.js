import {createStore} from "vuex";
import authModule from "@/store/authModule";
import pagesModule from "@/store/pagesModule";

export default createStore({
    state: {
        isAuth: true
    },
    modules: {
        auth: authModule,
        pages: pagesModule,
    }
});