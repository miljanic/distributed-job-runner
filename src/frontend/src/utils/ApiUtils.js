import { useState } from 'react';
import axios from 'axios';


export const baseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:9000';

export function useApiGet(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  axios
    .get(url)
    .then(({ data }) => {
      setData(data);
    })
    .catch((err) => {
      setError(err);
    })
    .finally(() => {
      setLoading(false);
    });

  return [data, loading, error];
}
