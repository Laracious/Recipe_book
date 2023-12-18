import axios from "axios"

export default axios.create({
    baseURL: "https://edamam-food-and-grocery-database.p.rapidapi.com/api/food-database/v2",
    params: {
        key: 'd4d358f586msheea05523a57959dp160f12jsnbecfac3a36bb'
    }
    }
)