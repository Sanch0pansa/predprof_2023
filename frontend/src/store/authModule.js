import axios from 'axios'

URL = "https://127.0.0.1"

export default {
    namespaced: true,
    state: () => ({
        isAuth: false,
        authToken: ""
    }),
    actions: {
        async authentificate({state, commit}, {login, password}) {
            try {
                // response = await axios.post(
                //     URL,
                //     {
                //         login: login,
                //         password: password
                //     }
                // );
                // data = response.json();

                const data = {
                    success: false,
                    // auth_token: "dfgdgf"
                }

                if (data.success) {
                    commit('setIsAuth', true);
                    commit('setAuthToken', data.auth_token);
                }

                return {"success": response.json().success};
            } catch (e) {
                return {"success": false};
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