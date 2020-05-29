import OAuthButton from "./OAuthButton";
import React from "react";

export default function SignInOrOutButton(props) {
    const positionTopRight = {
        position: "Fixed",
        top: "20px",
        right: "20px"
    }
    return (
        <section>
            {props.authState === "loading" && <div>loading...</div>}
            {props.authState === "signIn" && <OAuthButton />}
            {props.authState === "signedIn" && (
                <button
                    className="button has-text-weight-bold"
                    style={positionTopRight}
                    onClick={props.signOut}>
                    Se déconnecter
                </button>
            )}
        </section>
    )
}