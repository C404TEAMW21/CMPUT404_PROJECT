import React, { useEffect, useState, useContext } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { Context } from "../../Context";
import { getAllFollowers, checkIfFollowing } from "../../ApiUtils";

const FriendsList = (props) => {
  const context = useContext(Context);
  const [friends, updateFriends] = useState([]);

  useEffect(() => {
    if (context.user) {
      getFriendsList();
    }
  }, []);

  const getFriendsList = async () => {
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

        if (response.data.items[0].status === true) result.push(item);
      }

      updateFriends(result);
    } else {
      props.updateError(true);
    }
  };

  return (
    <div>
      {friends.map((author) => (
        <FriendFollowerComponent
          username={author.username}
          authorId={author.id}
        />
      ))}
    </div>
  );
};

export default FriendsList;
