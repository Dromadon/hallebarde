import React from "react";
import { withOAuth } from "aws-amplify-react";

function OAuthButton(props) {
  return (
    <button
      className="button has-text-weight-bold"
      onClick={props.OAuthSignIn}>
      <span className="icon">
        <img
        className="image is-16x16"
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png"
        alt="Google icon"/>
      </span>
      <span>Sign in with Google</span>
    </button>
  )
}

export default withOAuth(OAuthButton);
