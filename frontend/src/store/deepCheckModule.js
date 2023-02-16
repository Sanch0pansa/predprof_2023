import axios from 'axios'
import Url from "@/store/url";


const URLS = {
    makeReport: level => `${Url}/page/make_report/${level}/`,
}

export default {
    namespaced: true,
    state: () => ({
    }),
    actions: {
        // Получение первичных данных
        async getFirstRequest({rootState}, {url}) {

            try {
                const resp = await axios.post(
                    URLS.makeReport(1),
                    {
                        url: url,
                    },
                    {

                    }
                );

                return resp.data;

            } catch(e) {
                return {
                    id: 0, // ID для последующего дописывания

                    has_data: false, // Есть ли инфа по этому ресурсу

                    ping: 0, // Пингование
                    response_status_code: 200, // Код ответа
                    response_time: 0, // Задержка ответа
                };
            }
        },

        // Получение данных Google Page Speed Insights
        async getSecondRequest({rootState}, {id}) {

            try {
                const resp = await axios.post(
                    URLS.makeReport(2),
                    {
                        id: id
                    },
                    {

                    }
                );

                return resp.data;

            } catch(e) {
                return {
                    first_contentful_paint: 0,
                    first_meaningful_paint: 0,
                    largest_contentful_paint: 0,
                    speed_index: 0,
                    full_page_loading_time: 0,
                    score: 0,
                };
            }
        },

        // Получение данных по документу и, если есть, по проверкам и сообщениям об ошибках
        async getThirdRequest({rootState}, {id, date_from, date_to}) {
            try {
                const resp = await axios.post(
                    URLS.makeReport(3),
                    {
                        id: id,
                        date_from: date_from,
                        date_to: date_to
                    },
                    {

                    }
                );

                return resp.data;

            } catch(e) {
                return {
                    document_url: "",
                    other_check_reports: [
                    ],
                };
            }
        },
    },

    mutations: {
    }
}