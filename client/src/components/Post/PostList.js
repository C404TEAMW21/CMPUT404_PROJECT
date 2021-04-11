import React from "react";
import moment from "moment";
import PostComponent from "./PostComponent";
import GithubComponent from "../Github/GithubComponent";

const PostList = ({ posts, handleDeletePost, commentCount }) => {
  const postList = posts.map((post, index) => {
    const {
      id,
      source,
      origin,
      description,
      title,
      contentType,
      content,
      author,
      published,
      visibility,
      count,
    } = post;

    if (post.type === "github") {
      return <GithubComponent content={post} />;
    }

    return (
      <PostComponent
        key={id}
        index={index}
        id={id}
        source={source}
        origin={origin}
        title={title}
        description={description}
        content={content}
        contentType={contentType}
        author={author}
        published={moment(published).format("MMMM Do YYYY, h:mm:ss a")}
        visibility={visibility}
        handleDeletePost={handleDeletePost}
        commentCount={commentCount === false ? count : commentCount}
      />
    );
  });

  return <div>{postList}</div>;
};

export default PostList;
