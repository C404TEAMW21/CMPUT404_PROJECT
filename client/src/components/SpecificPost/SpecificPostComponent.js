import React, { useState, useContext, useEffect } from "react";
import { Dimmer, Loader, Message } from "semantic-ui-react";
import { getSpecificAuthorPost } from "../../ApiUtils";
import { Context } from "../../Context";

const SpecificPostComponent = () => {
  const context = useContext(Context);

  return <div>Post</div>;
};

export default SpecificPostComponent;
