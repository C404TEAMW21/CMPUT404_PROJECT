import React, { useState, useContext, useEffect } from "react";
import { Menu, Segment, Message } from "semantic-ui-react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import "./ProfilePage.scss";
import { Context } from "../../Context";
import ProfileData from "./ProfileData";
import FriendRequestList from "../Friends/FriendRequestList";
import FriendList from "../Friends/FriendList";
import FollowerList from "../Friends/FollowerList";
import FollowingList from "../Friends/FollowingList";
import { getUserObject } from "../../ApiUtils";
import { SERVER_HOST } from "../../Constants";

const recentPosts = "Recent Posts";
const friends = "Friends";
const followers = "Followers";
const following = "Following";
const friendRequests = "Friend Requests";

const MyProfilePage = () => {
  const context = useContext(Context);
  const location = useLocation();

  const [activeItem, updateActiveItem] = useState(friends);
  const [currentSection, updateSection] = useState(<FriendList />);
  const [error, updateError] = useState(false);
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

  const placeholder = (
    <img
      alt="placeholder "
      src="https://react.semantic-ui.com/images/wireframe/paragraph.png"
    />
  );

  const showElement = () => {
    const authorId = window.location.pathname.split("/").pop();
    return authorId === (context.user ? context.user.id : true);
  };

  const onSendFriendRequestClick = async () => {
    const authorId = window.location.pathname.split("/").pop();

    try {
      const response = await axios.put(
        `${SERVER_HOST}/service/author/${authorId}/followers/${context.user.id}/`,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      return true;
    } catch (error) {
      updateError(true);
      return false;
    }
  };

  return (
    <div className="profile-page-container">
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}

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
          <Menu.Item
            name={following}
            active={activeItem === following}
            onClick={handleItemClick}
            section={<FollowingList updateError={updateError} />}
          />
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
  );
};

export default MyProfilePage;
