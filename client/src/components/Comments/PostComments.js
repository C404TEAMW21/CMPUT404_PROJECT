import React, { useState, useEffect } from "react";
import { Comment, Button, Form, Header, Message } from "semantic-ui-react";
import CommentComponent from "./CommentComponent";
import CommentList from "./CommentList";
import { getComments, createComment } from "../../ApiUtils";
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

const PostComments = ({ post, token, currentAuthor }) => {
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(false);

  const onCommentChange = (e, { value }) => {
    setValue(value);
  };

  const addComment = async () => {
    // let response;
    // if (post.origin.includes("team6")) {
    //   //call remote
    // } else {
    //   let postId = post.id.split("/");
    //   postId = postId.slice(-2)[0];
    //   response = await createComment(token, currentAuthor, postId, value);
    //   console.log(response);
    // }
    // console.log(response);
    // if (response && response.status === 200) {
    //   await getPostComments();
    // } else {
    //   setError(true);
    // }
  };

  const getPostComments = async () => {
    if (post[0] && post[0].origin.includes("team6")) {
      //call remote
    } else if (post[0]) {
      let postId = post[0].id.split("/");
      postId = postId.slice(-2)[0];

      const response = await getComments(token, currentAuthor, postId);

      console.log(response);

      if (response && response.status === 200) {
        setComments(response);
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
