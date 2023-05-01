import Typography from "@mui/material/Typography";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderOutlinedIcon from "@mui/icons-material/FavoriteBorderOutlined";
import BookmarkAddOutlinedIcon from "@mui/icons-material/BookmarkAddOutlined";
import BookmarkOutlinedIcon from "@mui/icons-material/BookmarkOutlined";

import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function Cocktail() {
  const { id } = useParams();
  const [cocktail, setCocktail] = useState();

  const baseUrl =
    process.env.NODE_ENV === "production"
      ? "https://cocktails-back.vercel.app"
      : "http://127.0.0.1:8000";

  async function setCocktailFavoriteStatus(favoriteStatus) {
    const resp = await axios.patch(`${baseUrl}/cocktails/${id}`, {
      favorite_status: favoriteStatus,
    });
    setCocktail(resp.data);
  }

  useEffect(() => {
    async function f() {
      async function fetchCocktail() {
        const resp = await axios.get(`${baseUrl}/cocktails/${id}`);
        setCocktail(resp.data);
      }
      fetchCocktail();
    }
    f();
  }, [id, baseUrl]);

  return (
    cocktail && (
      <div style={{ whiteSpace: "pre-line", margin: "50px" }}>
        <Typography variant="h4" component="div">
          {cocktail.name}
          <span style={{ color: "red", cursor: "pointer", marginLeft: "4px" }}>
            {cocktail.favorite_status === "FAVORITE" ? (
              <FavoriteIcon
                onClick={function () {
                  setCocktailFavoriteStatus("NONE");
                }}
              />
            ) : (
              <FavoriteBorderOutlinedIcon
                onClick={function () {
                  setCocktailFavoriteStatus("FAVORITE");
                }}
              />
            )}
          </span>
          {cocktail.favorite_status !== "FAVORITE" && (
            <span
              style={{ color: "green", cursor: "pointer", marginLeft: "4px" }}
            >
              {cocktail.favorite_status === "BOOKMARKED" ? (
                <BookmarkOutlinedIcon
                  onClick={function () {
                    setCocktailFavoriteStatus("NONE");
                  }}
                />
              ) : (
                <BookmarkAddOutlinedIcon
                  onClick={function () {
                    setCocktailFavoriteStatus("BOOKMARKED");
                  }}
                />
              )}
            </span>
          )}
        </Typography>
        <Typography variant="h6" color="text.secondary">
          {cocktail.family}
        </Typography>
        <Typography variant="h5" style={{ marginTop: "12px" }}>
          Ingredients
        </Typography>
        <ul>
          {cocktail.doses.map((dose) => {
            return (
              <li key={dose.liquid.code}>
                <b>{dose.liquid.display_name}</b>:{" "}
                {dose.quantity === 0 ? "Unspecified" : dose.quantity}
              </li>
            );
          })}
          {cocktail.addons &&
            cocktail.addons.map((addon, index) => <li key={index}>{addon}</li>)}
        </ul>

        <Typography variant="h5" style={{ marginTop: "12px" }}>
          Preparation
        </Typography>
        {!!cocktail.preparation_recommendation && (
          <span>
            {cocktail.preparation_recommendation}
            <br />
          </span>
        )}
        <b>{cocktail.method}</b>
        {cocktail.feedback && (
          <div>
            <Typography variant="h5" style={{ marginTop: "12px" }}>
              Personal notes
            </Typography>
            {cocktail.feedback}
          </div>
        )}
      </div>
    )
  );
}

export default Cocktail;
