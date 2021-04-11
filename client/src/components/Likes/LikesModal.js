import React, { useContext, useEffect, useState } from "react";
import { Modal, Message } from "semantic-ui-react";
import { listLikesForPost, listLikesForComment } from "../../ApiUtils";
import { Context } from "../../Context";

const LikesModal = (props) => {
  const context = useContext(Context);

  const [error, setError] = useState(false);
  const [likes, setLikes] = useState([]);

  useEffect(() => {
    if (props.postId) {
      displayLikesForPost();
    } else if (props.commentId) {
      displayLikesForComment();
    }
  }, [props.open]);

  const displayLikesForPost = async () => {
    const response = await listLikesForPost(
      context.cookie,
      props.author,
      props.postId
    );

    if (response.status !== 200) {
      setError(true);
      return;
    }

    setLikes(response.data.items);
  };

  const displayLikesForComment = async () => {
    const response = await listLikesForComment(
      context.cookie,
      props.author,
      props.commentId
    );

    if (response.status !== 200) {
      setError(true);
      return;
    }

    setLikes(response.data.items);
  };

  return (
    <Modal
      onClose={() => props.setOpen()}
      onOpen={() => props.setOpen()}
      open={props.open}
      size="mini"
    >
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      <Modal.Header>Liked By</Modal.Header>
      <Modal.Content>
        <Modal.Description>
          {likes.map((like, index) => {
            return <p>{like.author.displayName}</p>;
          })}
        </Modal.Description>
      </Modal.Content>
    </Modal>
  );
};

export default LikesModal;
