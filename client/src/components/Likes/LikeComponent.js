import React from "react";
import { Card } from "semantic-ui-react";
import { useHistory } from "react-router-dom";
import "./Likes.scss";

const LikeComponent = (props) => {
  let history = useHistory();

  const renderLabel = () => {
    if (props.contents && props.contents.object) {
      if (props.contents.object.includes("comment")) {
        return `Like on Comment by ${props.contents.author.displayName}`;
      } else {
        return `Like on Post by ${props.contents.author.displayName}`;
      }
    }
  };

  const goToPost = () => {
    let url;
    let path;

    if (props.contents.object.includes("team6")) {
      url = new URL(props.contents.object);
      path = url.pathname.split("/").slice(2, 6).join("/");
      history.push(`/${path}`);
    } else {
      if (props.contents.object.includes("api")) {
        url = new URL(props.contents.object);
        path = url.pathname.split("/").slice(2, 6).join("/");
      } else {
        url = new URL(props.contents.object);
        path = url.pathname.split("/").slice(1, 6).join("/");
      }
    }

    history.push(`/${path}`);
  };

  return (
    <div className="custom-like-card">
      <Card raised centered>
        <Card.Content>
          <Card.Header>{renderLabel()}</Card.Header>
          <Card.Description>
            <a onClick={goToPost}>Link To Liked Object</a>
          </Card.Description>
        </Card.Content>
      </Card>
    </div>
  );
};

export default LikeComponent;
