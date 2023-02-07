import axios from 'axios'


const URLS = {
    getModerationCategories: `http://127.0.0.1:8000/api/v1/moderation/get_categories/`,
    getModerationPages: `http://127.0.0.1:8000/api/v1/moderation/pages/`,
    getRejectedPages: `http://127.0.0.1:8000/api/v1/moderation/rejected_pages/`,
    patchPageStatus: id => `http://127.0.0.1:8000/api/v1/moderation/moderate/page/${id}/`,
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

        // Получение модерируемых страниц
        async getModerationPages({state, commit, rootState}) {

            if (!rootState.auth.isModerator) {
                return [];
            }

            try {
                const resp = await axios.get(
                    URLS.getModerationPages,
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
        async getRejectedPages({state, commit, rootState}) {

            if (!rootState.auth.isModerator) {
                return [];
            }

            try {
                const resp = await axios.get(
                    URLS.getRejectedPages,
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

        // Изменение статуса страницы
        async patchPageStatus({state, commit, rootState}, {id, action}) {
            if (!rootState.auth.isModerator) {
                return {success: false};
            }

            try {
                const resp = await axios.patch(
                    URLS.patchPageStatus(id),
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