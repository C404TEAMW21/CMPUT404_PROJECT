import React, { useState, useContext, useEffect } from "react";
import { Dimmer, Loader, Message } from "semantic-ui-react";
import { getSpecificAuthorPost } from "../../ApiUtils";
import { Context } from "../../Context";
import SpecificPostComponent from "./SpecificPostComponent";

const SpecificPostPage = () => {
  const context = useContext(Context);

  const [loading, updateLoading] = useState(true);
  const [error, updateError] = useState(false);

  useEffect(() => {
    callGetPost();
  }, []);

  const callGetPost = async () => {
    const response = await getSpecificAuthorPost(
      context.cookie,
      window.location.pathname
    );

    if (response.status === 200) {
      console.log(response.data);
    } else {
      updateError(true);
    }

    updateLoading(false);
  };
  return (
    <div>
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Loading Post...</Loader>
        </Dimmer>
      )}
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      <SpecificPostComponent />
    </div>
  );
};

export default SpecificPostPage;
