import axios from 'axios';
import React, { Component } from "react";
import uploadFileIcon from "../assets/Picto_Cloud.png"
import successfulUploadFileIcon from "../assets/Picto_DockSheet_valid.png"
import LinkWithCopyToClipboardButton from "./LinkWithCopyToClipboardButton"
import { Auth } from "aws-amplify";

export default class UploadAFileModal extends Component {

    constructor(props) {
        super(props)
        this.toggleModal = this.toggleModal.bind(this)
        this.state = {
            modalIsActive: false,
            selectedFile: null,
            fileState: "UNSELECTED",
            uploadingProgress: 0,
            jwtToken: ""
        }
    }

    componentDidMount() {
        Auth.currentSession()
            .then((data) => {
                console.log(data)
                this.setState({ user: { email: data.getIdToken().payload.email } })
                this.setState({ jwtToken: data.getAccessToken().jwtToken })
                console.log(this.state.user)
            }
            ).catch((e) => {
                console.log(e)
            })

    }

    toggleModal() { this.setState({ modalIsActive: !this.state.modalIsActive }) }

    onFileChange = (event) => {
        this.setState({ selectedFile: event.target.files[0] })
        this.setState({ fileState: "SELECTED" })
    }

    onFileUpload = async () => {

        if (this.state.selectedFile) {
            this.setState({ fileState: "UPLOADING" })
            const config = {
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
                    this.setState({ uploadingProgress: percentCompleted })
                    console.log(percentCompleted)
                }
            }

            // create exchange
            await axios({
                method: 'post',
                url: 'https://dev.api.bda.ninja/exchanges',
                headers: { Authorization: this.state.jwtToken }
            }).then(response => {
                this.setState({ uploadToken: response.data.upload_token })
                this.setState({ downloadToken: response.data.download_token })
            }).catch((error) => console.log(error))

            // get presigned upload url
            console.log(this.state.uploadToken)
            await axios({
                method: 'get',
                url: `https://dev.api.bda.ninja/s3_presigned_upload_url?filename=${this.state.selectedFile.name}`,
                headers: { Authorization: this.state.uploadToken }
            }).then(response => {
                this.setState({ uploadUrl: response.data.url })
                this.setState({ uploadUrlFields: response.data.fields })
            }).catch((error) => console.log(error))


            // post presigned upload url with file
            const formData = new FormData();
            for (const field in this.state.uploadUrlFields) {
                formData.append(field, this.state.uploadUrlFields[field])
            }
            formData.append(
                "file",
                this.state.selectedFile
                )

            axios({
                method: 'post',
                url: this.state.uploadUrl,
                data: formData,
                config
            }).then(response => {
                this.setState({
                    fileState: "UPLOADED",
                    selectedFile: null
                })
            })
                .catch(error => { console.log(error) })

        }
    }

    uploadFileButton = (text) => {
        return (
            <div className="file is-primary is-large is-centered">
                <label className="file-label">
                    <input
                        onChange={this.onFileChange}
                        className="file-input"
                        type="file"
                        name="file-to-share" />
                    <span className="file-cta button modal-button">
                        <span className="file-label">{text}</span>
                    </span>
                </label>
            </div>
        )
    }

    modalMenu = () => {
        if (this.state.fileState === "UNSELECTED") {
            return (
                <section>
                    <figure className="image container is-128x128">
                        <img alt="icône d'un fichier à téléverser" src={uploadFileIcon} />
                    </figure>
                    <h2 className="title">Téléversez votre fichier</h2>
                    <p>
                        Attention, vous ne pouvez téléverser qu'un seul fichier, <br />
                        donc favorisez le <code>zip</code> si vous avez plus d'un fichier
                    </p>
                    <br />
                    {this.uploadFileButton("Sélectionnez votre fichier")}
                </section>
            )
        }
        if (this.state.fileState === "SELECTED") {
            return (
                <section>
                    <figure className="image container is-128x128">
                        <img alt="icône fichier sélectionné" src={uploadFileIcon} />
                    </figure>
                    <br />
                    <output className="has-text-weight-medium">{this.state.selectedFile.name} sélectionné</output>
                    <p>ou</p>
                    <br />
                    {this.uploadFileButton("Changez de fichier")}
                </section>
            )
        }
        if (this.state.fileState === "UPLOADING") {
            return (
                <section>
                    <figure className="image container is-128x128">
                        <img alt="icône fichier en train d'être téléversé" src={uploadFileIcon} />
                    </figure>
                    <br />
                    <output className="has-text-weight-medium">{this.state.selectedFile.name}</output>
                    <progress
                        className="progress is-primary"
                        value={this.state.uploadingProgress}
                        max="100">
                        {this.state.uploadingProgress}%
                    </progress>
                    <p>Téléversement en cours {this.state.uploadingProgress}% ...</p>
                    <br />
                </section>
            )
        }
        if (this.state.fileState === "UPLOADED") {
            return (
                <section>
                    <figure className="image container is-128x128">
                        <img alt="icône fichier uploadé" src={successfulUploadFileIcon} />
                    </figure>
                    <br />
                    <h2 className="title">Vous avez terminé !</h2>
                    <p>Copiez le lien à transmettre à votre client</p>
                    <LinkWithCopyToClipboardButton link="https://file.octo.com/dqOtleC445" />
                    <br />
                </section>
            )
        }
    }

    render() {
        const roundedCorners = { borderRadius: '10px' }
        const alignRight = { justifyContent: 'flex-end' }

        return this.props.authState === "signedIn" && (
            <section>
                <button
                    className="button is-primary is-large modal-button"
                    onClick={this.toggleModal}>Téléverser !
                </button>

                <div className={`modal ${this.state.modalIsActive ? "is-active" : ""}`}>
                    <div className="modal-background" onClick={this.toggleModal}></div>

                    <div className="modal-card" style={roundedCorners}>

                        <section className="modal-card-body">
                            <section className="has-text-centered">

                                {this.modalMenu(this.state.selectedFile)}
                            </section>
                        </section>

                        <footer className="modal-card-foot" style={alignRight}>
                            <button id="close-modal-button" className="button" onClick={this.toggleModal}>Annuler</button>
                            <button
                                onClick={this.onFileUpload}
                                className="button is-primary upload-button"
                                disabled={!this.state.selectedFile}>
                                Téléverser
                            </button>
                        </footer>
                    </div>

                </div>
            </section>
        )
    }
}