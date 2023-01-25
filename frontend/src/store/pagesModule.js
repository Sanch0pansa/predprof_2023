import axios from 'axios'

const URLS = {
    getPopularPages: "http://127.0.0.1:8000/api/v1/page/get_popular_pages/",
    getCheckingPages: "http://127.0.0.1:8000/api/v1/page/get_checking_pages/",
    getStatistics: "http://127.0.0.1:8000/api/v1/page/get_statistic/",
}

export default {
    namespaced: true,
    state: () => ({

    }),
    actions: {

        // Получение популярных страниц
        async getPopularPages({state, commit}) {
            try {
                const response = await axios.get(
                    URLS.getPopularPages,
                );

                if (response.data['details']) {
                    return [];
                } else {
                    return response.data;
                }

            } catch (e) {
                return [];
            }
        },

        // Получение популярных страниц
        async getCheckingPages({state, commit}) {
            try {
                const response = await axios.get(
                    URLS.getCheckingPages,
                );

                if (response.data['details']) {
                    return [];
                } else {
                    return response.data;
                }

            } catch (e) {
                return [];
            }
        },

        // Получение статистики
        async getStatistics({state, commit}) {
            try {
                const response = await axios.get(
                    URLS.getStatistics,
                );

                if (response.data['details']) {
                    return {
                        "total_pages": 0,
                        "total_reports": 0,
                        "total_reviews": 0,
                        "detected_failures": 0
                    };
                } else {
                    return response.data;
                }

            } catch (e) {
                return {
                    "total_pages": 0,
                    "total_reports": 0,
                    "total_reviews": 0,
                    "detected_failures": 0
                };
            }
        },
    },

}