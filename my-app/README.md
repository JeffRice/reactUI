# eIQ Mobility Frontend Software Engineer Take-Home Project
![This is a dynamic plot](https://github.com/JeffRice/reactUI/blob/main/my-app/public/dynamicplot.jpg)

## UI Features
### Login 
-[Login.js](https://github.com/JeffRice/reactUI/blob/main/my-app/src/Login.js)
-Login component can post an object to the login endpoint and receive a token, login is not integrated with the rest of the app. 
--no-auth for the following features

### Create new calculations
-[NewCalcForm.js](https://github.com/JeffRice/reactUI/blob/main/my-app/src/NewCalcForm.js)
-A form to create new calculations is above the table
-Validations check after each input against the accepted parameters
-Messages are displayed indicating what is invalid
-The submit button is disabled unless it is a valid submission

### Calculations Table 
-[TableListing.js](https://github.com/JeffRice/reactUI/blob/main/my-app/src/TableListing.js)
-The calculations are displayed in a table, sorted by most recent
-calculations created by the user have a different background color
-each calculation ID links to it's details page
-Every second the values are updated

### Details page
-[SecondPlot.js](https://github.com/JeffRice/reactUI/blob/main/my-app/src/SecondPlot.js)
-The values of the calculation are charted on a plotly graph
-Every second the values are updated 

Also implemented 
-Routing for components, using parameters for details page
-1 working test suite from "Testing-Library". Just a couple of DOM tests to try things out.

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
