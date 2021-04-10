import React from "react";
import moment from "moment";
import PostComponent from "./PostComponent";
import GithubComponent from "../Github/GithubComponent";

const PostList = ({ posts, handleDeletePost }) => {
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
      />
    );
  });

  return <div>{postList}</div>;
};

export default PostList;
