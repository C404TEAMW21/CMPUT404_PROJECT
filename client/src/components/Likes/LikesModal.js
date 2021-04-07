import React, { useContext, useEffect, useState } from "react";
import { Modal, Message } from "semantic-ui-react";
import { listLikesForPost } from "../../ApiUtils";
import { Context } from "../../Context";

const LikesModal = (props) => {
  const context = useContext(Context);

  const [error, setError] = useState(false);
  const [likes, setLikes] = useState([]);

  useEffect(() => {
    displayLikesForPost();
  }, [props.open]);

  const displayLikesForPost = async () => {
    try {
      const response = await listLikesForPost(
        context.cookie,
        props.author,
        props.postId
      );
      setLikes(response.data);
    } catch (err) {
      setError(true);
    }
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
