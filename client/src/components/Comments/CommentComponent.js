import React from "react";
import { Comment, Icon } from "semantic-ui-react";
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
      </Comment.Content>
    </Comment>
  );
};

export default CommentComponent;
