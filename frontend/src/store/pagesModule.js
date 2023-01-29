import axios from 'axios'

const URLS = {
    getPopularPages: "http://127.0.0.1:8000/api/v1/page/get_popular_pages/",
    getCheckingPages: "http://127.0.0.1:8000/api/v1/page/get_checking_pages/",
    getStatistics: "http://127.0.0.1:8000/api/v1/page/get_statistic/",
    getPageData: id => `https://127.0.0.1:8000/api/v1/page/${id}`,
    getPageChecks: id => `https://127.0.0.1:8000/api/v1/page/${id}/checks`,
    getPageReports: id => `https://127.0.0.1:8000/api/v1/page/${id}/reports`,
    getPageReviews: id => `https://127.0.0.1:8000/api/v1/page/${id}/reviews`,
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
        async getCheckingPages({state, commit}, {first=false}) {
            try {
                if (first) {
                    commit('setCanLoadMore', true);
                    commit('setPageNumber', 1);
                }

                const response = await axios.post(
                    URLS.getCheckingPages,
                    {
                        page_number: state.pageNumber,
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
                    title: 'Some page',
                    url: 'https://site.com',
                    description: "Загрузка не получилось, описание только такое(",
                    status: 2,
                    rating: 0,
                },
                lastCheck: {
                    status: 2,
                    response_time: 0,
                    checked_at: "22 янв 2023, 23:34:32"
                },
                checks: [
                    {
                        checked_at: "2023-01-23T18:04:05.000Z",
                        response_time: 26,
                        check_status: 2,
                    },
                    {
                        checked_at: "2023-01-23T19:04:05.000Z",
                        response_time: 23,
                        check_status: 2,
                    },
                    {
                        checked_at: "2023-01-23T20:04:05.000Z",
                        response_time: 21,
                        check_status: 2,
                    },
                    {
                        checked_at: "2023-01-23T21:04:05.000Z",
                        response_time: 68,
                        check_status: 1,
                    },
                    {
                        checked_at: "2023-01-23T22:04:05.000Z",
                        response_time: 24,
                        check_status: 2,
                    },
                    {
                        checked_at: "2023-01-23T23:04:05.000Z",
                        response_time: 36,
                        check_status: 2,
                    },
                ],
                reviews: [
                    {
                        added_at: "2023-01-23T23:04:05.000Z",
                        mark: 4.5,
                        message: "Всё работает",
                        added_by_user__username: "MGTU_Admin",
                        added_by_user: 1,
                    },
                ],
                reports: [
                    {
                        added_at: "2023-01-23T23:04:05.000Z",
                        message: "Всё работает",
                        added_by_user__username: "MGTU_Admin",
                        added_by_user: 1,
                    }
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

                page.reviews = resp.data;
            } catch {

            }

            // Запись текущего состояние сайта из последней проверки
            if (page.checks.length) {
                page.data.status = page.checks[page.checks.length - 1].check_status;
            }

            // Рассчёт среднего рейтинга
            if (page.reviews.length) {
                let sum = 0;
                page.reviews.forEach(review => sum += review.mark);
                page.data.rating = Math.round(100 * sum / page.reviews.length) / 100;
            }

            return page;
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