import React, { useState, useEffect } from "react";
import { Comment, Button, Form, Header, Message } from "semantic-ui-react";
import CommentList from "./CommentList";
import { getComments, createComment } from "../../ApiUtils";
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
      //call remote
    } else if (post[0]) {
      let postId = post[0].id.split("/");
      postId = postId.slice(-2)[0];
      const response = await createComment(token, currentAuthor, postId, value);

      if (response && response.status === 201) {
        setNoComments(false);
        await getPostComments();
        updateCommentCount();
      } else {
        setError(true);
      }
    }

    setValue("");
    setLoading(false);
  };

  const getPostComments = async () => {
    if (post[0] && post[0].origin.includes("team6")) {
      //call remote
    } else if (post[0]) {
      let postId = post[0].id.split("/");
      postId = postId.slice(-2)[0];

      const response = await getComments(token, currentAuthor, postId);

      if (response && response.status === 200) {
        setComments(response.data);

        if (response.data.length === 0) setNoComments(true);
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
          <CommentList comments={comments} setError={setError} />
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
