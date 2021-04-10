import React, { useState, useEffect } from "react";
import { Comment, Button, Form, Header, Message } from "semantic-ui-react";
import CommentList from "./CommentList";
import {
  getComments,
  getRemoteComments,
  createComment,
  createRemoteComment,
} from "../../ApiUtils";
import "./Comments.scss";

const PostComments = ({ post, token, currentAuthor, updateCommentCount }) => {
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);
  const [comments, setComments] = useState([]);
  const [noComments, setNoComments] = useState(false);
  const [loading, setLoading] = useState(false);

  const onCommentChange = (e, { value }) => {
    setValue(value);
  };

  const addComment = async () => {
    setLoading(true);
    if (post[0].origin.includes("team6")) {
      let postId = post[0].id.split("/").pop();
      let postAuthor = post[0].author;

      const response = await createRemoteComment(
        token,
        currentAuthor,
        postAuthor,
        postId,
        value
      );

      if (response && response.status === 201) {
        setNoComments(false);
        await getPostComments();
        updateCommentCount(comments.length + 1);
      } else {
        setError(true);
      }
    } else if (post[0]) {
      let postId = post[0].id;
      let postAuthor = post[0].author;
      const response = await createComment(
        token,
        currentAuthor,
        postAuthor,
        postId,
        value
      );

      if (response && response.status === 201) {
        setNoComments(false);
        await getPostComments();
        updateCommentCount(comments.length + 1);
      } else {
        setError(true);
      }
    }

    setValue("");
    setLoading(false);
  };

  const getPostComments = async () => {
    if (post[0] && post[0].origin.includes("team6")) {
      let postId = post[0].id.split("/").pop();
      let postAuthor = post[0].author;

      const response = await getRemoteComments(token, postAuthor, postId);

      if (response && response.status === 200) {
        setComments(response.data);

        if (response.data.length === 0) setNoComments(true);
        else updateCommentCount(response.data.length);
      } else {
        setError(true);
      }
    } else if (post[0]) {
      let postId = post[0].id;
      let postAuthor = post[0].author;

      const response = await getComments(token, postAuthor, postId);

      if (response && response.status === 200) {
        setComments(response.data);

        if (response.data.length === 0) setNoComments(true);
        else updateCommentCount(response.data.length);
      } else {
        setError(true);
      }
    }
  };

  useEffect(() => {
    getPostComments();
  }, [post]);

  return (
    <div className="comments-section">
      <Header as="h2" dividing>
        Comments
      </Header>
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      {noComments && <p className="no-comments">No comments</p>}
      <div className="comments-container">
        <Comment.Group className="comments" minimal>
          <CommentList comments={comments} />
          <Form className="add-comment">
            <Form.TextArea
              value={value}
              onChange={onCommentChange}
              disabled={loading}
            />
            <Button
              content="Add Comment"
              labelPosition="left"
              icon="comments"
              primary
              onClick={addComment}
              loading={loading}
            />
          </Form>
        </Comment.Group>
      </div>
    </div>
  );
};

export default PostComments;
