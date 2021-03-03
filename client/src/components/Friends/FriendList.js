import React, { useEffect, useState } from "react";
import FriendFollowerComponent from "./FriendFollowerComponent";

const FriendsList = () => {
  const [friends, updateFriends] = useState([]);

  useEffect(() => {
    // call get all followers list
  }, []);

  return (
    <div>
      {friends.map((author) => (
        <FriendFollowerComponent username={author.username} />
      ))}
    </div>
  );
};

export default FriendsList;
