import axios from 'axios'
import Url from "@/store/url";


const URLS = {
    getModerationCategories: `${Url}/moderation/get_categories/`,
    getModerationPages: `${Url}/moderation/pages/`,
    getRejectedPages: `${Url}/moderation/rejected_pages/`,
    getModerationReviews: `${Url}/moderation/reviews/`,
    getRejectedReviews: `${Url}/moderation/rejected_reviews/`,
    getModerationReports: `${Url}/moderation/reports/`,
    getRejectedReports: `${Url}/moderation/rejected_reports/`,
    patchPageStatus: id => `${Url}/moderation/moderate/page/${id}/`,
    patchReviewStatus: id => `${Url}/moderation/moderate/review/${id}/`,
    patchReportStatus: id => `${Url}/moderation/moderate/report/${id}/`,
}

export default {
    namespaced: true,
    state: () => ({
        pages: 0,
        reviews: 0,
        reports: 0
    }),
    actions: {

        // Получение категорий модерируемой информации
        async getModerationCategories({state, commit, rootState}) {
            try {
                const resp = await axios.get(
                    URLS.getModerationCategories,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                commit('setPages', resp.data.pages);
                commit('setReviews', resp.data.reviews);
                commit('setReports', resp.data.reports);

            } catch(e) {

                commit('setPages', 1);
                commit('setReviews', 2);
                commit('setReports', 3);
            }
        },

        // Получение элементов для модерации
        async getItems({rootState}, {url}) {
            if (!rootState.auth.isModerator) {
                return [];
            }

            try {
                const resp = await axios.get(
                    url,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return resp.data;

            } catch(e) {
                return [];
            }
        },

        // Получение отклонённых страниц
        async getRejectedPages({dispatch}) {
            return await dispatch("getItems", {url: URLS.getRejectedPages});
        },

        // Получение модерируемых страниц
        async getModerationPages({dispatch}) {
            return await dispatch("getItems", {url: URLS.getModerationPages});
        },

        // Получение отклонённых отзывов
        async getRejectedReviews({dispatch}) {
            return await dispatch("getItems", {url: URLS.getRejectedReviews});
        },

        // Получение модерируемых отзывов
        async getModerationReviews({dispatch}) {
            return await dispatch("getItems", {url: URLS.getModerationReviews});
        },

        // Получение отклонённых сообщений о сбоях
        async getRejectedReports({dispatch}) {
            return await dispatch("getItems", {url: URLS.getRejectedReports});
        },

        // Получение модерируемых сообщений о сбоях
        async getModerationReports({dispatch}) {
            return await dispatch("getItems", {url: URLS.getModerationReports});
        },

        // Изменение статуса модерируемого контента
        async patchItemStatus({state, commit, rootState}, {url, action}) {
            if (!rootState.auth.isModerator) {
                return {success: false};
            }

            try {
                const resp = await axios.patch(
                    url,
                    {
                        action: action
                    },
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return {success: resp.data.success};

            } catch(e) {
                return {success: false};
            }
        },

        // Изменение статуса страницы
        async patchPageStatus({dispatch}, {id, action}) {
            return await dispatch("patchItemStatus", {url: URLS.patchPageStatus(id), action: action});
        },

        // Изменение статуса отзывов
        async patchReviewStatus({dispatch}, {id, action}) {
            return await dispatch("patchItemStatus", {url: URLS.patchReviewStatus(id), action: action});
        },

        // Изменение статуса сообщений о сбоях
        async patchReportStatus({dispatch}, {id, action}) {
            return await dispatch("patchItemStatus", {url: URLS.patchReportStatus(id), action: action});
        }
    },

    mutations: {
        setPages(state, pages) {
            state.pages = pages;
        },
        setReviews(state, reviews) {
            state.reviews = reviews;
        },
        setReports(state, reports) {
            state.reports = reports;
        },
    }
}