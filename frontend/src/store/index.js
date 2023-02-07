import {createStore} from "vuex";
import authModule from "@/store/authModule";
import pagesModule from "@/store/pagesModule";
import telegramModule from "@/store/telegramModule";
import accountModule from "@/store/accountModule";
import reportsModule from "@/store/reportsModule";
import reviewsModule from "@/store/reviewsModule";
import moderationModule from "@/store/moderationModule";

export default createStore({
    state: {
        isAuth: true
    },
    modules: {
        auth: authModule,
        pages: pagesModule,
        telegram: telegramModule,
        account: accountModule,
        reports: reportsModule,
        reviews: reviewsModule,
        moderation: moderationModule
    }
});