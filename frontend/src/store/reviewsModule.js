import axios from 'axios';
import Url from "@/store/url";

const URLS = {
    createPageReviews: id => `${Url}/page/${id}/reviews/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {

        // Сохранение данных репорта
        async createReview({state, commit, rootState}, {id, message, mark}) {
            try {
                const resp = await axios.post(
                    URLS.createPageReviews(id),
                    {
                        message: message,
                        mark: mark
                    },
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (resp.data.success) {
                    return {success: true, detail: "Отзыв зарегистрирован"};
                }

                return {success: false, detail: "Что-то пошло не так"};

            } catch(e) {

                return {success: false, detail: "Что-то пошло не так"};
            }
        }
    },

}