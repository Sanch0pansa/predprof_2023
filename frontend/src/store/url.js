const serverUrlEl = document.querySelector('.server');
const URL = `${serverUrlEl.innerHTML}/api/v1`;
serverUrlEl.remove();

export default URL;