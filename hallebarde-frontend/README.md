# Hallebarde-frontend

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `configure-environment.sh`
As our website is statically hosted with S3, we must build it with hardcoded configuration (OAuth endpoints, 
API endpoints, etc.). This script gets infrastructure configuration and puts it in `.env` file, which is 
then automatically parsed by React.

It can be called with `./configure-environment.sh [local|dev|prod]`

Call it with `local` to get client credentials valid for `localhost`: best for testing on your 
computer with `npm start` after.

Call it with environment name `dev` before a build for packaging the website with `dev` endpoints, before 
uploading it to static hosting

Call it with environment name `prod` before a build for packaging the website with `prod` endpoints, before 
uploading it to static hosting

This needs you to have effective AWS credentials, as it calls terragrunt to access the terraform outputs

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.


Note that OAuth and domain configuration from the `.env` file is embedded.
The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## File upload flow

```mermaid
graph LR
    UNSELECTED -- Selection   --> SELECTED
    SELECTED   -- Cancel      --> UNSELECTED
    SELECTED   -- Change file --> SELECTED
    SELECTED   -- Upload      --> UPLOADING
    UPLOADING     ==>             FINISH
```
