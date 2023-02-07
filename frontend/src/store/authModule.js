import axios from 'axios'

const URLS = {
    login: "http://127.0.0.1:8000/api/v1/auth/user/login/",
    register: "http://127.0.0.1:8000/api/v1/auth/user/registration/",
    getUserData: "http://127.0.0.1:8000/api/v1/user/me/",
    logout: "http://127.0.0.1:8000/api/v1/auth/token/logout/"
}

export default {
    namespaced: true,
    state: () => ({
        isAuth: JSON.parse(localStorage.getItem('isAuth')),
        authToken: localStorage.getItem('authToken'),
        user: JSON.parse(localStorage.getItem('user') ?? "{}")
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
        async getUserData({state, commit}) {
            try {
                const res = await axios.get(
                    URLS.getUserData, {
                        headers: {
                            Authorization: `Token ${state.authToken}`
                        }
                    },
                );

                commit('setUser', res.data)
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
            commit("setAuthToken", "");
            commit("setUser", {});
        }
    },
    mutations: {
        setIsAuth(state, isAuth) {
            state.isAuth = isAuth;
            localStorage.setItem("isAuth", isAuth);
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
        }
    }

}