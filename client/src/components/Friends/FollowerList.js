import React, { useEffect, useState, useContext } from "react";
import { Message } from "semantic-ui-react";
import axios from "axios";
import FriendFollowerComponent from "./FriendFollowerComponent";
import { SERVER_HOST } from "../../Constants";
import { Context } from "../../Context";

const FollowerList = () => {
  const context = useContext(Context);
  const [followers, updateFollowers] = useState([]);

  const [error, updateError] = useState(false);

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
      updateError(true);
    }
  };

  useEffect(() => {
    if (context.user) {
      getAllFollowers();
    }
  }, []);

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
      {followers.map((author) => (
        <FriendFollowerComponent username={author.username} />
      ))}
    </div>
  );
};

export default FollowerList;
