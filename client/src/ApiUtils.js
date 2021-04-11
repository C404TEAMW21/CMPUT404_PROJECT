import axios from "axios";
import { SERVER_HOST } from "./Constants";

const parseAuthorIdURl = (author) => {
  const authorIdList = author.id.split("/");

  if (authorIdList.length > 1) {
    author.id = authorIdList[authorIdList.length - 1];
  }

  return author;
};

export const getUserObject = async (token, id) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/api/author/${id}/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });

    return response;
  } catch (error) {
    return error.response;
  }
};

export const getCurrentUserObject = async (token) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/api/author/me/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });

    return response;
  } catch (error) {
    return error.response;
  }
};

export const checkIfFollowing = async (token, A, B) => {
  try {
    const response = await axios.get(
      `${SERVER_HOST}/api/author/${A.id}/followers/${B.id}/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      },
      {
        type: "follow",
        summary: "AuthorB wants to follow AuthorA",
        actor: {
          ...B,
        },
        object: {
          ...A,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const localRemoteFollowing = async (token, localAuthor, otherAuthor) => {
  let id = otherAuthor.id;
  if (otherAuthor.id.includes("team6")) {
    id = otherAuthor.id.split("/").pop();
  }

  try {
    const response = await axios.post(
      `${SERVER_HOST}/api/author/${localAuthor.id}/following/${id}/`,
      {
        type: "follow",
        summary: "AuthorA wants to follow AuthorB",
        actor: {
          ...localAuthor,
        },
        object: {
          ...otherAuthor,
        },
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );

    return response;
  } catch (error) {
    return error.response;
  }
};

export const sendFriendFollowRequest = async (token, authorA, authorB) => {
  parseAuthorIdURl(authorA);

  try {
    const response = await axios.put(
      `${SERVER_HOST}/api/author/${authorA.id}/followers/${authorB.id}/`,
      {
        type: "Follow",
        summary: "AuthorB wants to follow AuthorA",
        actor: {
          ...authorB,
        },
        object: {
          ...authorA,
        },
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getAllFollowers = async (token, id) => {
  try {
    const response = await axios.get(
      `${SERVER_HOST}/api/author/${id}/followers/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const unFollowAuthor = async (token, A, B) => {
  try {
    const response = await axios.delete(
      `${SERVER_HOST}/api/author/${A.id}/followers/${B.id}/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        data: {
          host: A.host,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getInboxPosts = async (token, id) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/api/author/${id}/inbox`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    const posts = response.data.items.filter(function (item) {
      return item.type == "post";
    });
    response.data.items = posts;
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getAllFriends = async (token, id) => {
  try {
    const response = await axios.get(
      `${SERVER_HOST}/api/author/${id}/friends/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getSpecificAuthorPost = async (token, path) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/api${path}/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    return response;
  } catch (error) {
    return error.response;
  }
};

export const deletePost = async (token, userId, postId) => {
  try {
    const response = await axios.delete(
      `${SERVER_HOST}/api/author/${userId}/posts/${postId}/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getAllAuthors = async (token) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/api/all-authors/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
    });
    return response;
  } catch (error) {
    return error.response;
  }
};

export const sendLike = async (token, us, otherAuthor, postId) => {
  let id = otherAuthor.id;
  if (otherAuthor.id.includes("team6")) {
    id = otherAuthor.id.split("/").pop();
  }

  let object = `${otherAuthor.host}api/author/${id}/posts/${postId}`;
  if (otherAuthor.host.includes("team6")) {
    object = `${otherAuthor.host}author/${id}/posts/${postId}`;
  }

  try {
    const response = await axios.post(
      `${SERVER_HOST}/api/author/${id}/inbox/`,
      {
        type: "like",
        author: us,
        object,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
    return response;
  } catch (error) {
    return error.response;
  }
};

export const getComments = async (token, postAuthor, postId) => {
  if (postAuthor.host.includes("konnection")) {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/api/author/${postAuthor.id}/posts/${postId}/comments/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  } else {
    let id = postAuthor.id;
    if (id.includes("team6")) {
      id = id.split("/").pop();
      postId = postId.split("/").pop();
    }

    const comment_url =
      postAuthor.host + `author/${id}/posts/${postId}/comments`;

    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${id}/posts/${postId}/get_remote_comments/`,
        {
          comment_url,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  }
};

export const createComment = async (
  token,
  author,
  postAuthor,
  postId,
  comment
) => {
  if (postAuthor.host.includes("konnection")) {
    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${postAuthor.id}/posts/${postId}/comments/`,
        {
          comment,
          contentType: "text/markdown",
          author,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  } else {
    let id = postAuthor.id;
    if (id.includes("team6")) {
      id = id.split("/").pop();
      postId = postId.split("/").pop();
    }

    const comment_url =
      postAuthor.host + `author/${id}/posts/${postId}/comments`;

    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${id}/posts/${postId}/create_remote_comments/`,
        {
          comment,
          comment_url,
          contentType: "text/markdown",
          author,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      return response;
    } catch (error) {
      return error.response;
    }
  }
};

export const likedByAuthor = async (token, author) => {
  let id = author.id;
  if (author.id.includes("team6")) {
    id = author.id.split("/").pop();
  }

  if (author.host.includes("konnection")) {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/api/author/${id}/liked/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );
      return response;
    } catch (error) {
      return error.response;
    }
  } else {
    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${id}/liked/`,
        {
          host_url: author.host,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );
      return response;
    } catch (error) {
      return error.response;
    }
  }
};

export const listLikesForPost = async (token, author, postId) => {
  let id = author.id;
  if (author.id.includes("team6")) {
    id = author.id.split("/").pop();
  }

  if (author.host.includes("konnection")) {
    try {
      const response = await axios.get(
        `${SERVER_HOST}/api/author/${id}/posts/${postId}/likes/`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );
      return response;
    } catch (error) {
      return error.response;
    }
  } else {
    try {
      const response = await axios.post(
        `${SERVER_HOST}/api/author/${id}/posts/${postId}/likes/`,
        {
          post_url: author.host,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );
      return response;
    } catch (error) {
      return error.response;
    }
  }
};
