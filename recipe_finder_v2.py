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
        sorted_keys = sorted(recipe_info.keys())
        template = """
        Recipe Name: {title}<br>
        Summary: {summary}<br>
        Ingredients:<br>
        {ingredients}<br>
        Instructions:<br>
        {instructions}<br>
        """
        llm = OpenAI(temperature=0.5, api_key=self.api_key)
        prompt_template = PromptTemplate(input_variables=sorted_keys, template=template)
        chain = LLMChain(llm=llm, prompt=prompt_template)
        formatted_recipe = chain.run(**recipe_info)
        return formatted_recipe

@st.cache_data
def get_recipe(query, api_key):
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=1&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

@st.cache_data
def get_recipe_id(query, api_key):
    data = get_recipe(query, api_key)
    if data and "results" in data and len(data["results"]) > 0:
        return data["results"][0]["id"]
    return None

@st.cache_data
def get_recipe_information(recipe_id, api_key):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}&includeNutrition=false"
    response = requests.get(url)
    return response.json()

def extract_ingredients(recipe_info):
    if 'extendedIngredients' in recipe_info:
        ingredients = recipe_info['extendedIngredients']
        return [ingredient['original'] for ingredient in ingredients]
    return []

def extract_instructions(recipe_info):
    if 'analyzedInstructions' in recipe_info and len(recipe_info['analyzedInstructions']) > 0:
        instructions = recipe_info['analyzedInstructions'][0]['steps']
        return [step['step'] for step in instructions]
    return []

def main():
    st.sidebar.title("Recipe Finder")
    query = st.sidebar.text_input("Enter a recipe query:")

    if st.sidebar.button("Search"):
        if not query:
            st.sidebar.warning("Please enter a recipe query.")
            return
        
        with st.spinner('Fetching recipe...'):
            recipe_id = get_recipe_id(query, SPOONACULAR_API_KEY)
            if not recipe_id:
                st.sidebar.error("No recipe found.")
                return

            recipe_info = get_recipe_information(recipe_id, SPOONACULAR_API_KEY)

        # Debug: Display raw recipe information and its keys
        st.subheader("Raw Recipe Information:")
        st.code(recipe_info)

        st.subheader("Recipe Info Keys:")
        st.code(recipe_info.keys())

        if "image" in recipe_info:
            st.image(recipe_info["image"], caption="Recipe Image", use_column_width=True)

        # Extract and prepare the ingredients and instructions
        ingredients = extract_ingredients(recipe_info)
        instructions = extract_instructions(recipe_info)

        # Debug: Display extracted ingredients and instructions
        st.subheader("Extracted Ingredients:")
        st.write(ingredients)

        st.subheader("Extracted Instructions:")
        st.write(instructions)

        # Check if ingredients and instructions are empty
        if not ingredients:
            st.error("No ingredients found.")
            return

        if not instructions:
            st.error("No instructions found.")
            return

        # Update recipe_info with the new keys
        recipe_info['ingredients'] = "\n".join(ingredients)
        recipe_info['instructions'] = "\n".join(instructions)

        formatter = RecipeFormatter(OPENAI_API_KEY)
        formatted_recipe = formatter.sort_keys_and_format(recipe_info)
        
        st.subheader("Formatted Recipe:")
        with st.expander("View Full Recipe"):
            st.markdown(formatted_recipe, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
