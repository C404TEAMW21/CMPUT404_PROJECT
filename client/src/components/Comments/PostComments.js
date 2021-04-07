import React, { useState } from "react";
import { Comment, Button, Form, Header, Message } from "semantic-ui-react";
import CommentComponent from "./CommentComponent";
import CommentList from "./CommentList";
import "./Comments.scss";

const mockComments = [
  {
    type: "comment",
    author: {
      type: "author",
      id: "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
      url: "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
      host: "http://127.0.0.1:5454/",
      displayName: "Test1",
      github: "http://github.com/test",
    },
    comment: "# testing 1",
    contentType: "text/markdown",
    published: "2015-03-09T13:07:04+00:00",
    id:
      "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
  },
  {
    type: "comment",
    author: {
      type: "author",
      id: "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
      url: "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
      host: "http://127.0.0.1:5454/",
      displayName: "Test2",
      github: "http://github.com/test",
    },
    comment: "testing 2",
    contentType: "text/markdown",
    published: "2015-03-09T13:07:06+00:00",
    id:
      "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
  },
];

const PostComments = () => {
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);

  const onCommentChange = (e, { value }) => {
    setValue(value);
  };

  const addComment = () => {
    console.log("clicked");
  };

  return (
    <div className="comments-section">
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      <Header as="h2" dividing>
        Comments
      </Header>
      <div className="comments-container">
        <Comment.Group className="comments" minimal>
          <CommentList comments={mockComments} />

          <Form className="add-comment">
            <Form.TextArea value={value} onChange={onCommentChange} />
            <Button
              content="Add Comment"
              labelPosition="left"
              icon="comments"
              primary
              onClick={addComment}
            />
          </Form>
        </Comment.Group>
      </div>
    </div>
  );
};

export default PostComments;
