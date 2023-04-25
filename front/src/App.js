import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid';
import Switch from '@mui/material/Switch';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import MenuItem from '@mui/material/MenuItem';
import axios from 'axios';
import { stringify } from 'qs';

function App() {
  const [cocktails, setCocktails] = useState();
  const [ingredients, setIngredients] = useState();
  const [substitute, setSubstitute] = useState(false);
  const [filteredIngredients, setFilteredIngredients] = useState([]);
  let [searchParams, setSearchParams] = useSearchParams();

  async function fetchCocktails() {
        const baseUrl = process.env.NODE_ENV == "production" ? "https://cocktails-back.vercel.app" : "http://127.0.0.1:8000"
        const resp = await axios.get(`${baseUrl}/cocktails`, 
        { params: { ingredients: filteredIngredients, substitute: substitute},
        paramsSerializer: (params) => {
          return stringify(params, {arrayFormat: 'repeat'})
       },
      },);
        const payload = resp.data;
        setCocktails(payload.cocktails)
        setIngredients(payload.ingredients)
  }

  async function handleSelector(event) {
    setFilteredIngredients(event.target.value)
    setSearchParams({ingredients: JSON.stringify(event.target.value)});
  }

  async function handleSubstituteSwitch(event) {
    setSubstitute(event.target.checked)
  }

  useEffect(() => {
    async function f() {
      fetchCocktails()
    }
    f();
  }, [filteredIngredients, substitute]);

  useEffect(() => {
      if (searchParams.get("ingredients")) {
        setFilteredIngredients(JSON.parse(searchParams.get("ingredients")))
      }
  }, [])

  
  return (
    <div className="App">
      <header className="App-header">
        <FormControlLabel control={<Switch value={substitute} onChange={handleSubstituteSwitch}/>} label="Substitution" />
        
        <Select 
          multiple
          displayEmpty
          renderValue={(selected) => {
            if (selected.length === 0) {
              return <p>Ingredients</p>;
            }

            return selected.join(', ');
          }}
          value={filteredIngredients}
          onChange={handleSelector}
          >
            {ingredients && ingredients.map((ingredient) => {
              return <MenuItem key={ingredient.code} value={ingredient.code}>
                {ingredient.display_name} - {ingredient.count}
              </MenuItem>
            })}
          </Select>
      </header>
      <div>
        <Grid container spacing={2}>
        {cocktails && cocktails.map((cocktail) => {
          return <Grid item xs={6} sm={3} key={cocktail.index}>
          <Link to={cocktail.index.toString()} target="_blank">
          <Card sx={{ minHeight: 180 }}>
          <CardContent>
          <Typography variant="h5" component="div">
            {cocktail.name}
          </Typography>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            { cocktail.family} {cocktail.custom_category ? `- ${cocktail.custom_category}` : ''}
          </Typography>
          <div>
            {cocktail.doses.map((dose) => <Chip key={dose.liquid.code}
             color={ filteredIngredients.includes(dose.liquid.code) ? 'primary': undefined} label={dose.liquid.display_name} />)}
          </div>
          </CardContent>
        </Card>
        </Link>
        </Grid>
        })
        }
        </Grid>
      
      </div>
    </div>
  );
}

export default App;
