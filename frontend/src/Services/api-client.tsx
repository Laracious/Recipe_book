import axios from "axios";

export default axios.create({
  baseURL: "http://127.0.0.1:5000/api/v1/recipes/"
  // headers: {
  //   'X-RapidAPI-Key': 'c3bdd45b4dmsh54e7cd50dfa1272p1c1d30jsn04da1101d6c4',
  //   'X-RapidAPI-Host': 'tasty.p.rapidapi.com'
  // }
});
