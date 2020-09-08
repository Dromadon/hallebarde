import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import "../style/App.css";
import "../style/App.sass";
import SignInOrOutButton from "./SignInOrOutButton";
import Download from "./Download"
import UploadAFileModal from "./UploadAFileModal";
import Amplify, { Auth, Hub } from "aws-amplify";
import config from "../OAuth/config";

Amplify.configure(config);

class App extends Component {
  _isMounted = false;

  constructor(props) {
    super(props);
    this.state = {
      authState: "loading",
      authData: null,
      authError: null,
      user: { email: "" },
    };
    this.signOut = this.signOut.bind(this);

    Hub.listen("auth", (data) => {
      switch (data.payload.event) {
        case "signIn":
          this.setState({
            authState: "signedIn",
            authData: data.payload.data,
            authError: null,
          });
          break;
        case "signIn_failure":
          this.setState({
            authState: "signIn",
            authData: null,
            authError: data.payload.data,
          });
          break;
        default:
          break;
      }
    });
  }

  componentDidMount() {
    this._isMounted = true;
    Auth.currentAuthenticatedUser()
      .then((user) => {
        this.setState({ authState: "signedIn" });
      })
      .catch((e) => {
        console.log(e);
        this.setState({ authState: "signIn" });
      });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  signOut = () => {
    Auth.signOut()
      .then(() => {
        this.setState({ authState: "signIn" });
      })
      .catch((e) => {
        console.log(e);
      });
  };

  render() {
    return (
      < Router >
        <div>
          <Switch>
            <Route path="/download" component={Download}>
            </Route>
            <Route path="/">
              <Home authState={this.state.authState} signOut={this.signOut}/>
            </Route>
          </Switch>
        </div>
      </Router >
    );
  }
}

function Home(props) {
  return (<div className="App">
    <section className="hero is-fullheight">
      <div className="hero-body">
        <div className="container has-text-centered">
          <figure className="image container is-128x128">
            <img
              alt="octo logo"
              src="https://www.octo.com/wp-content/themes/octo-v1/img/logo-mini-color.svg"
            />
          </figure>
          <section id="login">
            <h1 className="title">
              Bienvenue sur le partage de fichiers !
                </h1>
            <h2 className="subtitle is-size-6">
              Envoi de fichiers sécurisés permettant de mettre à disposition
              un lien de
                  <br />
              téléchargement pendant 7 jours à vos clients.
                </h2>
            <SignInOrOutButton
              authState={props.authState}
              signOut={props.signOut}
            />
            {props.authState === 'signedIn' && <UploadAFileModal authState={props.authState} />}
          </section>
        </div>
      </div>
    </section>
  </div>)
}

export default App;
