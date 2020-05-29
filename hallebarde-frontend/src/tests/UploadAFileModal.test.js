import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import UploadAFileModal from "../components/UploadAFileModal"

test('modal is disabled when not logged in', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signIn" />);

    // Then
    const modalComponent = container.querySelector('.modal')
    expect(modalComponent).toBeNull()
})

test('modal is not displayed at first, when signed in', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signedIn" />);

    // Then
    const modalComponent = container.querySelector('.modal')
    expect(modalComponent).not.toBeNull()

    // And Then
    const modalComponentNotDisplayed = container.querySelector('.modal.is-active')
    expect(modalComponentNotDisplayed).toBeNull()
})

test('modal is displayed when signed in and "call to action" clicked', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signedIn" />);

    // When
    const button = container.querySelector('button')
    fireEvent.click(button)

    // Then
    const modalComponentDisplayed = container.querySelector('.modal.is-active')
    expect(modalComponentDisplayed).not.toBeNull()
})

test('modal can be closed when clicking on a button', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signedIn" />);
    const button = container.querySelector('button')
    fireEvent.click(button)
    const modalComponent = container.querySelector('.modal.is-active')
    expect(modalComponent).not.toBeNull()

    // When
    const closeModalButton = container.querySelector('#close-modal-button')
    expect(closeModalButton).not.toBeNull()
    fireEvent.click(closeModalButton)

    // Then
    const modalComponentAfterClickingCloseButton = container.querySelector('.modal.is-active')
    expect(modalComponentAfterClickingCloseButton).toBeNull()
})

test('modal can be closed when clicking on its background', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signedIn" />);
    const button = container.querySelector('.modal-button')
    fireEvent.click(button)
    const modalComponent = container.querySelector('.modal.is-active')
    expect(modalComponent).not.toBeNull()

    // When
    const modalBackground = container.querySelector('.modal-background')
    expect(modalBackground).not.toBeNull()
    fireEvent.click(modalBackground)

    // Then
    const modalComponentAfterClickingItsBackground = container.querySelector('.modal.is-active')
    expect(modalComponentAfterClickingItsBackground).toBeNull()
})

test('upload button in modal is disabled when no file is selected', () => {
    // Given
    const { container } = render(<UploadAFileModal authState="signedIn" />);
    const button = container.querySelector('.modal-button')
    fireEvent.click(button)
    const modalComponent = container.querySelector('.modal.is-active')
    expect(modalComponent).not.toBeNull()

    // Then
    const disabledUploadButton = container.querySelector('.upload-button[disabled]')
    expect(disabledUploadButton).not.toBeNull()
})