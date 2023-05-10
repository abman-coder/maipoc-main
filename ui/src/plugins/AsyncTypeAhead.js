import React, { useCallback, useEffect, useState } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import { methods } from "./http";

import 'react-bootstrap-typeahead/css/Typeahead.css';

const CACHE = {};
const PER_PAGE = 50;


function AsyncInput({ searchUrl, placeholder, query, setQuery, keyWord, onChange, type }) {
  const [isLoading, setIsLoading] = useState(false);
  const [options, setOptions] = useState([]);
  // const [query, setQuery] = useState('');

  const handleInputChange = (q) => {
    setQuery("" + q);
  };

  async function makeAndHandleRequest(searchUrl, query, keyWord) {
    const result = await methods.get(`${searchUrl}?q=${query}&per_page=20&type=${type}`)

    const options = result.data[keyWord];
    return { options };
  }

  const handlePagination = (e, shownResults) => {
    const cachedQuery = CACHE[query];

    // Don't make another request if:
    // - the cached results exceed the shown results
    // - we've already fetched all possible results
    if (
      cachedQuery.options.length > shownResults ||
      cachedQuery.options.length === cachedQuery.total_count
    ) {
      return;
    }

    setIsLoading(true);

    const page = cachedQuery.page + 1;

    makeAndHandleRequest(searchUrl, query + `&p=${options.length / 50 + 1}&`, keyWord).then((resp) => {
      const options = cachedQuery.options.concat(resp.options);
      CACHE[query] = { ...cachedQuery, options, page };

      setIsLoading(false);
      setOptions(options);
    });
  };

  // `handleInputChange` updates state and triggers a re-render, so
  // use `useCallback` to prevent the debounced search handler from
  // being cancelled.
  const handleSearch = useCallback((q) => {
    if (CACHE[q]) {
      setOptions(CACHE[q].options);
      return;
    }

    setIsLoading(true);
    makeAndHandleRequest(searchUrl, q, keyWord).then((resp) => {
      CACHE[q] = { ...resp, page: 1 };

      setIsLoading(false);
      setOptions(resp.options);
    });
  }, []);

  useEffect(() => {
    if (!query) {
      makeAndHandleRequest(searchUrl, "", keyWord).then((resp) => {
        CACHE[query] = { ...resp, page: 1 };

        setIsLoading(false);
        setOptions(resp.options);
      });
    }
  }, [type, query]);


  return (
    <div>
      <AsyncTypeahead
        id="async-pagination-example"
        isLoading={isLoading}
        labelKey="ids"
        maxResults={PER_PAGE - 1}
        minLength={0}
        onInputChange={handleInputChange}
        onChange={onChange}
        onPaginate={handlePagination}
        onSearch={handleSearch}
        options={options}
        clearButton={true}
        delay={700}
        paginate
        paginationText="click to load more"
        placeholder={placeholder}
        renderMenuItemChildren={(option) => (
          <div key={option}>
            <span>{option}</span>
          </div>
        )}
        useCache={false}
      />
    </div>
  );
}

export default AsyncInput;