import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import { FOLLOWER_LIST } from "../../Constants";
import { Context } from "../../Context";
import "./FriendFollower.scss";

const FriendFollowerComponent = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [loading, updateLoading] = useState(true);
  const [showRemoveBtn, updateShowRemoveBtn] = useState(false);
  const [profileLink, updateProfileLink] = useState("#");

  useEffect(() => {
    updateProfileLink(`/author/${props.authorId}`);

    const authorId = window.location.pathname.split("/").pop();
    if (context.user) {
      updateShowRemoveBtn(authorId === context.user.id);
    }
    updateLoading(false);
  }, [location, props]);

  const handleDelete = () => {
    if (props.parent === FOLLOWER_LIST) {
      // TODO implement
      props.handleDeleteFollower(props.authorId);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  } else {
    return (
      <div className="friendfollower-container">
        <Header as="a" size="large" href={profileLink} className="userlink">
          {props.username}
        </Header>

        {showRemoveBtn && <Button onClick={handleDelete}>Remove</Button>}
      </div>
    );
  }
};

export default FriendFollowerComponent;
