import React from "react";
import { Card } from "semantic-ui-react";
import "./Likes.scss";

const LikeComponent = (props) => {
  return (
    <div className="custom-like-card">
      <Card raised centered>
        <Card.Content>
          <Card.Header>Like by {props.contents.author.displayName}</Card.Header>
          <Card.Description>
            <a href={props.contents.object}>Link To Liked Object</a>
          </Card.Description>
        </Card.Content>
      </Card>
    </div>
  );
};

export default LikeComponent;
