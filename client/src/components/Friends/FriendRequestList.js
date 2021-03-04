import React, { useEffect, useContext, useState } from "react";

import FriendRequestComponent from "./FriendRequestComponent";
import { Context } from "../../Context";
import {
  getAllFollowers,
  checkIfFollowing,
  sendFriendFollowRequest,
} from "../../ApiUtils";

const FriendRequestList = (props) => {
  const context = useContext(Context);
  const [friendRequests, updateFriendRequests] = useState([]);

  useEffect(() => {
    getFollowerList();
  }, []);

  const getFollowerList = async () => {
    const response = await getAllFollowers(context.cookie, context.user.id);

    if (response.status === 200) {
      const result = [];
      for (let item of response.data.items) {
        const response = await checkIfFollowing(
          context.cookie,
          item.id,
          context.user.id
        );

        if (response.status !== 200) {
          props.updateError(true);
          break;
        }

        if (response.data.items[0].status !== true) result.push(item);
      }

      updateFriendRequests(result);
    } else {
      props.updateError(true);
    }
  };

  const handleAccept = async (indexToRemove, authorId) => {
    const response = await sendFriendFollowRequest(
      context.cookie,
      authorId,
      context.user.id
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
        <FriendRequestComponent
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
