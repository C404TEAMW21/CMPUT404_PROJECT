import React, { useEffect, useContext, useState } from "react";
import { useLocation } from "react-router-dom";

import { Context } from "../../Context";
import {
  getAllFollowers,
  checkIfFollowing,
  sendFriendFollowRequest,
} from "../../ApiUtils";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { FRIEND_REQUEST_LIST } from "../../Constants";

const FriendRequestList = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [friendRequests, updateFriendRequests] = useState([]);

  useEffect(() => {
    getFollowerList();
  }, [location]);

  const getFollowerList = async () => {
    const response = await getAllFollowers(context.cookie, context.user.id);

    if (response.status === 200) {
      const result = [];
      for (let item of response.data.items) {
        const response = await checkIfFollowing(
          context.cookie,
          item,
          context.user
        );

        if (response.status !== 200) {
          props.updateError(true);
          break;
        }

        if (
          response.data.items &&
          response.data.items.length > 0 &&
          response.data.items[0].follower === context.user.id
        )
          result.push(item);
      }

      updateFriendRequests(result);
    } else {
      props.updateError(true);
    }
  };

  const handleAccept = async (indexToRemove, author) => {
    const response = await sendFriendFollowRequest(
      context.cookie,
      author,
      context.user
    );

    if (response.status !== 200) {
      props.updateError(true);
      return;
    }

    updateFriendRequests(
      friendRequests.filter((req, index) => index !== indexToRemove)
    );
  };

  return (
    <div>
      {friendRequests.map((author, index) => (
        <FriendFollowerComponent
          parent={FRIEND_REQUEST_LIST}
          author={author}
          username={author.username}
          authorId={author.id}
          index={index}
          handleAccept={handleAccept}
        />
      ))}
    </div>
  );
};

export default FriendRequestList;
