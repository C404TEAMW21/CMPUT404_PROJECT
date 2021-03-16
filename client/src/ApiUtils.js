import axios from "axios";
import { SERVER_HOST } from "./Constants";

export const getUserObject = async (token, id) => {
  try {
    const response = await axios.get(`${SERVER_HOST}/service/author/${id}/`, {
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
    const response = await axios.get(`${SERVER_HOST}/service/author/me/`, {
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
      `${SERVER_HOST}/service/author/${A}/followers/${B}/`,
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

export const sendFriendFollowRequest = async (token, A, B) => {
  try {
    const response = await axios.put(
      `${SERVER_HOST}/service/author/${A}/followers/${B}/`,
      {},
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
      `${SERVER_HOST}/service/author/${id}/followers/`,
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
      `${SERVER_HOST}/service/author/${A}/followers/${B}/`,
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
    const response = await axios.get(
      `${SERVER_HOST}/service/author/${id}/inbox`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      }
    );
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
      `${SERVER_HOST}/service/author/${id}/friends/`,
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
    const response = await axios.get(`${SERVER_HOST}/service${path}/`, {
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
