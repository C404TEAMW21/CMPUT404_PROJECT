import React, { useEffect, useState } from "react";
import { Header, Button } from "semantic-ui-react";
import "./FriendFollower.scss";

const FriendRequestComponent = (props) => {
  const [profileLink, updateProfileLink] = useState("#");

  useEffect(() => {
    updateProfileLink(`/author/${props.authorId}`);
  }, [props]);

  const handleAccept = () => {
    props.handleAccept(props.index, props.authorId);
  };

  const handleDecline = () => {};

  return (
    <div className="friendrequest-container">
      <Header as="a" size="large" href={profileLink} className="userlink">
        {props.username}
      </Header>

      <div className="test">
        <Button onClick={handleDecline}>Decline</Button>
        <Button className="accept-request-btn" onClick={handleAccept}>
          Accept
        </Button>
      </div>
    </div>
  );
};

export default FriendRequestComponent;
