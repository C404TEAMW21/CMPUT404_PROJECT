import React, { useEffect, useState, useContext } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { useLocation } from "react-router-dom";
import { FOLLOWER_LIST } from "../../Constants";
import { Context } from "../../Context";
import { getAllFollowers } from "../../ApiUtils";

const FollowerList = (props) => {
  const context = useContext(Context);
  const location = useLocation();

  const [followers, updateFollowers] = useState([]);

  const getFollowers = async () => {
    const authorId = window.location.pathname.split("/").pop();
    let idToUse = context.user.id;
    if (authorId !== context.user.id) {
      idToUse = authorId;
    }

    const response = await getAllFollowers(context.cookie, idToUse);
    if (response.status !== 200) {
      props.updateError(true);
      return;
    }

    updateFollowers(response.data.items);
  };

  useEffect(() => {
    if (context.user) {
      getFollowers();
    }
  }, [location]);

  return (
    <div>
      {followers.map((author) => (
        <FriendFollowerComponent
          parent={FOLLOWER_LIST}
          username={author.username}
          authorId={author.id}
        />
      ))}
    </div>
  );
};

export default FollowerList;
