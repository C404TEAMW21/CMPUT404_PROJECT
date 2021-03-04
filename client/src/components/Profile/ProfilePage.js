import React, { useState, useContext, useEffect } from "react";
import { Menu, Segment, Message } from "semantic-ui-react";
import { useLocation } from "react-router-dom";

import "./ProfilePage.scss";
import { Context } from "../../Context";
import ProfileData from "./ProfileData";
import FriendRequestList from "../Friends/FriendRequestList";
import FriendList from "../Friends/FriendList";
import FollowerList from "../Friends/FollowerList";
import FollowingList from "../Friends/FollowingList";
import { getUserObject, sendFriendFollowRequest } from "../../ApiUtils";

const recentPosts = "Recent Posts";
const friends = "Friends";
const followers = "Followers";
const following = "Following";
const friendRequests = "Friend Requests";

const MyProfilePage = () => {
  const placeholder = (
    <img
      alt="placeholder "
      src="https://react.semantic-ui.com/images/wireframe/paragraph.png"
    />
  );

  const context = useContext(Context);
  const location = useLocation();

  const [activeItem, updateActiveItem] = useState(recentPosts);
  const [error, updateError] = useState(false);
  const [currentSection, updateSection] = useState(placeholder);
  const [currentAuthor, updateCurrentAuthor] = useState({});

  useEffect(() => {
    const authorId = window.location.pathname.split("/").pop();
    getOtherAuthorObject(authorId);
  }, [location]);

  const handleItemClick = (e, { name, section }) => {
    updateActiveItem(name);
    updateSection(section);
  };

  const getOtherAuthorObject = async (authorId) => {
    if (context.user) {
      if (authorId === context.user.id) return;
    }

    try {
      const response = await getUserObject(context.cookie, authorId);
      updateCurrentAuthor(response.data);
    } catch (error) {
      updateError(true);
    }
  };

  const showElement = () => {
    const authorId = window.location.pathname.split("/").pop();
    return authorId === (context.user ? context.user.id : true);
  };

  const onSendFriendRequestClick = async () => {
    const authorId = window.location.pathname.split("/").pop();

    const response = await sendFriendFollowRequest(
      context.cookie,
      authorId,
      context.user.id
    );

    if (response.status !== 200) {
      updateError(true);
      return false;
    }
    return true;
  };

  return (
    <div>
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      <div className="profile-page-container">
        <div className="profile-data">
          <ProfileData
            author={currentAuthor}
            onSendFriendRequestClick={onSendFriendRequestClick}
            updateError={updateError}
          />
        </div>

        <div className="profile-posts">
          <Menu attached="top" tabular>
            <Menu.Item
              name={recentPosts}
              active={activeItem === recentPosts}
              onClick={handleItemClick}
              section={placeholder}
            />
            <Menu.Item
              name={friends}
              active={activeItem === friends}
              onClick={handleItemClick}
              section={<FriendList updateError={updateError} />}
            />
            <Menu.Item
              name={followers}
              active={activeItem === followers}
              onClick={handleItemClick}
              section={<FollowerList updateError={updateError} />}
            />
            {/* Save following list for future sprint */}
            {false && (
              <Menu.Item
                name={following}
                active={activeItem === following}
                onClick={handleItemClick}
                section={<FollowingList updateError={updateError} />}
              />
            )}
            {showElement() && (
              <Menu.Item
                name={friendRequests}
                active={activeItem === friendRequests}
                onClick={handleItemClick}
                section={<FriendRequestList updateError={updateError} />}
              />
            )}
          </Menu>

          <Segment attached="bottom">{currentSection}</Segment>
        </div>
      </div>
    </div>
  );
};

export default MyProfilePage;
