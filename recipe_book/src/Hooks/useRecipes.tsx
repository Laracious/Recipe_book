import { useEffect, useState } from "react";
import apiClient from "../Services/api-client";
import { CanceledError } from "axios";

export interface Recipe {
  id: number;
  name: string;
  thumbnail_url: string;
  user_ratings:{
    score: number;
  }
}

interface FetchRecipesRespone {
  count: number;
  results: Recipe[];
}

const useRecipes = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    apiClient
      .get<FetchRecipesRespone>("/list", { signal: controller.signal })
      .then((res) => setRecipes(res.data.results))
      .catch((err) => {
        if (err instanceof CanceledError) return;
        setError(err.message);
      });

    return () => controller.abort();
  }, []);

  return { recipes, error };
};
export default useRecipes;