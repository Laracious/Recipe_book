import { useEffect, useState } from "react";
import apiClient from "../Services/api-client";
import { CanceledError } from "axios";
import { SelectField } from "@chakra-ui/react";

export interface Recipe {
  id: number;
  name: string;
  thumbnail_url: string;
  description: string;
  user_ratings:{
    score: string;
  }
}

interface FetchRecipesRespone {
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
      .get<FetchRecipesRespone>("/list", { signal: controller.signal })
      .then((res) => {
        setRecipes(res.data.results)
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
