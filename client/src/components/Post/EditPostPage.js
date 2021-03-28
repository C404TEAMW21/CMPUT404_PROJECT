import React, { useState, useContext, useEffect } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { Header, Icon, Message } from "semantic-ui-react";
import { getSpecificAuthorPost, deletePost } from "../../ApiUtils";
import { Context } from "../../Context";
import EditPostForm from "./EditPostForm";
import DeletePostModal from "./DeletePostModal";
import "./PostPage.scss";
import { SERVER_HOST, ROUTE_MY_FEED } from "../../Constants";
import PostSuccess from "./PostSuccess";

const EditPostPage = (props) => {
  const context = useContext(Context);
  const history = useHistory();
  const [error, setError] = useState(false);
  const [postData, setPostData] = useState({});
  const [postId, setPostId] = useState("");
  const [success, updateSuccess] = useState(false);
  const [deletePostFlag, setDeletePostFlag] = useState(false);

  const getPost = async () => {
    let getPostId = window.location.pathname;
    getPostId = getPostId.split("/")[2];

    setPostId(getPostId);

    const path = `/author/${context.user.id}/posts/${getPostId}`;

    const response = await getSpecificAuthorPost(context.cookie, path);

    if (response.status === 200) {
      setPostData(response.data);
    } else {
      setError(true);
    }
  };

  const handleSavePost = async (body) => {
    if (Array.isArray(body.content)) {
      let base64Image = await getBase64(body.content[0]);

      body["content"] = base64Image;
      body["contentType"] = base64Image.split(/[:,]/)[1];
    }

    console.log(body);

    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${context.user.id}/posts/${postId}/`,
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

  const deletePostClick = () => {
    setDeletePostFlag(!deletePostFlag);
  };

  const handleDeletePost = async (currentPostId, index) => {
    const response = await deletePost(
      context.cookie,
      context.user.id,
      currentPostId
    );

    if (response.status === 204) {
      history.push(ROUTE_MY_FEED);
    } else {
      setError(true);
    }
  };

  const postSuccess = () => {
    updateSuccess(true);
  };

  useEffect(() => {
    if (context.user) {
      getPost();
    }
  }, []);

  return (
    <div className="edit-post-page">
      <DeletePostModal
        id={postId}
        index={0}
        open={deletePostFlag}
        setOpen={deletePostClick}
        handleDeletePost={handleDeletePost}
      />
      {success ? (
        <PostSuccess postId={postId} version="edited" />
      ) : (
        <div className="edit-post">
          <Header as="h2">
            <Icon name="pencil" />
            <Header.Content>Edit Post</Header.Content>
          </Header>
          {error ? (
            <Message
              error
              size="large"
              header="Error"
              content="Something happened on our end. Please try again later."
            />
          ) : (
            <EditPostForm
              data={postData}
              handleSavePost={handleSavePost}
              setDeletePost={deletePostClick}
              postSuccess={postSuccess}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default EditPostPage;
