import axios from "axios";
import { SERVER_HOST, TEAM2_HOST, TEAM6_HOST, TEAM8_HOST } from "./Constants";

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
  console.log(localAuthor);
  console.log(otherAuthor);
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

    // const response = await axios({
    //   method: "get",
    //   url: `${SERVER_HOST}/api/author/${localAuthor.id}/following/${otherAuthor.id}/`,
    //   headers: {
    //     "Content-Type": "application/json",
    //     Authorization: `Token ${token}`,
    //   },
    //   data: {
    //     type: "follow",
    //     summary: "AuthorA wants to follow AuthorB",
    //     actor: {
    //       ...localAuthor,
    //     },
    //     object: {
    //       ...otherAuthor,
    //     },
    //   },
    // });
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

const getAuthorsKonnections = (token) =>
  axios.get(`${SERVER_HOST}/api/authors/`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });

const getAuthorsTeam6 = () =>
  axios.get(`${TEAM6_HOST}/authors`, {
    auth: {
      username: process.env.REACT_APP_TEAM6_BAUTH_USERNAME,
      password: process.env.REACT_APP_TEAM6_BAUTH_PASSWORD,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });

// justin's team
const getAuthorsTeam2 = () =>
  axios.get(`${TEAM2_HOST}/api/authors/`, {
    headers: {
      "Content-Type": "application/json",
    },
  });

// anas' team
const getAuthorsTeam8 = () =>
  axios.get(`${TEAM8_HOST}/api/authors/`, {
    headers: {
      "Content-Type": "application/json",
    },
  });

export const getAllAuthors = async (token) => {
  console.log("hello");
  try {
    const responses = await axios.all([
      getAuthorsKonnections(token),
      getAuthorsTeam6(),
      getAuthorsTeam2(),
      getAuthorsTeam8(),
    ]);

    return responses;
  } catch (error) {
    return error.response;
  }
};

export const getLikesForPost = async (token, authorId, postId) => {
  try {
    const response = await axios.get(
      `${SERVER_HOST}/api/author/${authorId}/posts/${postId}/likes`,
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

export const sendLike = async (token, us, otherAuthor, postId) => {
  try {
    const response = await axios.post(
      `${SERVER_HOST}/api/author/${otherAuthor.id}/inbox/`,
      {
        type: "like",
        author: us,
        object: `${otherAuthor.host}api/author/${otherAuthor.id}/posts/${postId}`,
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

export const likedByAuthor = async (token, authorId) => {
  try {
    const response = await axios.get(
      `${SERVER_HOST}/api/author/${authorId}/liked`,
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
