import React, { useEffect, useContext, useState } from "react";
import { Context } from "../../Context";
import { likedByAuthor } from "../../ApiUtils";
import LikeComponent from "../Likes/LikeComponent";

const LikedByAuthor = (props) => {
  const context = useContext(Context);
  const [likes, updateLikes] = useState([]);

  useEffect(() => {
    if (context.user) {
      getLikedByAuthor();
    }
  }, []);

  const getLikedByAuthor = async () => {
    try {
      const response = await likedByAuthor(context.cookie, context.user);
      updateLikes(response.data.items);
    } catch (err) {
      props.updateError(err);
    }
  };

  return (
    <div>
      {likes.map((like, index) => {
        return (
          <div key={index}>
            <LikeComponent contents={like} />
          </div>
        );
      })}
    </div>
  );
};

export default LikedByAuthor;
