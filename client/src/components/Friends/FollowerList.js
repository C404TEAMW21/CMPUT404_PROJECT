import React, { useEffect, useState, useContext } from "react";
import { Message } from "semantic-ui-react";
import axios from "axios";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";

const FollowerList = (props) => {
  const context = useContext(Context);
  const [followers, updateFollowers] = useState([]);

  const getAllFollowers = async () => {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/service/author/${context.user.id}/followers/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${context.cookie}`,
          },
        }
      );

      updateFollowers(response.data.items);
    } catch (error) {
      props.updateError(true);
    }
  };

  useEffect(() => {
    if (context.user) {
      getAllFollowers();
    }
  }, []);

  return (
    <div>
      {followers.map((author) => (
        <FriendFollowerComponent
          username={author.username}
          authorId={author.id}
        />
      ))}
    </div>
  );
};

export default FollowerList;
