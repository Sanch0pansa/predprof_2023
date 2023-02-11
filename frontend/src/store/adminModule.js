import axios from 'axios'
import Url from "@/store/url";


const URLS = {
    getStaffUsers: `${Url}/admin/staff_users/`,
    changeUserRights: id => `${Url}/admin/change_user_rights/${id}/`,
    searchUser: search => `${Url}/admin/search_user/${search}/`,
}

export default {
    namespaced: true,
    state: () => ({

    }),
    actions: {
        // Сменить полномочия пользователя
        async changeUserRights({rootState}, {newRight, id}) {
            if (!rootState.auth.isAdmin) {
                return {success: false};
            }

            try {
                const resp = await axios.post(
                    URLS.changeUserRights(id),
                    {
                        rights: newRight,
                    },
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return {success: false};

            } catch(e) {
                return {success: false};
            }
        },

        // Получение списка уполномоченных пользователей (без пагинации, ибо их не должно быть много)
        async getStaffUsers({rootState}) {
            if (!rootState.auth.isAdmin) {
                return [];
            }

            try {
                const resp = await axios.get(
                    URLS.getStaffUsers,
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return resp.data;

            } catch(e) {
                return [

                ];
            }
        },

        // Поиск пользователя по юзернейму
        async searchUser({rootState}, {search}) {
            if (!rootState.auth.isAdmin) {
                return [];
            }

            try {
                const resp = await axios.get(
                    URLS.searchUser(search),
                    {
                        headers: {
                            Authorization: `Token ${rootState.auth.authToken}`
                        }
                    }
                );

                return resp.data;

            } catch(e) {
                return [
                    {
                        id: 18,
                        username: "Usr 1"
                    },

                    {
                        id: 19,
                        username: "Usr 2"
                    },
                ];
            }
        }
    },

    mutations: {
    }
}