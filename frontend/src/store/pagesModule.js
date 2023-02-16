import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    getPopularPages: `${Url}/page/get_popular_pages/`,
    getCheckingPages: `${Url}/page/get_checking_pages/`,
    getStatistics: `${Url}/page/get_statistic/`,
    createPage: `${Url}/page/`,
    getPageData: id => `${Url}/page/${id}/`,
    getPageChecks: id => `${Url}/page/${id}/checks/`,
    getPageReports: id => `${Url}/page/${id}/reports/`,
    getPageReviews: id => `${Url}/page/${id}/reviews/`,
    subscriptionPage: id => `${Url}/page/${id}/subscription/`,
}

export default {
    namespaced: true,
    state: () => ({
        pageNumber: 1,
        totalPagesNumber: 0,
        canLoadMore: true,
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
        async getCheckingPages({state, commit}, {first=false, search=''}) {
            try {
                if (first) {
                    commit('setCanLoadMore', true);
                    commit('setPageNumber', 1);
                }

                const response = await axios.post(
                    URLS.getCheckingPages,
                    {
                        page_number: state.pageNumber,
                        search: search
                    }
                );

                if (response.data['details']) {
                    return [];
                } else {

                    commit('setTotalPagesNumber', response.data.num_pages);
                    commit('setPageNumber', state.pageNumber + 1);

                    if (state.pageNumber > state.totalPagesNumber) {
                        commit('setCanLoadMore', false);
                    }

                    return response.data.pages;
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

        // Получение данных по одной странице
        async getPageData({state, commit}, {id}) {
            // Изначально пустые данные страницы
            let page = {
                data: {
                    name: '',
                    url: '',
                    description: "",
                    status: 3,
                    rating: 0,
                },
                lastCheck: {
                    status: 3,
                    response_time: 0,
                    checked_at: ""
                },
                checks: [

                ],
                reviews: [

                ],
                reports: [

                ],
            }

            // Получение данных самой страницы
            try {
                const resp = await axios.get(
                    URLS.getPageData(id)
                );

                page.data = resp.data;
            } catch {

            }

            // Получение проверок
            try {
                const resp = await axios.get(
                    URLS.getPageChecks(id)
                );

                page.checks = resp.data;
            } catch {

            }

            // Получение отзывов
            try {
                const resp = await axios.get(
                    URLS.getPageReviews(id)
                );
                page.reviews = resp.data;
            } catch {

            }

            // Получение репортов
            try {
                const resp = await axios.get(
                    URLS.getPageReports(id)
                );

                page.reports = resp.data;
            } catch {

            }

            // Запись текущего состояние сайта из последней проверки
            if (page.checks.length) {
                page.data.status = page.checks[page.checks.length - 1].check_status;
            }

            // Рассчёт среднего рейтинга
            page.data.rating = 0;
            if (page.reviews.length) {
                let sum = 0;
                page.reviews.forEach(review => sum += Number(review.mark));
                page.data.rating = Math.round(100 * sum / page.reviews.length) / 100;
            }

            return page;
        },

        // Получение данных об отслеживании страницы
        async getPageSubscription({state, commit, rootState}, {id}) {
            try {
                let res = await axios.get(
                    URLS.subscriptionPage(id),
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (res.data.subscribed) {
                    return {subscribed: true};
                }

                return {subscribed: false};

            } catch (e) {
                return {subscribed: false};
            }
        },

        // Включение отслеживания
        async subscribePage({state, commit, rootState}, {id}) {
            try {
                let res = await axios.post(
                    URLS.subscriptionPage(id),
                    {},
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (res.data.success) {
                    return {success: true};
                }

                return {success: false};

            } catch (e) {
                return {success: false};
            }
        },

        // Отключение отслеживания
        async unsubscribePage({state, commit, rootState}, {id}) {
            try {
                let res = await axios.delete(
                    URLS.subscriptionPage(id),
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (res.data.success) {
                    return {success: true};
                }

                return {success: false};

            } catch (e) {
                return {success: false};
            }
        },

        // Добавление ресурса
        async createPage({state, commit, rootState}, {name, description, url}) {
            try {
                let res = await axios.post(
                    URLS.createPage,
                    {
                        name: name,
                        description: description,
                        url: url,
                    },
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                if (res.data.success) {
                    return {success: true, detail: "Страница успешно добавлена"}
                } else {
                    return {success: false, detail: res.data.errors}
                }

            } catch (e) {
                return {success: false, detail: e.response.data.errors};
            }
        }
    },

    mutations: {
        setPageNumber(state, pageNumber) {
            state.pageNumber = pageNumber;
        },

        setTotalPagesNumber(state, totalPagesNumber) {
            state.totalPagesNumber = totalPagesNumber;
        },

        setCanLoadMore(state, canLoadMore) {
            state.canLoadMore = canLoadMore;
        }
    },
}