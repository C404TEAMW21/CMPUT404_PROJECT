import React, { useEffect, useState } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";

const FollowingList = () => {
  const [following, updateFollowing] = useState([
    { username: "Not Yet Implemented" },
  ]);

  useEffect(() => {
    // call get all following list
  }, []);

  return (
    <div>
      {following.map((author) => (
        <FriendFollowerComponent username={author.username} />
      ))}
    </div>
  );
};

export default FollowingList;
