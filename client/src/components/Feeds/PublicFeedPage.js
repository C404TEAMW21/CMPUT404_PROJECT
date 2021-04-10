import React, { useEffect, useState, useContext } from "react";
import { Card, Message, Dimmer, Loader } from "semantic-ui-react";
import axios from "axios";
import PostList from "../Post/PostList";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";

const PublicFeedPage = () => {
  const [posts, updatePosts] = useState([]);
  const [error, updateError] = useState(false);
  const [loading, updateLoading] = useState(true);
  const context = useContext(Context);

  const getAllPublicPosts = async () => {
    try {
      const response = await axios.get(`${SERVER_HOST}/api/public/`);
      updatePosts(response.data);
    } catch (error) {
      updateError(true);
    }
    updateLoading(false);
  };

  const handleDeletePost = async (id, index) => {
    try {
      const response = await axios.delete(
        `${SERVER_HOST}/api/author/${context.user.id}/posts/${id}/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      let postsTemp = [...posts];
      const removedPosts = postsTemp.filter((post, i) => {
        return i !== index;
      });
      updatePosts(removedPosts);
    } catch (error) {
      updateError(true);
    }
  };

  useEffect(() => {
    getAllPublicPosts();
  }, []);

  return (
    <div>
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Loading Posts...</Loader>
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
      <Card.Group centered itemsPerRow={1}>
        <PostList posts={posts} handleDeletePost={handleDeletePost} />
      </Card.Group>
    </div>
  );
};

export default PublicFeedPage;
