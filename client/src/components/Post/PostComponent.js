import React, { useContext, useState } from "react";
import { Card, Icon, Image, Button, Label } from "semantic-ui-react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import "./PostComponent.scss";
import { Context } from "../../Context";
import DeletePostModal from "./DeletePostModal";

const markdownType = "text/markdown";
const plainTextType = "text/plain";

const defaultProps = {
  title: "Test Title",
  description: "Some Description",
  content: "Some Content",
  contentType: "text/plain",
  author: { displayName: "John Appleseed", id: "1" },
  published: "2021-02-18T07:21:52.915800Z",
  visibility: "PUBLIC",
};

const PostComponent = (props) => {
  const context = useContext(Context);
  const [deletePost, setDeletePost] = useState(false);

  const passedValues = { ...defaultProps, ...props };
  const {
    id,
    title,
    description,
    content,
    contentType,
    author,
    published,
    visibility,
  } = passedValues;

  const renderContent = () => {
    if (contentType.includes("image")) {
      return <Image src={content} size="medium" />;
    } else if (contentType === markdownType) {
      return <ReactMarkdown plugins={[gfm]} children={content} />;
    } else if (contentType === plainTextType) {
      return <p>{content}</p>;
    }
  };

  const deletePostClick = () => {
    setDeletePost(!deletePost);
  };

  return (
    <div className="custom-card">
      <DeletePostModal
        id={id}
        index={props.index}
        open={deletePost}
        setOpen={deletePostClick}
        handleDeletePost={props.handleDeletePost}
      />
      <Card fluid raised centered>
        <Card.Content>
          <Button basic color="black" floated="right" icon="share alternate" />
          {author.id === context.user.id && (
            <Button
              basic
              color="black"
              floated="right"
              icon="trash alternate"
              onClick={deletePostClick}
            />
          )}
          {author.id === context.user.id && (
            <Button basic color="black" floated="right" icon="pencil" />
          )}
          <Card.Header>{title}</Card.Header>
          <Card.Meta>
            <div>
              <Icon name="eye" />
              <span>
                {visibility.charAt(0) + visibility.substring(1).toLowerCase()}
              </span>
            </div>
            <div>
              <span className="date">
                Posted by{" "}
                <a href={`/author/${author.id}`}>
                  {author.displayName || author.username}
                </a>{" "}
                on {published}
              </span>
            </div>
          </Card.Meta>
          <Card.Description>{description}</Card.Description>
        </Card.Content>
        <Card.Content>
          <Card.Description>{renderContent()}</Card.Description>
        </Card.Content>
        <Card.Content extra>
          <Button as="div" labelPosition="right">
            <Button color="red">
              <Icon name="heart" />
              Like
            </Button>
            <Label as="a" basic color="red" pointing="left">
              0
            </Label>
          </Button>
          <Button as="div" labelPosition="left">
            <Button color="blue" floated="right">
              <Icon name="comments" />
              Comment
            </Button>
            <Label as="a" basic color="blue" pointing="left">
              0
            </Label>
          </Button>
        </Card.Content>
      </Card>
    </div>
  );
};

export default PostComponent;
