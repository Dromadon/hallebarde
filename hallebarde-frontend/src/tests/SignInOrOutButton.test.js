import React from 'react';
import {render} from '@testing-library/react';
import SignInOrOutButton from '../components/SignInOrOutButton';

test('renders "sign in" button', () => {
    const {getByText} = render(<SignInOrOutButton authState="signIn"/>);
    const signInText = getByText(/Sign In With Google/i);
    expect(signInText).toBeInTheDocument();
});

test('renders "loading" while signing in', () => {
    const {getByText} = render(<SignInOrOutButton authState="loading"/>);
    const signInText = getByText(/loading\.\.\./i);
    expect(signInText).toBeInTheDocument();
});

test('renders "sign out" when signed in', () => {
    const {getByText} = render(<SignInOrOutButton authState="signedIn"/>);
    const signInText = getByText(/Se déconnecter/i);
    expect(signInText).toBeInTheDocument();
});
