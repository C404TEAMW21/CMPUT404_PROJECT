import React from "react";
import { Button, Modal } from "semantic-ui-react";

const DeletePostModal = (props) => {
  const handleDelete = async () => {
    await props.handleDeletePost(props.id, props.index);
    props.setOpen();
  };

  return (
    <Modal size="mini" open={props.open}>
      <Modal.Header>Delete Post</Modal.Header>
      <Modal.Content>
        <p>Are you sure you want to delete this post?</p>
      </Modal.Content>
      <Modal.Actions>
        <Button onClick={props.setOpen}>Cancel</Button>
        <Button negative onClick={handleDelete}>
          Delete
        </Button>
      </Modal.Actions>
    </Modal>
  );
};

export default DeletePostModal;
