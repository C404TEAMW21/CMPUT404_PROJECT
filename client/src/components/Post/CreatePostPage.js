import React, { useContext, useState } from "react";
import axios from "axios";
import { Header, Icon } from "semantic-ui-react";
import CreatePostForm from "./CreatePostForm";
import PostSuccess from "./PostSuccess";
import { Context } from "../../Context";
import { SERVER_HOST } from "../../Constants";

import "./CreatePostPage.scss";

const CreatePostPage = (props) => {
  const context = useContext(Context);
  const [success, updateSuccess] = useState(false);

  const onSubmit = async (body) => {
    if (Array.isArray(body.content)) {
      let base64Image = await getBase64(body.content[0]);

      body["content"] = base64Image;
      body["contentType"] = base64Image.split(/[:,]/)[1];
    }

    try {
      const response = await axios.post(
        `${SERVER_HOST}/service/author/${context.user.id}/posts/`,
        body,
        {
          headers: {
            Authorization: `Token ${context.cookie}`,
            "Content-Type": "application/json",
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  };

  const getBase64 = async (file) => {
    return new Promise((resolve, reject) => {
      let reader = new FileReader();

      reader.onload = () => {
        resolve(reader.result);
      };

      reader.onerror = reject;

      reader.readAsDataURL(file);
    });
  };

  const postSuccess = () => {
    updateSuccess(true);
  };

  return (
    <div className="create-post-page">
      {success ? (
        <PostSuccess />
      ) : (
        <div className="create-post-form-page">
          <Header as="h2">
            <Icon name="edit" />
            <Header.Content>Create Post</Header.Content>
          </Header>
          <CreatePostForm submit={onSubmit} postSuccess={postSuccess} />
        </div>
      )}
    </div>
  );
};

export default CreatePostPage;
