import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom'
import axios from 'axios';



function Cocktail() {
    const { id } = useParams()
    const [content, setContent] = useState();

    async function fetchCocktails() {
        const resp = await axios.get(`http://127.0.0.1:8000/cocktails/${id}`)
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
        <div dangerouslySetInnerHTML={{__html:content}} />
    </div>
}

export default Cocktail;
