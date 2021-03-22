import React, { useEffect, useState } from "react";
import { ReactComponent as GithubLogo } from "../../assets/GitHubLogo.svg";
import { Card } from "semantic-ui-react";
import moment from "moment";
import "./Github.scss";

const GithubComponent = (props) => {
  const [description, updateDescription] = useState("");

  useEffect(() => {
    displayContents();
  }, [props.content]);

  const displayContents = () => {
    let message = <div></div>;
    const {
      eventType,
      repo,
      branch,
      commits,
      action,
      base,
      head,
      url,
      merged,
      title,
    } = props.content;

    if (eventType === "PushEvent") {
      message = (
        <div>
          <p>
            Pushed to
            <b> {branch} </b>
            on
            <b> {repo} </b>
          </p>
          <p>Commits Made:</p>
          <ul>
            {commits.map((commit) => {
              return <li>{commit.message}</li>;
            })}
          </ul>
        </div>
      );
    } else if (eventType === "PullRequestEvent") {
      if (action === "opened") {
        message = (
          <div>
            <p>
              Created a pull request from
              <b> {head} </b>
              to
              <b> {base} </b>
              on
              <b> {repo} </b>
            </p>
            <br />
            <a href={url}>Pull Request Link</a>
          </div>
        );
      } else if (action === "closed") {
        message = (
          <div>
            <p>
              {merged
                ? `Merged pull request from `
                : `Closed pull request from `}
              <b>{head} </b>
              to
              <b> {base} </b>
              on
              <b> {repo} </b>
            </p>
            <br />
            <a href={url}>Pull Request Link</a>
          </div>
        );
      }
    } else if (eventType === "IssuesEvent") {
      message = (
        <div>
          <p>
            {action === "opened"
              ? `Opened a new issue: `
              : `Closed the issue: `}
            <b>{title} </b>
            on <b>{repo}</b>
          </p>
          <br />
          <a href={url}>Issue Link</a>
        </div>
      );
    } else if (eventType === "Error") {
      message = "Unable to fetch from GitHub. Please check your credentials";
    }

    updateDescription(message);
  };

  return (
    <div className="github-card">
      <Card raised fluid centered>
        <Card.Content>
          <div className="logo">
            <GithubLogo />
          </div>

          <div className="github-data">
            <Card.Header>{props.content.eventType}</Card.Header>
            <Card.Meta>
              {moment(props.content.published).format(
                "MMMM Do YYYY, h:mm:ss a"
              )}
            </Card.Meta>
            <Card.Description>{description}</Card.Description>
          </div>
        </Card.Content>
      </Card>
    </div>
  );
};

export default GithubComponent;
