import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    createPageReports: id => `${Url}/page/${id}/reports/`,
    getPersonalReports: `${Url}/user/report/`,
    removePersonalReport: id => `${Url}/user/report/${id}/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {

        // Сохранение данных репорта
        async createReport({state, commit, rootState}, {id, message, added_at}) {
            try {
                const resp = await axios.post(
                    URLS.createPageReports(id),
                    {
                        message: message,
                        added_at: added_at
                    },
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (resp.data.success) {
                    return {success: true, detail: "Сообщение зарегистрировано"};
                }

                return {success: false, detail: "Что-то пошло не так"};

            } catch(e) {

                return {success: false, detail: "Что-то пошло не так"};
            }
        },


        // Получение репортов пользователя
        async getPersonalReports({rootState}) {
            try {
                const resp = await axios.get(
                    URLS.getPersonalReports,
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
                        id: 1,
                        page: {
                            id: 2,
                            name: "МИРЭА"
                        },
                        message: "Test",
                        status: "accepted"
                    }
                ];
            }
        },

        // Удаление пользовательского отзыва
        async removePersonalReport({state, commit, rootState}, {id}) {
            try {
                const resp = await axios.delete(
                    URLS.removePersonalReport(id),
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