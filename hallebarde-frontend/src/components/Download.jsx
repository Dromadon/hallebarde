import axios from "axios";
import React, { Component } from "react";
import backendConfig from "../backend/config";

export default class Download extends Component {
  constructor(props) {
    super(props);
    this.state = {
        isLoading: false
    }
  }

  handleClickOnDownloadButton = () => {
    this.setState({'isLoading': true})

    const download_token = new URLSearchParams(this.props.location.search).get(
      "download_token"
    );
    const url = backendConfig.backend_url + "/s3_presigned_download_url";
    axios
      .request({
        url,
        method: "GET",
        headers: { Authorization: download_token },
      })
      .then(({ data }) => {
        this.setState({'isLoading': false})
        window.open(data, '_self')
      });
  };

  render() {
    return (
      <div className="App">
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
                <button
                  onClick={this.handleClickOnDownloadButton}
                  className={`button has-text-weight-medium is-info has-text-centered ${this.state.isLoading ? "is-loading" : "" }`}
                >
                  Téléchargez
                </button>
              </section>
            </div>
          </div>
        </section>
      </div>
    );
  }
}
