import axios from 'axios'
import Url from "@/store/url";

const URLS = {
    generateTelegramCode: `${Url}/user/generate_telegram_code/`,
    unlinkTelegram: `${Url}/user/unlink_telegram/`,
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

        // Отвязка телеграма
        async unlinkTelegram({state, commit, rootState}) {
            try {
                const response = await axios.delete(
                    URLS.unlinkTelegram,
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
        }
    },

}