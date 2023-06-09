import "./App.css";
import React, { useState, useEffect } from "react";
import { useSearchParams, Link, createSearchParams } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid";
import Switch from "@mui/material/Switch";
import Select from "@mui/material/Select";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";
import FormControlLabel from "@mui/material/FormControlLabel";
import CircularProgress from "@mui/material/CircularProgress";
import MenuItem from "@mui/material/MenuItem";
import FavoriteIcon from "@mui/icons-material/Favorite";
import BookmarkOutlinedIcon from "@mui/icons-material/BookmarkOutlined";
import axios from "axios";
import { stringify } from "qs";

function App() {
  const baseUrl =
    process.env.NODE_ENV === "production"
      ? "https://cocktails-back.vercel.app"
      : "http://127.0.0.1:8000";

  const [loaded, setLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [cocktails, setCocktails] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [substitute, setSubstitute] = useState(false);
  const [
    FilteredIngredientsSelectorValue,
    setFilteredIngredientsSelectorValue,
  ] = useState([]);
  const [filteredIngredients, setFilteredIngredients] = useState([]);
  const [
    filteredIngredientsWithSubstitution,
    setFilteredIngredientsWithSubstitution,
  ] = useState([]);
  let [searchParams, setSearchParams] = useSearchParams();

  async function handleSelector(event) {
    setFilteredIngredientsSelectorValue(event.target.value);
  }

  async function confirmSelector(event) {
    setFilteredIngredients(FilteredIngredientsSelectorValue);
    setSearchParams({
      substitute: JSON.stringify(substitute),
      ingredients: JSON.stringify(FilteredIngredientsSelectorValue),
    });
  }

  async function handleSubstituteSwitch(event) {
    setSubstitute(event.target.checked);
    setSearchParams({
      substitute: JSON.stringify(event.target.checked),
      ingredients: JSON.stringify(filteredIngredients),
    });
  }

  async function reset() {
    setFilteredIngredients([]);
    setFilteredIngredientsWithSubstitution([]);
    setFilteredIngredientsSelectorValue([]);
    setSubstitute(false);
    setSearchParams({});
  }

  useEffect(() => {
    if (searchParams.get("ingredients")) {
      const queryParamIngredients = JSON.parse(searchParams.get("ingredients"));
      setFilteredIngredients(queryParamIngredients);
      setFilteredIngredientsSelectorValue(queryParamIngredients);
    }
    if (searchParams.get("substitute")) {
      const substituteFromUrl = JSON.parse(searchParams.get("substitute"));
      setSubstitute(substituteFromUrl);
    }
    setLoaded(true);
  }, [searchParams]);

  useEffect(() => {
    async function f() {
      async function fetchCocktails() {
        setCocktails([]);
        setFilteredIngredientsWithSubstitution([]);
        const resp = await axios.get(`${baseUrl}/cocktails`, {
          params: { ingredients: filteredIngredients, substitute: substitute },
          paramsSerializer: (params) => {
            return stringify(params, { arrayFormat: "repeat" });
          },
        });
        const payload = resp.data;
        setCocktails(payload.cocktails);
        setIngredients(payload.ingredients);
        setFilteredIngredientsWithSubstitution(
          payload.ingredients_with_substitution.map((x) => x.code)
        );
      }

      if (!loaded) {
        return;
      }
      setLoading(true);
      try {
        await fetchCocktails();
      } finally {
        setLoading(false);
      }
    }
    f();
  }, [filteredIngredients, substitute, loaded, baseUrl]);

  return (
    loaded && (
      <div className="App">
        {loading}
        <header className="App-header">
          <div style={{ paddingBottom: "12px", paddingTop: "12px" }}>
            <div>
              <Tooltip title="If checked, allow replacing unavailable ingredients with similar ones (displayed in orange)">
                <FormControlLabel
                  control={
                    <Switch
                      checked={substitute}
                      onChange={handleSubstituteSwitch}
                    />
                  }
                  label="Substitution"
                />
              </Tooltip>
              <Select
                multiple
                displayEmpty
                renderValue={(selected) => {
                  if (
                    selected.length === 0 ||
                    !ingredients ||
                    !ingredients.length
                  ) {
                    return (
                      <p>
                        {ingredients && ingredients.length
                          ? "Available Ingredients"
                          : "Loading ingredients..."}
                      </p>
                    );
                  }
                  const selectedNames = selected.map((selectedCode) => {
                    return ingredients.filter((x) => x.code === selectedCode)[0]
                      .display_name;
                  });
                  return selectedNames.join(", ");
                }}
                value={FilteredIngredientsSelectorValue}
                onChange={handleSelector}
                onClose={confirmSelector}
              >
                {ingredients &&
                  ingredients.length &&
                  ingredients.map((ingredient) => {
                    return (
                      <MenuItem key={ingredient.code} value={ingredient.code}>
                        {ingredient.display_name} - {ingredient.count}
                      </MenuItem>
                    );
                  })}
              </Select>
            </div>
            <div style={{ marginTop: "12px" }}>
              <Button variant="contained" onClick={reset}>
                Reset
              </Button>
            </div>
          </div>
        </header>
        {!loading ? (
          <div style={{ marginTop: "12px" }} className="App-main">
            <Grid container spacing={2}>
              {cocktails &&
                cocktails.length &&
                cocktails.map((cocktail) => {
                  return (
                    <Grid item xs={6} sm={3} key={cocktail.id}>
                      <Link
                        to={`${cocktail.id.toString()}?${createSearchParams(
                          searchParams
                        )}`}
                      >
                        <Card sx={{ minHeight: 180 }} className="cocktail-card">
                          <CardContent>
                            <Typography variant="h5" component="div">
                              <span style={{ cursor: "pointer" }}>
                                {cocktail.name}
                              </span>
                              <span style={{ marginLeft: "4px" }}>
                                {cocktail.favorite_status === "FAVORITE" ? (
                                  <FavoriteIcon
                                    style={{
                                      color: "red",
                                      verticalAlign: "text-bottom",
                                    }}
                                  />
                                ) : cocktail.favorite_status ===
                                  "BOOKMARKED" ? (
                                  <BookmarkOutlinedIcon
                                    style={{
                                      color: "green",
                                      verticalAlign: "text-bottom",
                                    }}
                                  />
                                ) : (
                                  <></>
                                )}
                              </span>
                            </Typography>
                            <Typography sx={{ mb: 1.5 }} color="text.secondary">
                              {cocktail.family} {cocktail.shaken && " (Shaken)"}
                            </Typography>
                            <div>
                              {cocktail.doses.map((dose) => {
                                const available = filteredIngredients.includes(
                                  dose.liquid.code
                                );
                                const availableSubstituted =
                                  filteredIngredientsWithSubstitution.includes(
                                    dose.liquid.code
                                  );
                                const color = available
                                  ? "primary"
                                  : availableSubstituted
                                  ? "warning"
                                  : undefined;
                                return (
                                  <Chip
                                    key={dose.liquid.code}
                                    color={color}
                                    label={dose.liquid.display_name}
                                    style={{ margin: "2px" }}
                                  />
                                );
                              })}
                            </div>
                          </CardContent>
                        </Card>
                      </Link>
                    </Grid>
                  );
                })}
            </Grid>
          </div>
        ) : (
          <div style={{ marginTop: "30px" }}>
            <CircularProgress />
          </div>
        )}
      </div>
    )
  );
}

export default App;
