import axios from "axios";

export default axios.create({
  baseURL: "https://tasty.p.rapidapi.com/recipes",
  headers: {
    'X-RapidAPI-Key': 'd4d358f586msheea05523a57959dp160f12jsnbecfac3a36bb',
    'X-RapidAPI-Host': 'tasty.p.rapidapi.com'
  }
});
