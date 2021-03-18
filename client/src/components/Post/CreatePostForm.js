import React, { useState } from "react";
import {
  Button,
  Form,
  Input,
  Select,
  TextArea,
  Radio,
  Message,
  Checkbox,
} from "semantic-ui-react";
import ImageUploader from "react-images-upload";
import "./CreatePostPage.scss";

const visibilityOptions = [
  { key: "p", text: "Public", value: "PUBLIC" },
  { key: "f", text: "Friends", value: "FRIENDS" },
  { key: "a", text: "Author", value: "AUTHOR" },
];

const CreatePost = (props) => {
  const [title, updateTitle] = useState("");
  const [description, updateDescription] = useState("");
  const [content, updateContent] = useState("");
  const [titleError, updateTitleError] = useState(null);
  const [descError, updateDescError] = useState(null);
  const [image, updateImage] = useState([]);
  const [contentType, updateContentType] = useState("text/markdown");
  const [visibility, updateVisibility] = useState("PUBLIC");
  const [unlisted, updateUnlisted] = useState(false);
  const [formError, updateFormError] = useState(false);
  const [formErrorMessage, updateFormErrorMessage] = useState(null);
  const [loading, updateLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (titleError || descError) {
      updateFormError(true);

      const message = (
        <Message
          error
          size="tiny"
          header="Error"
          content="Please resolve errors."
        />
      );

      updateFormErrorMessage(message);
      return;
    } else if (formErrorMessage) updateFormErrorMessage(null);

    const postInfo = {
      title,
      source: "", // TODO: not sure what source is
      origin: "", // TODO: not sure what origin is
      description,
      contentType,
      content,
      visibility,
      unlisted,
    };

    if (image.length > 0) {
      postInfo["content"] = image;
    }

    updateLoading(true);
    const response = await props.submit(postInfo);
    updateLoading(false);

    if (response.status === 201) {
      const postId = response.data.id.split("/").splice(-2)[0];
      props.postSuccess(postId);
    } else {
      const message = (
        <Message
          error
          size="tiny"
          header="Unexpected Error"
          content="Please try again."
        />
      );
      updateFormError(true);
      updateFormErrorMessage(message);
    }
  };

  const handleInputChange = (e, { name, value }) => {
    if (name === "title") {
      validLength(name, value);
      updateTitle(value);
    } else if (name === "description") {
      validLength(name, value);
      updateDescription(value);
    } else if (name === "content") updateContent(value);
  };

  const validLength = (name, value) => {
    if (name === "title" && value.length <= 100) {
      if (titleError) updateTitleError(null);
      return true;
    } else if (name === "description" && value.length <= 250) {
      if (descError) updateDescError(null);
      return true;
    } else if (name === "title" && value.length > 100) {
      if (titleError === null) {
        const error = {
          content: "Title length must be 100 characters or less.",
          pointing: "below",
        };
        updateTitleError(error);
      }

      return false;
    } else if (name === "description" && value.length > 250) {
      if (descError === null) {
        const error = {
          content: "Description length must be 250 characters or less.",
          pointing: "below",
        };
        updateDescError(error);
      }

      return false;
    }
  };

  const handleRadioChange = (e, { value }) => {
    updateContentType(value);
  };

  const addImage = (image) => {
    updateImage(image);
  };

  const truncateFileName = (filename) => {
    if (filename.length > 15)
      return "..." + filename.substr(filename.length - 15);
    return filename;
  };

  const handleSelectChange = (e, { value }) => {
    updateVisibility(value);
  };

  const handleCheckboxChange = () => {
    updateUnlisted(!unlisted);
  };

  return (
    <Form
      className="create-post-form"
      onSubmit={handleSubmit}
      error={formError}
      loading={loading}
    >
      {formErrorMessage ? formErrorMessage : <div></div>}
      <Form.Field
        required
        control={Input}
        name="title"
        label="Title"
        placeholder="Post title"
        value={title}
        onChange={handleInputChange}
        error={titleError}
      />
      <Form.Field
        control={Input}
        name="description"
        label="Description"
        placeholder="Post description"
        value={description}
        onChange={handleInputChange}
        error={descError}
      />
      <Form.Field
        control={TextArea}
        name="content"
        label="Content"
        placeholder="Post content"
        value={content}
        onChange={handleInputChange}
        disabled={image[0] ? true : false}
      />
      <Form.Group inline>
        <label>Content Type:</label>
        <Form.Field
          control={Radio}
          label="Common Mark"
          value="text/markdown"
          checked={contentType === "text/markdown"}
          onChange={handleRadioChange}
          disabled={image[0] ? true : false}
        />
        <Form.Field
          control={Radio}
          label="Plain Text"
          value="text/plain"
          checked={contentType === "text/plain"}
          onChange={handleRadioChange}
          disabled={image[0] ? true : false}
        />
      </Form.Group>
      <Form.Field disabled={content ? true : false}>
        <ImageUploader
          label={image[0] ? truncateFileName(image[0].name) : "Upload an Image"}
          buttonText="Choose Image"
          withIcon={true}
          onChange={addImage}
          singleImage={true}
          withPreview={true}
          imgExtension={[".jpg", ".png"]}
          maxFileSize={5242880}
        />
      </Form.Field>
      <Form.Field
        width={6}
        control={Select}
        options={visibilityOptions}
        value={visibility}
        onChange={handleSelectChange}
        label="Post Visibility"
        placeholder="Post Visibility"
      />
      <Form.Field
        control={Checkbox}
        label="Unlisted Post"
        checked={unlisted}
        onChange={handleCheckboxChange}
      />
      <Form.Field>
        <Button className="create-post-btn" type="submit">
          Create Post
        </Button>
      </Form.Field>
    </Form>
  );
};

export default CreatePost;
