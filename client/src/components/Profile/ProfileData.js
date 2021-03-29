import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import EditProfileModal from "./EditProfileModal";
import { Context } from "../../Context";
import "./ProfilePage.scss";
import { checkIfFollowing, unFollowAuthor } from "../../ApiUtils";

const MyProfileData = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [name, updateName] = useState("Loading...");
  const [github, updateGithub] = useState("N/A");
  const [host, updateHost] = useState("N/A");
  const [showEditBtn, updateShowEditBtn] = useState(false);
  const [showFriendRequestBtn, updateShowFriendRequestBtn] = useState(false);
  const [showUnFollowBtn, updateShowUnFollowBtn] = useState(false);
  const [loadingFriendRequest, updateLoadingFriendRequest] = useState(false);
  const [loadingUnFollowRequest, updateLoadingUnFollowRequest] = useState(
    false
  );

  useEffect(() => {
    const authorId = window.location.pathname.split("/").pop();
    nameToRender(authorId);
    selectBtnToShow(authorId);
    githubToRender(authorId);
    hostToRender(authorId);
  }, [location, props.author]);

  const selectBtnToShow = async (authorId) => {
    if (!context.user) {
      return;
    }

    if (context.user.id === authorId) {
      updateShowEditBtn(true);
      updateShowFriendRequestBtn(false);
      updateShowUnFollowBtn(false);
      return;
    }

    const response = await checkIfFollowing(
      context.cookie,
      props.author,
      context.user
    );
    if (response.status !== 200 && response.status !== 404) {
      props.updateError(true);
      return;
    }

    if (response.status === 404) {
      updateShowFriendRequestBtn(true);
    } else if (response.data.items.length > 0) {
      const following = response.data.items[0].follower === context.user.id;
      updateShowFriendRequestBtn(!following);
      updateShowUnFollowBtn(following);
    }
  };

  const nameToRender = (authorId) => {
    let result = "Loading...";

    if (context.user) {
      if (authorId !== context.user.id) {
        result = props.author.displayName
          ? props.author.displayName
          : props.author.username;
        updateName(result);
        return;
      }
    }

    if (context.user && context.user.displayName) {
      result = context.user.displayName;
    } else if (context.user && context.user.username) {
      result = context.user.username;
    }

    updateName(result);
  };

  const sendFriendRequest = async () => {
    updateLoadingFriendRequest(true);
    const status = await props.onSendFriendRequestClick();
    if (status) {
      updateShowFriendRequestBtn(false);
      updateShowUnFollowBtn(true);
    }

    updateLoadingFriendRequest(false);
  };

  const handleUnFollow = async () => {
    updateLoadingUnFollowRequest(true);

    const authorId = window.location.pathname.split("/").pop();
    const response = await unFollowAuthor(
      context.cookie,
      authorId,
      context.user.id
    );

    if (response.status !== 200) {
      props.updateError(true);
    }

    updateLoadingUnFollowRequest(false);

    if (response.status === 200) {
      updateShowFriendRequestBtn(true);
      updateShowUnFollowBtn(false);
    }
  };

  const githubToRender = (authorId) => {
    let result = "N/A";

    if (context.user) {
      if (authorId !== context.user.id) {
        result = props.author.github ? props.author.github : "N/A";
      } else {
        result = context.user.github ? context.user.github : "N/A";
      }

      updateGithub(result);
    }
  };

  const hostToRender = (authorId) => {
    let result = "N/A";

    if (context.user) {
      if (authorId !== context.user.id) {
        result = props.author.host ? props.author.host : "N/A";
      } else {
        result = context.user.host ? context.user.host : "N/A";
      }

      updateHost(result);
    }
  };

  return (
    <div>
      <div className="profile-top-section">
        <div className="display-name-heading">
          <Header as="h1" floated="left">
            {name}
          </Header>

          {showEditBtn && <EditProfileModal />}

          {showFriendRequestBtn && (
            <Button
              className="send-friend-request-btn"
              onClick={sendFriendRequest}
              loading={loadingFriendRequest}
            >
              Send Friend Request
            </Button>
          )}

          {showUnFollowBtn && (
            <Button onClick={handleUnFollow} loading={loadingUnFollowRequest}>
              Unfollow Author
            </Button>
          )}
        </div>

        <div className="display-name-heading">
          <Header as="h4" floated="left">
            GitHub:
          </Header>
          <span>{github}</span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Host:
          </Header>
          <span>{host}</span>
        </div>
      </div>
    </div>
  );
};

export default MyProfileData;
