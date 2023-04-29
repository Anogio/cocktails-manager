import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function Cocktail() {
  const { id } = useParams();
  const [content, setContent] = useState();

  useEffect(() => {
    async function f() {
      async function fetchCocktail() {
        const baseUrl =
          process.env.NODE_ENV === "production"
            ? "https://cocktails-back.vercel.app"
            : "http://127.0.0.1:8000";
        const resp = await axios.get(`${baseUrl}/cocktails/${id}`);
        console.log(resp);
        setContent(resp.data);
      }
      fetchCocktail();
    }
    f();
  }, [id]);

  return (
    <div style={{ whiteSpace: "pre-line", margin: "50px" }}>
      <div dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
}

export default Cocktail;
