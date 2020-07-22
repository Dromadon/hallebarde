import React from "react";
import { Component } from "react";

export default class LinkWithCopyToClipboardButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      link: props.link,
      clicked: false,
    };
  }
  copyContentOnClick = (event) => {
    navigator.clipboard
      .writeText(this.state.link)
      .then(() => this.setState({ clicked: true }));

    setTimeout(() => {
      this.setState({ clicked: false });
    }, 3000);
  };

  render() {
    return (
      <button
        onClick={this.copyContentOnClick}
        data-tooltip={
          this.state.clicked ? "Copié !" : "Cliquez pour copier le lien"
        }
        className={`button has-text-weight-medium is-info has-text-centered ${
          this.state.clicked ? "has-tooltip-success" : ""
        }`}
      >
        {this.state.link}
      </button>
    );
  }
}
