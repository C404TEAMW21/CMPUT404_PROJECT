import React, { useEffect, useState, useContext } from "react";
import { Card, Message, Dimmer, Loader } from "semantic-ui-react";
import moment from "moment";
import axios from "axios";
import PostList from "../Post/PostList";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";

const MyFeedPage = () => {
  const context = useContext(Context);

  const [posts, updatePosts] = useState([]);
  const [authorPosts, updateAuthorPosts] = useState([]);
  const [inboxPosts, updateInboxPosts] = useState([]);
  const [error, updateError] = useState(false);
  const [loading, updateLoading] = useState(true);

  const getAllMyPosts = async () => {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/service/author/${context.user.id}/posts/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      updateAuthorPosts(response.data);
    } catch (error) {
      updateError(true);
    }
  };

  const getAllInboxPosts = async () => {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/service/author/${context.user.id}/inbox/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );
      const posts = response.data.items.filter((item) => {
        return item.type == "post";
      });
      updateInboxPosts(posts);
    } catch (error) {
      updateError(true);
    }
  };

  const getMyFeedPosts = () => {
    let posts = [...authorPosts, ...inboxPosts];

    posts.sort(
      (a, b) => moment(b.published).toDate() - moment(a.published).toDate()
    );

    updatePosts(posts);
    updateLoading(false);
  };

  const handleDeletePost = async (id, index) => {
    let postId = id.split("/");
    postId = postId.slice(-2)[0];

    try {
      const response = await axios.delete(
        `${SERVER_HOST}/service/author/${context.user.id}/posts/${postId}/`,
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
    if (context.user) {
      getAllMyPosts();
      getAllInboxPosts();
    }
  }, []);

  useEffect(() => {
    if (context.user) {
      getMyFeedPosts();
    }
  }, [authorPosts, inboxPosts]);

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

export default MyFeedPage;
