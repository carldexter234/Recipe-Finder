# Recipe Finder

This application allows you to find recipes based on your query. It utilizes the Spoonacular API to fetch recipe information and the OpenAI language model for formatting the retrieved data.

## Installation

1. Clone the repository:
git clone <repository_URL>


2. Install the required dependencies:

pip install -r requirements.txt


3. Set up environment variables:

- Create a `.env` file in the root directory.
- Add the following lines to the `.env` file and replace `<your_SPOONACULAR_API_KEY>` and `<your_OPENAI_API_KEY>` with your respective API keys:

  ```
  SPOONACULAR_API_KEY=<your_SPOONACULAR_API_KEY>
  OPENAI_API_KEY=<your_OPENAI_API_KEY>
  ```

## Usage

Run the following command to start the application:

streamlit run recipe_finder.py


Once the application is running, enter a recipe query in the text input field, and the app will display the formatted recipe information along with the recipe image (if available).

## Dependencies

- `requests`
- `dotenv`
- `streamlit`
- `langchain`

## Credits

- [Spoonacular API](https://spoonacular.com/)
- [OpenAI](https://openai.com/)
- [Streamlit](https://streamlit.io/)

