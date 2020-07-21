export default {
    Auth: {
        region: "eu-west-1",
        userPoolId: process.env.REACT_APP_USER_POOL_ID,
        userPoolWebClientId: process.env.REACT_APP_USER_POOL_WEB_CLIENT_ID,
        oauth: {
            domain: process.env.REACT_APP_OAUTH_DOMAIN,
            scope: ["email", "profile", "openid"],
            redirectSignIn: process.env.REACT_APP_OAUTH_CALLBACK_URL,
            redirectSignOut: process.env.REACT_APP_OAUTH_SIGNOUT_URL,
            responseType: "code",
        },
    },
};