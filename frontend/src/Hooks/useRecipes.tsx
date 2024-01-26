import { useEffect, useState } from "react";
import apiClient from "../Services/api-client";
import { CanceledError } from "axios";

export interface Recipe {
  id: string;
  name: string;
  image: string;
  description: string;
  video: string;
  user_rating:{
    score: number;
  }
}

interface FetchRecipesRespone {
  recipes: any;
  count: number;
  results: Recipe[];
}

const useRecipes = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    setLoading(true);
    apiClient
      .get<FetchRecipesRespone>("/all?page=1&per_page=22", { signal: controller.signal })
      .then((res) => {
        console.log(res)
        setRecipes(res.data.recipes)
        setLoading(false);
    })
      .catch((err) => {
        if (err instanceof CanceledError) return;
        setError(err.message);
        setLoading(false)
      });

    return () => controller.abort();
  }, []);

  return { recipes, error, isLoading };
};
export default useRecipes;
