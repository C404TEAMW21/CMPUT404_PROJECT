import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import { Context } from "../../Context";
import "./FriendFollower.scss";

const FriendFollowerComponent = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [loading, updateLoading] = useState(true);
  const [showRemoveBtn, updateShowRemoveBtn] = useState(false);
  const [profileLink, updateProfileLink] = useState("#");

  useEffect(() => {
    const authorId = window.location.pathname.split("/").pop();

    if (context.user) {
      updateShowRemoveBtn(authorId === context.user.id);
      updateProfileLink(`/author/${props.authorId}`);
    }
    updateLoading(false);
  }, [location]);

  const handleDelete = () => {
    // call props function depending if parent is FriendList, FollowerList, FollowingList
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
