import React, { useEffect, useState, useContext } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { Context } from "../../Context";
import {
  getAllFollowers,
  checkIfFollowing,
  unFollowAuthor,
  getAllFriends,
} from "../../ApiUtils";
import { FRIEND_LIST } from "../../Constants";

const FriendsList = (props) => {
  const context = useContext(Context);
  const [friends, updateFriends] = useState([]);

  useEffect(() => {
    if (context.user) {
      getFriendsList();
    }
  }, []);

  const getFriendsList = async () => {
    const authorId = window.location.pathname.split("/").pop();

    let id = context.user.id;
    if (authorId !== context.user.id) {
      id = authorId;
    }
    const response = await getAllFriends(context.cookie, id);

    if (response.status === 200) {
      updateFriends(response.data.friends);
    } else {
      props.updateError(true);
    }
  };

  const handleDeleteFriend = async (indexToDelete, authorId) => {
    const response = await unFollowAuthor(
      context.cookie,
      authorId,
      context.user.id
    );

    if (response.status !== 200) {
      props.updateError(true);
      return;
    }

    updateFriends(friends.filter((follower, index) => index !== indexToDelete));
  };

  return (
    <div>
      {friends.map((author, index) => (
        <FriendFollowerComponent
          parent={FRIEND_LIST}
          username={author.username}
          authorId={author.id}
          handleDeleteFriend={handleDeleteFriend}
          index={index}
        />
      ))}
    </div>
  );
};

export default FriendsList;
