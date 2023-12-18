import { useEffect, useState } from "react";
import apiClient from "../Services/api-client";
import { CanceledError } from "axios";

interface Recipe {
    id: number;
    name: string;
  }
  
  interface FetchRecipesRespone {
    count: number;
    results: Recipe[];
  }
  
const useRecipes = () => {
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController;
    
    apiClient
      .get<FetchRecipesRespone>("/list", {signal: controller.signal})
      .then((res) => setRecipes(res.data.results))
      .catch((err) => {
      if (err instanceof CanceledError) return;
      setError(err.message)});

      return () => controller.abort();
      }, []);

  return {recipes, error};
}
export default useRecipes;