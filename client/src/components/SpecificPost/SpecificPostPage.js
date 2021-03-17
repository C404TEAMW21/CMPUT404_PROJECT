import React, { useState, useContext, useEffect } from "react";
import { Dimmer, Loader, Message } from "semantic-ui-react";
import { getSpecificAuthorPost } from "../../ApiUtils";
import { Context } from "../../Context";
import PostComponent from "../Post/PostComponent";

const SpecificPostPage = () => {
  const context = useContext(Context);

  const [loading, updateLoading] = useState(true);
  const [error, updateError] = useState(false);
  const [postInfo, updatePostInfo] = useState([]);

  useEffect(() => {
    callGetPost();
  }, []);

  const callGetPost = async () => {
    const response = await getSpecificAuthorPost(
      context.cookie,
      window.location.pathname
    );

    if (response.status === 200) {
      console.log(response.data);
      updatePostInfo([response.data]);
    } else {
      updateError(true);
    }

    updateLoading(false);
  };

  const handleDeletePost = () => {
    // TODO implement so that if successful delete, reroute to public feed otherwise display error
  };

  return (
    <div>
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Loading Post...</Loader>
        </Dimmer>
      )}
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      {postInfo.map((post, index) => {
        return (
          <div id={index}>
            <PostComponent
              id={post.id}
              title={post.id}
              description={post.description}
              content={post.content}
              contentType={post.contentType}
              author={post.author}
              published={post.published}
              visibility={post.visibility}
              handleDeletePost={handleDeletePost}
              showSpecificPostContents={true}
            />
          </div>
        );
      })}
    </div>
  );
};

export default SpecificPostPage;
