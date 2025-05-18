import { useEffect, useState } from "react";
import Papa from "papaparse";

export default function useSheetData(csvUrl) {
  const [data, setData] = useState([]);

  useEffect(() => {
    Papa.parse(csvUrl, {
      download: true,
      header: true,
      complete: (results) => {
        setData(results.data);
      },
    });
  }, [csvUrl]);

  return data;
}