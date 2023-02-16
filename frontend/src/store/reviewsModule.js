import axios from 'axios';
import Url from "@/store/url";

const URLS = {
    createPageReviews: id => `${Url}/page/${id}/reviews/`,
    getPersonalReviews: `${Url}/user/review/`,
    removePersonalReview: id => `${Url}/user/review/${id}/`,
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
        },

        // Получение отзывов пользователя
        async getPersonalReviews({rootState}) {
            try {
                const resp = await axios.get(
                    URLS.getPersonalReviews,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return resp.data;

            } catch(e) {
                return [
                    {

                    }
                ];
            }
        },

        // Удаление пользовательского отзыва
        async removePersonalReview({state, commit, rootState}, {id}) {
            try {
                const resp = await axios.delete(
                    URLS.removePersonalReview(id),
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return {success: resp.data.success};

            } catch(e) {
                return {success: false};
            }
        },
    },

}