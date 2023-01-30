import {createStore} from "vuex";
import authModule from "@/store/authModule";
import pagesModule from "@/store/pagesModule";
import telegramModule from "@/store/telegramModule";

export default createStore({
    state: {
        isAuth: true
    },
    modules: {
        auth: authModule,
        pages: pagesModule,
        telegram: telegramModule
    }
});