import React, { useState, useContext } from "react";
import { Form, Input, Button } from "semantic-ui-react";
import { Context } from "../../Context";
import "./SignupLoginForm.scss";

const SignupLoginForm = (props) => {
  const context = useContext(Context);

  const [username, updateUsername] = useState("");
  const [password, updatePassword] = useState("");
  const [error, setError] = useState(false);
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState();

  const handleChange = (e, { name, value }) => {
    if (name === "username") {
      updateUsername(value);
    } else if (name === "password") {
      updatePassword(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let message = await props.onSubmit(username, password);

    // redirect the user to the myfeed page
    if (message !== null && message.props.to) {
      context.updateCookie(message.props.token);
      setMessage(message);
    }

    if (message !== null && message.props.error == true) {
      setSuccess(false);
      setError(true);
      setMessage(message);
      console.log("error");
    } else if (message !== null && message.props.success == true) {
      setError(false);
      setSuccess(true);
      setMessage(message);
      console.log("success");
    }
  };

  return (
    <Form size="big" success={success} error={error} onSubmit={handleSubmit}>
      {message ? message : <div />}
      <Form.Field>
        <Input
          fluid
          icon="user"
          iconPosition="left"
          placeholder="username"
          name="username"
          type="text"
          value={username}
          onChange={handleChange}
          disabled={success}
        />
      </Form.Field>
      <Form.Field>
        <Input
          fluid
          icon="lock"
          iconPosition="left"
          placeholder="password"
          name="password"
          type="password"
          value={password}
          onChange={handleChange}
          disabled={success}
        />
      </Form.Field>
      <Button fluid type="submit" disabled={success}>
        {props.buttonText}
      </Button>
    </Form>
  );
};

export default SignupLoginForm;
