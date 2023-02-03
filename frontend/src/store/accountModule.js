import axios from 'axios'

const URLS = {
    getAccountSubscriptions: "http://127.0.0.1:8000/api/v1/page/get_account_data/",
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {

        // Получение данных по одной странице
        async getAccountSubscriptions({state, commit, rootState}) {

            let data = {};

            // Получение данных самой страницы
            try {
                const resp = await axios.get(
                    URLS.getAccountSubscriptions,
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