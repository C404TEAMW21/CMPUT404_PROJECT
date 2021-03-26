import React, { useState } from "react";
import { Search, Button, Label } from "semantic-ui-react";
import { getAllAuthors } from "../../ApiUtils";
import { useHistory } from "react-router-dom";
import "./ProfilePage.scss";

const ProfileSearchBar = (props) => {
  let history = useHistory();

  const [value, setValue] = useState("");
  const [results, setResults] = useState([]);
  const [rawResults, setRawResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const handleSearchChange = (e, { name, value }) => {
    setValue(value);
    setOpen(false);
  };
  const handleOnSubmit = async () => {
    setLoading(true);
    const responses = await getAllAuthors(props.token);

    let raw = [];

    responses.forEach((response) => {
      let filteredAuthors;
      if (response.status === 200) {
        filteredAuthors = response.data.filter((author) => {
          return author.displayName.toLowerCase().includes(value.trim());
        });

        raw = raw.concat(filteredAuthors);
      }
    });

    setRawResults(raw);

    let formatted = [];
    raw.forEach((author) => {
      let item = {
        title: author.displayName,
        description: author.host,
        author,
        onClick: authorOnClick,
      };

      formatted.push(item);
    });

    setOpen(true);
    setResults(formatted);
    setLoading(false);
  };

  const handleResultSelection = (e, { result }) => {
    const author = rawResults.filter((a) => {
      return a.displayName == result.title;
    });
  };

  const authorOnClick = (e, { author }) => {
    const authorId = author.id.split("/").pop();

    history.push({
      pathname: `/author/${authorId}`,
      state: { author },
    });
  };

  return (
    <div className="search-profile">
      <h3>Search for other profiles: </h3>
      <div className="search-container">
        <Search
          fluid
          results={results}
          onSearchChange={handleSearchChange}
          onResultSelect={handleResultSelection}
          value={value}
          open={open}
          icon={null}
        />
        <Button
          onClick={handleOnSubmit}
          loading={loading}
          icon="search"
          content="Search"
        />
      </div>
    </div>
  );
};

export default ProfileSearchBar;
