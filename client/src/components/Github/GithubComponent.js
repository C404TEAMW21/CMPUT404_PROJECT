import React, { useState } from "react";
import { ReactComponent as GithubLogo } from "../../assets/GitHubLogo.svg";
import { Card, Icon, Image, Button, Label, Dropdown } from "semantic-ui-react";
import axios from "axios";
import moment from "moment";
import "./Github.scss";

const GithubComponent = (props) => {
  return (
    <div className="custom-card">
      <Card raised fluid centered>
        <Card.Content>
          <GithubLogo />
          <Card.Header>{props.content.eventType}</Card.Header>
          <Card.Meta>
            {moment(props.content.published).format("MMMM Do YYYY, h:mm:ss a")}
          </Card.Meta>
          <Card.Description>TODO</Card.Description>
        </Card.Content>
      </Card>
    </div>
  );
};

export default GithubComponent;
