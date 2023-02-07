import axios from 'axios'

const URLS = {
    createPageReports: id => `http://127.0.0.1:8000/api/v1/page/${id}/reports/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {

        // Получение данных по одной странице
        async createReport({state, commit, rootState}, {id, message, added_at}) {

            let data = {};

            // Получение данных самой страницы
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

                data = resp.data;
            } catch(e) {

            }

            return data;
        }
    },

}