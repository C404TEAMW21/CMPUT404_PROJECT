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
  const [githubActivity, updateGithubActivity] = useState([]);
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
    // TODO also sort Github activity posts by date
    let posts = [...authorPosts, ...inboxPosts, ...githubActivity];

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

  const getAllGithubActivity = async () => {
    if (!context.user.github) {
      return;
    }

    try {
      const response = await axios.get(
        `https://api.github.com/users/${context.user.github}/events?per_page=5&page=1`,
        {
          headers: {
            Authorization: `token ${process.env.REACT_APP_GITHUB_KEY}`,
          },
        }
      );

      const result = [];
      for (let event of response.data) {
        if (event.type === "PushEvent") {
          result.push({
            type: "github",
            eventType: event.type,
            published: event.created_at,
            repo: event.name,
            commits: event.payload.commits,
          });
        } else if (event.type === "PullRequestEvent") {
          result.push({
            type: "github",
            eventType: event.type,
            published: event.created_at,
            repo: event.repo.url,
            action: event.payload.action,
            url: event.payload.pull_request.html_url,
          });
        }
      }

      updateGithubActivity(result);
    } catch {
      updateGithubActivity([
        {
          type: "github",
          error: "Unable to fetch from GitHub. Please check your credentials",
          published: new Date(),
        },
      ]);
    }
  };

  useEffect(() => {
    if (context.user) {
      getAllMyPosts();
      getAllInboxPosts();
      getAllGithubActivity();
    }
  }, []);

  useEffect(() => {
    if (context.user) {
      getMyFeedPosts();
    }
  }, [authorPosts, inboxPosts, githubActivity]);

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
