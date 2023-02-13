import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    getAccountSubscriptions: `${Url}/page/account/data/`,
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