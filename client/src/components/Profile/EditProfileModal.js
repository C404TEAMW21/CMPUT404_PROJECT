import React, { useState, useContext } from "react";
import { Button, Input, Message, Header, Modal, Form } from "semantic-ui-react";
import { Context } from "../../Context";
import axios from "axios";
import { SERVER_HOST } from "../../Constants";

const EditProfileModal = (props) => {
  const context = useContext(Context);

  const [open, updateOpen] = useState(false);
  const [loading, updateLoading] = useState(false);
  const [currentDisplayName, updateCurrentDisplayName] = useState(
    context.user ? context.user.displayName : "Loading..."
  );
  const [githubUsername, updateGithubUsername] = useState(
    context.user ? context.user.github : "Loading..."
  );
  const [error, updateError] = useState(false);
  const [errorMessage, updateErrorMessage] = useState("");

  const modalOnClose = () => {
    updateError(false);
    updateErrorMessage("");
    updateCurrentDisplayName(context.user.displayName);
    updateGithubUsername(context.user.github);
    updateOpen(false);
  };

  const handleChange = (e, { name, value }) => {
    if (name === "displayName") {
      updateCurrentDisplayName(value);
    } else if (name === "githubUsername") {
      updateGithubUsername(value);
    }
  };

  const validateDisplayName = () => {
    const displayNameLength = currentDisplayName.trim().length;
    return displayNameLength >= 3 || displayNameLength === 0;
  };

  const updateUserProfile = async () => {
    try {
      const response = await axios.put(
        `${SERVER_HOST}/api/author/${context.user.id}/`,
        {
          displayName: currentDisplayName,
          github: githubUsername,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    updateLoading(true);

    if (!validateDisplayName()) {
      updateError(true);
      updateErrorMessage("Display Name must be at least 3 characters or more.");
      updateLoading(false);
      return;
    }

    const updateUserProfileResponse = await updateUserProfile();
    if (updateUserProfileResponse.status === 200) {
      context.updateUser(updateUserProfileResponse.data);
    } else {
      updateError(true);
      updateErrorMessage(
        "Something happened while trying to update your profile. Please try again later."
      );
      updateLoading(false);
      return;
    }
  };

  return (
    <Modal
      onClose={() => modalOnClose()}
      onOpen={() => updateOpen(true)}
      closeIcon
      open={open}
      size="tiny"
      trigger={<Button>Edit</Button>}
    >
      {error && <Message error header="Error" content={errorMessage} />}
      <Modal.Content className="modal-content-wrapper">
        <Form size="large" error={error} className="edit-profile-form">
          <Header as="h3">Display Name</Header>
          <Form.Field>
            <Input
              fluid
              placeholder="Display Name"
              name="displayName"
              type="text"
              value={currentDisplayName}
              onChange={handleChange}
            />
          </Form.Field>
          <Header as="h3">GitHub Username</Header>
          <Form.Field>
            <Input
              fluid
              placeholder="Github Username"
              name="githubUsername"
              type="text"
              value={githubUsername}
              onChange={handleChange}
            />
          </Form.Field>
          <Button
            fluid
            type="submit"
            loading={loading}
            onClick={handleSubmit}
            className="edit-profile-save-btn"
          >
            Save
          </Button>
        </Form>
      </Modal.Content>
    </Modal>
  );
};

export default EditProfileModal;
