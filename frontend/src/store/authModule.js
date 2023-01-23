import axios from 'axios'

URL = "http://127.0.0.1:8000/api/v1/token/login/"

export default {
    namespaced: true,
    state: () => ({
        isAuth: false,
        authToken: ""
    }),
    actions: {
        async authentificate({state, commit}, {login, password}) {
            try {
                const response = await axios.post(
                    URL,
                    {
                        email: login,
                        password: password
                    }
                );

                const data = response.data;

                // const data = {
                //     success: true,
                //     auth_token: "dfgdgf"
                // }

                if (data.auth_token) {
                    commit('setIsAuth', true);
                    commit('setAuthToken', data.auth_token);

                    return {success: true, detail: "Вход выполнен"};
                } else {

                    return {success: false, detail: data};
                }

            } catch (e) {

                return {success: false, detail: e.response.data};
            }
        }
    },
    mutations: {
        setIsAuth(state, isAuth) {
            state.isAuth = isAuth;
        },
        setAuthToken(state, authToken) {
            state.authToken = authToken;
        },
    }

}