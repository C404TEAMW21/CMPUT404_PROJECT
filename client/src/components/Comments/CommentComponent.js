import React, { useEffect, useState, useContext } from "react";
import { Comment, Icon, Label, Button } from "semantic-ui-react";
import { Context } from "../../Context";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";
import "./Comments.scss";
import { sendLikeOnComment, listLikesForComment } from "../../ApiUtils";
import LikesModal from "../Likes/LikesModal";

const CommentComponent = ({
  author,
  content,
  contentType,
  published,
  commentId,
  setError,
  post,
}) => {
  const context = useContext(Context);

  const [loading, setLoading] = useState(false);
  const [numberLikes, setNumberLikes] = useState(0);
  const [openLikesModal, setOpenLikesModal] = useState(false);

  useEffect(() => {
    getNumberOfLikes();
  }, []);

  const getNumberOfLikes = async () => {
    const response = await listLikesForComment(
      context.cookie,
      author,
      commentId,
      post
    );
    if (response.status !== 200) {
      setError(true);
      return;
    }

    setNumberLikes(response.data.items.length);
  };

  const sendLikeToInbox = async () => {
    setLoading(true);

    const response = await sendLikeOnComment(
      context.cookie,
      context.user,
      post[0].author,
      commentId
    );
    if (response.status !== 200) {
      setError(true);
      setLoading(false);
      return;
    }
    getNumberOfLikes();
    setLoading(false);
  };

  const handleLikesModal = () => {
    setOpenLikesModal(!openLikesModal);
  };

  return (
    <div>
      <LikesModal
        open={openLikesModal}
        setOpen={handleLikesModal}
        commentId={commentId}
        author={author}
        numberLikes={numberLikes}
        post={post}
      />
      <Comment>
        <Comment.Content>
          <Comment.Author as="a">{author.displayName}</Comment.Author>
          <Comment.Metadata>
            <div>{published}</div>
          </Comment.Metadata>
          <Comment.Text>
            <ReactMarkdown plugins={[gfm]} children={content} />
          </Comment.Text>
          <Comment.Actions>
            <Comment.Action>
              <Button as="div" labelPosition="right">
                <Button color="red" onClick={sendLikeToInbox} loading={loading}>
                  <Icon name="heart" />
                  Like
                </Button>
                <Label
                  as="a"
                  basic
                  color="red"
                  pointing="left"
                  onClick={handleLikesModal}
                >
                  {numberLikes}
                </Label>
              </Button>
            </Comment.Action>
          </Comment.Actions>
        </Comment.Content>
      </Comment>
    </div>
  );
};

export default CommentComponent;
