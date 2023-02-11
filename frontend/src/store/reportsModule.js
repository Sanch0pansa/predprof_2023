import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    createPageReports: id => `${Url}/page/${id}/reports/`,
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
        }
    },

}