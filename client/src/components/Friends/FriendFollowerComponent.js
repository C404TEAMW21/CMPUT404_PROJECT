import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import { FRIEND_REQUEST_LIST, FRIEND_LIST } from "../../Constants";
import { Context } from "../../Context";
import "./FriendFollower.scss";

const FriendFollowerComponent = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [loading, updateLoading] = useState(true);
  const [showRemoveBtn, updateShowRemoveBtn] = useState(false);
  const [showAcceptBtn, updateShowAcceptBtn] = useState(false);
  const [profileLink, updateProfileLink] = useState("#");

  useEffect(() => {
    updateProfileLink(`/author/${props.authorId}`);
    renderButtons();
    updateLoading(false);
  }, [location, props]);

  const renderButtons = () => {
    if (!context.user) {
      return;
    }

    const authorId = window.location.pathname.split("/").pop();

    if (authorId !== context.user.id) {
      updateShowRemoveBtn(false);
      updateShowAcceptBtn(false);
      return;
    }

    if (props.parent === FRIEND_LIST) {
      updateShowRemoveBtn(true);
      updateShowAcceptBtn(false);
    } else if (props.parent === FRIEND_REQUEST_LIST) {
      updateShowAcceptBtn(true);
      updateShowRemoveBtn(false);
    }
  };

  const handleDelete = () => {
    if (props.parent === FRIEND_LIST) {
      props.handleDeleteFriend(props.index, props.authorId);
    }
  };

  const handleAccept = () => {
    props.handleAccept(props.index, props.author);
  };

  if (loading) {
    return <p>Loading...</p>;
  } else {
    return (
      <div className="friendfollower-container">
        <Header as="a" size="large" href={profileLink} className="userlink">
          {props.displayName}
        </Header>
        <p>{props.host}</p>
        {showRemoveBtn && <Button onClick={handleDelete}>Remove</Button>}
        {showAcceptBtn && (
          <Button className="accept-request-btn" onClick={handleAccept}>
            Accept
          </Button>
        )}
      </div>
    );
  }
};

export default FriendFollowerComponent;
