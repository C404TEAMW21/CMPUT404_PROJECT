import React, { useEffect, useState, useContext } from "react";
import { Card, Message, Dimmer, Loader } from "semantic-ui-react";
import LikeComponent from "../Likes/LikeComponent";
import moment from "moment";
import axios from "axios";
import PostList from "../Post/PostList";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";
import "./MyFeed.scss";

const MyFeedPage = () => {
  const context = useContext(Context);

  const [posts, updatePosts] = useState([]);
  const [authorPosts, updateAuthorPosts] = useState([]);
  const [inboxPosts, updateInboxPosts] = useState([]);
  const [githubActivity, updateGithubActivity] = useState([]);
  const [likes, updateLikes] = useState([]);
  const [error, updateError] = useState(false);
  const [loading, updateLoading] = useState(true);

  const getAllMyPosts = async () => {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/api/author/${context.user.id}/posts/`,
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
        `${SERVER_HOST}/api/author/${context.user.id}/inbox/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );
      const posts = response.data.items.filter((item) => {
        return item.type === "post";
      });

      const inboxLikes = response.data.items.filter((item) => {
        return item.type === "like";
      });

      updateLikes(inboxLikes);
      updateInboxPosts(posts);
    } catch (error) {
      updateError(true);
    }
  };

  const getMyFeedPosts = () => {
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
        `${SERVER_HOST}/api/author/${context.user.id}/posts/${postId}/`,
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
            repo: event.repo.name,
            commits: event.payload.commits,
            branch: event.payload.ref.split("/").splice(2).join("/"),
          });
        } else if (event.type === "PullRequestEvent") {
          result.push({
            type: "github",
            eventType: event.type,
            published: event.created_at,
            repo: event.repo.name,
            action: event.payload.action,
            url: event.payload.pull_request.html_url,
            base: event.payload.pull_request.base.label,
            head: event.payload.pull_request.head.label,
            merged: event.payload.pull_request.merged,
          });
        } else if (
          event.type === "IssuesEvent" &&
          (event.payload.action === "opened" ||
            event.payload.action === "closed")
        ) {
          result.push({
            type: "github",
            eventType: event.type,
            published: event.created_at,
            repo: event.repo.name,
            action: event.payload.action,
            url: event.payload.issue.html_url,
            title: event.payload.issue.title,
          });
        }
      }

      updateGithubActivity(result);
    } catch {
      updateGithubActivity([
        {
          type: "github",
          eventType: "Error",
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
      <div className="cardGroupContainer">
        <Card.Group centered itemsPerRow={1}>
          <PostList posts={posts} handleDeletePost={handleDeletePost} />
        </Card.Group>
        <Card.Group centered itemsPerRow={1}>
          {likes.map((individualLike, index) => {
            return (
              <div key={index}>
                <LikeComponent contents={individualLike} />
              </div>
            );
          })}
        </Card.Group>
      </div>
    </div>
  );
};

export default MyFeedPage;
