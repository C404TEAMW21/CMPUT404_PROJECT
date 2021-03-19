import React, { useContext } from "react";
import { useHistory } from "react-router-dom";
import { Button, Icon } from "semantic-ui-react";
import { PAGE_CREATE_POST } from "../../Constants";
import { Context } from "../../Context";
import "./CreatePostPage.scss";

const PostSuccess = (props) => {
  const context = useContext(Context);
  let history = useHistory();

  const handleCreateClick = () => {
    history.push(PAGE_CREATE_POST);
  };

  const handleViewPostClick = () => {
    history.push(`/author/${context.user.id}/posts/${props.postId}`);
  };

  return (
    <div className="post-success">
      <Icon name="check circle outline" className="check-icon" size="huge" />
      <div className="success-content">
        <h1>Post created successfully!</h1>
        <Button className="success-view-post" onClick={handleViewPostClick}>
          View Post
        </Button>
        <Button className="success-createpost" onClick={handleCreateClick}>
          Create Another Post
        </Button>
      </div>
    </div>
  );
};

export default PostSuccess;
