import React from "react";
import { Link } from "react-router-dom";
import { Message } from "semantic-ui-react";
import axios from "axios";
import "./SignupLoginPage.scss";
import SignupLoginForm from "./SignupLoginForm";
import { ReactComponent as AppName } from "../../assets/AppName.svg";
import { SERVER_HOST, ROUTE_LOGIN } from "../../Constants";

const SignupPage = () => {
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

    const response = await signupRequest(username, password);

    if (response === 201) {
      return (
        <Message
          success
          size="tiny"
          header="Account Registered"
          content="Please wait for admin approval to login."
        />
      );
    } else if (response === 400) {
      return (
        <Message
          error
          size="tiny"
          header="Username in use"
          content="Please try a different username."
        />
      );
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

  const signupRequest = async (username, password) => {
    const request = {
      username,
      password,
    };

    try {
      const response = await axios.post(
        `${SERVER_HOST}/service/author/create/`,
        request
      );
      return response.status;
    } catch (error) {
      return error.response.status;
    }
  };

  return (
    <div className="page">
      <AppName className="app-name" />
      <h2 className="signuplogin-title">SIGNUP</h2>
      <SignupLoginForm onSubmit={onSubmit} buttonText="Sign up" />
      <div className="link-container">
        <p className="link-info">Already have an account?</p>
        <Link to={ROUTE_LOGIN}>Login</Link>
      </div>
    </div>
  );
};

export default SignupPage;
