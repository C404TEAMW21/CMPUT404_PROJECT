import React, { useState, useContext, useEffect } from "react";
import { Header, Button } from "semantic-ui-react";
import { useLocation } from "react-router-dom";
import axios from "axios";

import EditProfileModal from "./EditProfileModal";
import { Context } from "../../Context";
import { SERVER_HOST } from "../../Constants";
import "./ProfilePage.scss";

const MyProfileData = (props) => {
  const context = useContext(Context);
  const location = useLocation();
  const [name, updateName] = useState("Loading...");
  const [showEditBtn, updateShowEditBtn] = useState(true);
  const [disableFriendRequestBtn, updateDisableFriendRequestBtn] = useState(
    false
  );
  const [loadingFriendRequest, updateLoadingFriendRequest] = useState(false);

  useEffect(() => {
    const authorId = window.location.pathname.split("/").pop();
    nameToRender(authorId);
    shouldShowEditBtn(authorId);
    shouldDisableFriendRequestBtn(authorId);
  }, [location, props.author]);

  const shouldShowEditBtn = (authorId) => {
    if (context.user) {
      updateShowEditBtn(authorId === context.user.id);
    }
  };

  const shouldDisableFriendRequestBtn = async (authorId) => {
    if (!context.user) {
      return;
    }

    try {
      const response = await axios.get(
        `${SERVER_HOST}/service/author/${authorId}/followers/${context.user.id}/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      updateDisableFriendRequestBtn(response.data.items[0].status === true);
    } catch (error) {
      props.updateError(true);
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
      updateDisableFriendRequestBtn(true);
    }

    updateLoadingFriendRequest(false);
  };

  return (
    <div>
      <div className="profile-top-section">
        <div className="display-name-heading">
          <Header as="h1" floated="left">
            {name}
          </Header>

          {showEditBtn ? (
            <EditProfileModal />
          ) : (
            <Button
              className="send-friend-request-btn"
              onClick={sendFriendRequest}
              disabled={disableFriendRequestBtn}
              loading={loadingFriendRequest}
            >
              Send Friend Request
            </Button>
          )}
        </div>

        <div className="display-name-heading">
          <Header as="h4" floated="left">
            GitHub:
          </Header>
          <span>
            {context.user && context.user.github ? context.user.github : "N/A"}
          </span>
        </div>
      </div>

      <div className="profile-stats-table">
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Posts:
          </Header>
          <span></span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Friends:
          </Header>
          <span></span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Followers:
          </Header>
          <span></span>
        </div>
        <div className="display-name-heading">
          <Header as="h4" floated="left">
            Following:
          </Header>
          <span></span>
        </div>
      </div>
    </div>
  );
};

export default MyProfileData;
