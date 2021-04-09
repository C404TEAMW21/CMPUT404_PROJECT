import React from "react";
import { Comment, Icon, Label, Button } from "semantic-ui-react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import "./Comments.scss";

const CommentComponent = ({
  author,
  content,
  contentType,
  published,
  commentId,
}) => {
  return (
    <Comment>
      <Comment.Content>
        <Comment.Author as="a">{author.displayName}</Comment.Author>
        <Comment.Metadata>
          <div>{published}</div>
        </Comment.Metadata>
        <Comment.Text>
          <ReactMarkdown plugins={[gfm]} children={content} />
        </Comment.Text>
        <Comment.Actions>
          <Comment.Action>
            <Button as="div" labelPosition="right">
              <Button color="red">
                <Icon name="heart" />
                Like
              </Button>
              <Label as="a" basic color="red" pointing="left">
                0
              </Label>
            </Button>
          </Comment.Action>
        </Comment.Actions>
      </Comment.Content>
    </Comment>
  );
};

export default CommentComponent;
