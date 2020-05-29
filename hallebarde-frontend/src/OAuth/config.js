export default {
    Auth: {
        region: "eu-west-1",
        userPoolId: "eu-west-1_v0laOwH0X",
        userPoolWebClientId: "6h9vs34mtffltbbg16dughqomj",
        oauth: {
            domain: "hallebarde-dev.auth.eu-west-1.amazoncognito.com",
            scope: ["email", "profile", "openid"],
            redirectSignIn: "http://localhost:3000/callback",
            redirectSignOut: "http://localhost:3000/logout",
            responseType: "code",
        },
    },
};