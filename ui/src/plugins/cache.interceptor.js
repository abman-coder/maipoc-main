let cache = new Map();
const maxAge = 120000;

export default {
    get: (method, url, body) => {
        if (url.includes("nocache=true")) {
            return undefined
        }
        const cached = cache.get(url + method + JSON.stringify(body));
        if (!cached) {
            return undefined;
        } else {
            const isExpired = cached.lastRead < Date.now() - maxAge;
            return isExpired ? undefined : JSON.parse(JSON.stringify(cached.response));
        }
    },
    put: (method, inputUrl, body, response) => {
        if (
            method !== "put" &&
            (response && response.data && response.status < 300)
        ) {
            let splits = inputUrl.split("?")
            const url = inputUrl.replace("?nocache=true", "") + method + JSON.stringify(body);
            let expDef = 0
            const entry = { url, response: JSON.parse(JSON.stringify(response)), lastRead: Date.now() + expDef };
            cache.set(url, entry);
            // remove expired cache entries
            const expired = Date.now() - maxAge;
            cache.forEach(expiredEntry => {
                if (expiredEntry.lastRead < expired) {
                    cache.delete(expiredEntry.url);
                }
            });
        }
    },
    clear: () => {
        cache.forEach(remove => {
            cache.delete(remove.url);
        });
    }
}