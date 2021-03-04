import React, { useState, useContext } from "react";
import { Link, Redirect } from "react-router-dom";
import { Message, Dimmer, Loader } from "semantic-ui-react";
import axios from "axios";
import "./SignupLoginPage.scss";
import SignupLoginForm from "./SignupLoginForm";
import { ReactComponent as AppName } from "../../assets/AppName.svg";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";
import { getCurrentUserObject } from "../../ApiUtils";
import { ROUTE_MY_FEED, ROUTE_SIGNUP } from "../../Constants";

const LoginPage = (props) => {
  const [loading, updateLoading] = useState(false);
  const context = useContext(Context);

  const onSubmit = async (username, password) => {
    username = username.trim();

    if (!validate(username, password)) {
      return (
        <Message
          error
          size="tiny"
          header="Insufficient username or password length"
          list={[
            "Usernames must be 3 characters or more",
            "Passwords must be 5 characters or more",
          ]}
        />
      );
    }

    updateLoading(true);

    const response = await signinRequest(username, password);
    const { status } = response;
    const { token } = response.data;

    if (status !== 200) {
      updateLoading(false);
    }

    if (status === 401) {
      return (
        <Message
          error
          size="tiny"
          header="Account Not Approved"
          content="Please wait for admin approval to login."
        />
      );
    } else if (status === 400) {
      return (
        <Message
          error
          size="tiny"
          header="Invalid Username or Password"
          content="Please check if your username or password is correct."
        />
      );
    } else if (status === 200) {
      // save cookie and redirect user to the myfeed page
      const getAuthorResponse = await getCurrentUserObject(token);

      updateLoading(false);
      const getAuthorStatus = getAuthorResponse.status;
      const userData = getAuthorResponse.data;

      if (getAuthorStatus !== 200) {
        return (
          <Message
            error
            size="tiny"
            header="Error"
            content="Please try again."
          />
        );
      }

      context.updateUser(userData);
      return <Redirect to={ROUTE_MY_FEED} token={token} />;
    } else {
      return (
        <Message error size="tiny" header="Error" content="Please try again." />
      );
    }
  };

  const validate = (username, password) => {
    if (username.length >= 3 && password.length >= 5) {
      return true;
    }

    return false;
  };

  const signinRequest = async (username, password) => {
    const request = {
      username,
      password,
    };

    try {
      const response = await axios.post(
        `${SERVER_HOST}/service/author/auth/`,
        request
      );
      return response;
    } catch (error) {
      return error.response;
    }
  };

  return (
    <div className="page">
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Logging In...</Loader>
        </Dimmer>
      )}
      <AppName className="app-name" />
      <h2 className="title">LOGIN</h2>
      <SignupLoginForm onSubmit={onSubmit} buttonText="Login" />
      <div className="link-container">
        <p className="link-info">Don't have an account?</p>
        <Link to={ROUTE_SIGNUP}>Sign up</Link>
      </div>
    </div>
  );
};

export default LoginPage;
