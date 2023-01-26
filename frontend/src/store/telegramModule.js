import axios from 'axios'

const URLS = {
    generateTelegramCode: "http://127.0.0.1:8000/api/v1/user/generate_telegram_code/",
}

export default {
    namespaced: true,
    state: () => ({

    }),
    actions: {

        // Запрос на генерацию телеграм-кода
        async generateTelegramCode({state, commit, rootState}) {
            try {
                const response = await axios.get(
                    URLS.generateTelegramCode,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    },
                );

                if (!response.data.detail) {
                    return {
                        success: true,
                        code: response.data.telegram_verification_code,
                        remain_time: response.data.remain_time,
                    };
                } else {
                    return {
                        success: false,
                        errors: response.data.errors,
                        code: response.data.telegram_verification_code,
                        remain_time: response.data.remain_time,
                    };
                }

            } catch (e) {
                return {success: false, error: e.response.data};
            }
        },
    },

}