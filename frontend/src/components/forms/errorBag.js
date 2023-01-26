export const errorBagFill = (bag, res) => {
    if (res.success) {
        bag["success"] = res.detail;
    } else {
        for (let key in res.detail) {
            bag[key] = res.detail[key];
        }
    }
}