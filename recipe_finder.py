import requests
from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RecipeFormatter:
    def __init__(self, api_key):
        self.api_key = api_key

    def sort_keys_and_format(self, recipe_info):
        # Sort keys alphabetically
        sorted_keys = sorted(recipe_info.keys())

        # Create a template for formatting
        template = """Start by showing the name of the recipe and a short description of the dish,
                      Then show the ingredients in bullet format and the procedure in a sorted number format
                      Make sure that the prompt is complete and do not stop mid-sentence or mid-word"""
        for key in sorted_keys:
            template += f"{key.replace('_', ' ').capitalize()}: {{{key}}}<br>"

        # Initialize LangChain
        llm = OpenAI(temperature=0.5, api_key=self.api_key)
        prompt_template = PromptTemplate(input_variables=list(recipe_info.keys()), template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Format the recipe information using LangChain
        formatted_recipe = chain.run(**recipe_info)

        return formatted_recipe

def get_recipe(query, api_key):
    """Get a recipe from Spoonacular API."""
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=1&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def get_recipe_id(query, api_key):
    """Get the ID of a recipe from Spoonacular API."""
    data = get_recipe(query, api_key)
    if data and "results" in data and len(data["results"]) > 0:
        recipe_id = data["results"][0]["id"]
        return recipe_id
    return None

def get_recipe_information(recipe_id, api_key):
    """Get recipe information from Spoonacular API."""
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/summary?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def main():
    # Streamlit UI
    st.title("Recipe Finder")

    query = st.text_input("Enter a recipe query:")
    if not query:
        st.warning("Please enter a recipe query.")
        return

    recipe_id = get_recipe_id(query, SPOONACULAR_API_KEY)
    if not recipe_id:
        st.warning("No recipe found.")
        return

    recipe_info = get_recipe_information(recipe_id, SPOONACULAR_API_KEY)

    # Display recipe image
    if "image" in recipe_info:
        st.image(recipe_info["image"], caption="Recipe Image", use_column_width=True)

    formatter = RecipeFormatter(OPENAI_API_KEY)
    formatted_recipe = formatter.sort_keys_and_format(recipe_info)

    st.subheader("Formatted Recipe:")
    st.markdown(formatted_recipe, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
