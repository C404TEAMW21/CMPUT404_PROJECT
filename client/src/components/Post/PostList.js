import React from "react";
import moment from "moment";
import PostComponent from "./PostComponent";

const PostList = ({ posts, handleDeletePost }) => {
  const postList = posts.map((post, index) => {
    const {
      id,
      description,
      title,
      contentType,
      content,
      author,
      published,
      visibility,
    } = post;

    return (
      <PostComponent
        key={id}
        index={index}
        id={id}
        title={title}
        description={description}
        content={content}
        contentType={contentType}
        author={author}
        published={moment(published).format("MMMM Do YYYY, h:mm:ss a")}
        visibility={visibility}
        handleDeletePost={handleDeletePost}
      />
    );
  });

  return <div>{postList}</div>;
};

export default PostList;
