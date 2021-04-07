import React from "react";
import moment from "moment";
import PostComponent from "./CommentComponent";

const CommentList = ({ comments }) => {
  const commentList = comments.map((comment, index) => {
    return (
      <PostComponent
        key={index}
        author={comment.author}
        content={comment.comment}
        contentType={comment.contentType}
        published={moment(comment.published).format("MMMM Do YYYY, h:mm:ss a")}
      />
    );
  });

  return <div>{commentList}</div>;
};

export default CommentList;
