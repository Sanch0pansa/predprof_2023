import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    login: `${Url}/auth/user/login/`,
    register: `${Url}/auth/user/registration/`,
    getUserData: `${Url}/user/me/`,
    logout: `${Url}/auth/token/logout/`,
    patchUserData: `${Url}/user/change_account_info/`
}

export default {
    namespaced: true,
    state: () => ({
        isAuth: JSON.parse(localStorage.getItem('isAuth')),
        authToken: localStorage.getItem('authToken'),
        user: JSON.parse(localStorage.getItem('user') ?? "{}"),
        isAdmin: JSON.parse(localStorage.getItem('isAdmin')),
        isModerator: JSON.parse(localStorage.getItem('isModerator')),
    }),
    actions: {
        // Функция авторизации
        async authentificate({state, commit, dispatch}, {login, password}) {
            try {
                // Пробуем получить ответ
                const res = await axios.post(
                    URLS.login,
                    {
                        login: login,
                        password: password
                    }
                );

                const data = res.data;

                // Если токен пришел, заполняем соответствующее состояние
                if (data.auth_token) {
                    commit('setIsAuth', true);
                    commit('setAuthToken', data.auth_token);

                    await dispatch('getUserData');

                    return {success: true, detail: "Вход выполнен"};
                } else {

                    return {success: false, detail: data};
                }

            } catch (e) {
                return {success: false, detail: e.response.data.errors};
            }
        },

        // Регистрация
        async registrate({state, commit, dispatch}, {login, password, username}) {
            try {
                // Пробуем получить ответ
                await axios.post(
                    URLS.register,
                    {
                        email: login,
                        password: password,
                        username: username,
                    }
                );

                // Если ошибок нет, то есть, вернулся 2хх код, пробуем автоматически авторизоваться с введенными данными
                const res = await dispatch('authentificate', {login, password});

                // Если авторизация с новыми данными прошла успешно, то есть, пользователь полностью был создан, возвращаем успех
                if (res.success) {
                    return {success: true, detail: "Регистрация успешна"}
                } else {
                    return {success: false, detail: {non_field_errors: ["Что-то пошло не так"]}}
                }

            } catch (e) {

                return {success: false, detail: e.response.data.errors};
            }
        },

        // Получение данных пользователя
        async getUserData({state, commit, dispatch}) {
            try {
                const res = await axios.get(
                    URLS.getUserData, {
                        headers: {
                            Authorization: `Token ${state.authToken}`
                        }
                    },
                );

                commit('setUser', res.data)
                commit('setIsModerator', res.data.is_moderator)
                commit('setIsAdmin', res.data.is_admin)

            } catch (e) {

            }
        },

        // Выход из лк
        async logout({state, commit}) {
            try {
                const res = await axios.post(
                    URLS.logout,
                    {},
                    {headers: {
                            Authorization: `Token ${state.authToken}`
                        }},
                );


            } catch (e) {

            }

            commit("setIsAuth", false);
            commit("setIsModerator", false);
            commit("setIsAdmin", false);
            commit("setAuthToken", "");
            commit("setUser", {});
        },


        // Изменение данных пользователя
        async patchUserData({state, commit, rootState}, data) {
            try {
                // Пробуем получить ответ
                await axios.patch(
                    URLS.patchUserData,
                    data,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                // Если ошибок нет, то есть, вернулся 2хх код, пробуем автоматически получить данные
                const res = await dispatch('getUserData');

                // Если получение новых данных прошло успешно, то есть, пользователь изменил данные, возвращаем успех
                if (res.success) {
                    return {success: true, detail: "Изменение данных успешно"}
                } else {
                    return {success: false, detail: {non_field_errors: ["Что-то пошло не так"]}}
                }

            } catch (e) {

                return {success: false, detail: e.response.data.errors};
            }
        }
    },
    mutations: {
        setIsAuth(state, isAuth) {
            state.isAuth = isAuth;
            localStorage.setItem("isAuth", isAuth);
        },
        setIsModerator(state, isModerator) {
            state.isModerator = isModerator;
            localStorage.setItem("isModerator", isModerator);
        },
        setIsAdmin(state, isAdmin) {
            state.isAdmin = isAdmin;
            localStorage.setItem("isAdmin", isAdmin);
        },
        setAuthToken(state, authToken) {
            state.authToken = authToken;
            localStorage.setItem("authToken", authToken);
        },
        setUser(state, user) {
            state.user = user;
            localStorage.setItem("user", JSON.stringify(user));
        },
    },
    getters: {
        getAuthToken(state) {
            return state.authToken
        },

        getIsModerator(state) {
            return state.isModerator;
        }
    }

}