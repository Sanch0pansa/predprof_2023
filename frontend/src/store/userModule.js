import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    getUserData: id => `${Url}/user/${id}/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {

        // Получение данных пользователя
        async getUserData({state, commit, rootState}, {id}) {

            let data = {
                id: 10,
                username: "",
                joined: 'нет данных',
                reviews: 'нет данных',
                reports: 'нет данных',
                subscriptions: 'нет данных',
            };

            try {
                const resp = await axios.get(
                    URLS.getUserData(id),
                );

                data = resp.data;
            } catch(e) {

            }

            return data;
        }
    },

}