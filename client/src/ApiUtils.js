import axios from "axios";
import { SERVER_HOST, TEAM2_HOST, TEAM6_HOST } from "./Constants";

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
      `${SERVER_HOST}/api/author/${A}/followers/${B}/`,
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
      `${SERVER_HOST}/api/author/${A}/followers/${B}/`,
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
  axios.get(`${TEAM6_HOST}/api/authors`, {
    auth: {
      username: process.env.REACT_APP_TEAM6_BAUTH_USERNAME,
      password: process.env.REACT_APP_TEAM6_BAUTH_PASSWORD,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });

const getAuthorsTeam2 = () =>
  axios.get(`${TEAM2_HOST}/api/authors/`, {
    headers: {
      "Content-Type": "application/json",
    },
  });

export const getAllAuthors = async (token) => {
  try {
    const responses = await axios.all([
      getAuthorsKonnections(token),
      getAuthorsTeam6(),
      // getAuthorsTeam2(),
    ]);

    return responses;
  } catch (error) {
    return error.response;
  }
};
