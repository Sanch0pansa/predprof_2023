import axios from 'axios'

const URLS = {
    createPageReports: id => `http://127.0.0.1:8000/api/v1/page/${id}/reports/`,
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