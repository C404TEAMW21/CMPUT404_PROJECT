import React from "react";
import moment from "moment";
import CommentComponent from "./CommentComponent";

const CommentList = ({ comments, setError, post }) => {
  const commentList = comments.map((comment, index) => {
    return (
      <CommentComponent
        key={index}
        author={comment.author}
        content={comment.comment}
        contentType={comment.contentType}
        published={moment(comment.published).format("MMMM Do YYYY, h:mm:ss a")}
        commentId={comment.id}
        setError={setError}
        post={post}
      />
    );
  });

  return <div>{commentList}</div>;
};

export default CommentList;
