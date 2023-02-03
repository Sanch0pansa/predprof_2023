import {createStore} from "vuex";
import authModule from "@/store/authModule";
import pagesModule from "@/store/pagesModule";
import telegramModule from "@/store/telegramModule";
import accountModule from "@/store/accountModule";

export default createStore({
    state: {
        isAuth: true
    },
    modules: {
        auth: authModule,
        pages: pagesModule,
        telegram: telegramModule,
        account: accountModule,
    }
});