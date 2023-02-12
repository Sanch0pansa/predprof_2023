import axios from 'axios'
import Url from "@/store/url";


const URLS = {
    getEvents: `${Url}/account/get_events/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {
        // Получение списка событий
        async getEvents({rootState}) {

            try {
                const resp = await axios.get(
                    URLS.getEvents,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return resp.data;

            } catch(e) {
                return {
                    working: 0,
                    not_working: 0,
                    lazy_loading: 0,
                    events: [
                        // {
                        //     "type": "failure",
                        //     "page": {
                        //         "id": 1,
                        //         "name": "МИРЭА"
                        //     },
                        //     "detail": {
                        //         "error_description": "Ошибка сервера",
                        //         "reasons": [
                        //             "Перезагрузка сервера",
                        //             "Ошибка в коде сервера",
                        //             "Ошибка в файле .htaccess"
                        //         ]
                        //     },
                        //     "message_datetime": "2023-02-12T18:02:26"
                        // },
                        // {
                        //     "type": "lazy_loading",
                        //     "page": {
                        //         "id": 1,
                        //         "name": "МИРЭА"
                        //     },
                        //     "detail": {
                        //         "time": 1215,
                        //         "reasons": [
                        //             "Большой трафик",
                        //             "DDOS",
                        //             "т.д."
                        //         ]
                        //     },
                        //     "message_datetime": "2023-02-12T18:02:26"
                        // },
                        // {
                        //     "type": "report",
                        //     "page": {
                        //         "id": 1,
                        //         "name": "МИРЭА"
                        //     },
                        //     "detail": {
                        //         "added_at": "2023-02-12T18:00:25",
                        //         "message": "Сайт не работает из Рязани",
                        //         "user": {
                        //             "id": 18,
                        //             "username": "Tester 2356"
                        //         }
                        //     },
                        //     "message_datetime": "2023-02-12T18:02:26"
                        // },
                        // {
                        //     "type": "review",
                        //     "page": {
                        //         "id": 1,
                        //         "name": "МИРЭА"
                        //     },
                        //     "detail": {
                        //         "mark": 3,
                        //         "message": "Сайт плохой",
                        //         "user": {
                        //             "id": 18,
                        //             "username": "Tester 2356"
                        //         }
                        //     },
                        //     "message_datetime": "2023-02-12T18:02:26"
                        // },
                    ]
                };
            }
        },
    },

    mutations: {
    }
}