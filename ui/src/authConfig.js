export const msalConfig = {
    auth: {
        postLogoutRedirectUri: "/login", // Indicates the page to navigate after logout.
        navigateToLoginRequestUrl: false, // If "true", will navigate back to the original request location before processing the auth code response.
        clientId: "397882f2-c3b9-4989-b20f-51af37cc1dda",
        authority: "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/",
        redirectUri: window.location.origin // "http://localhost:8080/"
    },
    cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false,
    },
    system: {
        loggerOptions: {
            loggerCallback: (level, message, containsPii) => {
                if (containsPii) {
                    return;
                }
                return;
            }
        }
    }
};

export const loginRequest = {
    scopes: []
};

export const protectedResources = {
    graphMe: {
        endpoint: "https://graph.microsoft.com/v1.0/me",
        scopes: ["User.Read"],
    },
    apiHello: {
        endpoint: "http://localhost:5000/api",
        scopes: ["api://583c8d92-37c2-48f7-b918-3a7156b66354/access_as_user"],

        // test version
        // scopes: ["api://5ac8ac35-170d-430a-b03d-b3d4b7cc6a70/access_as_user"],
        // scopes: ["api://583c8d92-37c2-48f7-b918-3a7156b66354/user_impersonation"],
        // scopes: ["api://583c8d92-37c2-48f7-b918-3a7156b66354/access_as_user",]
        //  "api://5ac8ac35-170d-430a-b03d-b3d4b7cc6a70/user_impersonation"],
    },
}