import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom'
import axios from 'axios';



function Cocktail() {
    const { id } = useParams()
    const [content, setContent] = useState();

    async function fetchCocktails() {
      const baseUrl = process.env.NODE_ENV == "production" ? "https://cocktails-back.vercel.app" : "http://127.0.0.1:8000"
        const resp = await axios.get(`${baseUrl}/cocktails/${id}`)
        console.log(resp)
        setContent(resp.data) 
    }
    useEffect(() => {
        async function f() {
          fetchCocktails()
        }
        f();
      }, [id]);
    
    return <div style={{whiteSpace: "pre-line", margin: '50px'}}>
      THIS IS A COCKTAIL
        <div dangerouslySetInnerHTML={{__html:content}} />
    </div>
}

export default Cocktail;
