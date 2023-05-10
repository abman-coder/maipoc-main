import './App.css';
// import InputForm from './components/inputForm';
import { MsalProvider } from "@azure/msal-react";
import MainPage from './MainPage'
import { Container } from "semantic-ui-react";

import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
  useAccount,
} from "@azure/msal-react";
import { Routes, Route, BrowserRouter } from "react-router-dom";

function App({ instance }) {

  const Secureroute = ({ component: Component, ...rest }) => {
    return (
      <>
        <AuthenticatedTemplate>
          <Component {...rest} />
        </AuthenticatedTemplate>

        <UnauthenticatedTemplate>
          Please Login To Continue
        </UnauthenticatedTemplate>
      </>
    );
  };

  return (

    <MsalProvider instance={instance}>
      {/* <Container style={{ paddingTop: "0.5em" }}> */}
      <div id="loader"></div>

      <BrowserRouter
        getUserConfirmation={(message, callback) => {
          // this is the default behavior
          const allowTransition = window.confirm(message);
          callback(allowTransition);
        }}
      >

        <Routes>
          <Route path="/" exact element={<MainPage />} />
          <Route path="/home" exact element={<Secureroute component={MainPage} instance={instance} />} />

        </Routes>
      </BrowserRouter>
      {/* </Container> */}
    </MsalProvider>
  );
}

export default App;
