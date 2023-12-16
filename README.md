# Recipe Book App

An innovative mobile and web application designed to be your go-to culinary companion, offering a seamless blend of local and continental recipes to tantalize taste buds and inspire culinary adventures. This user-friendly app is a treasure trove of diverse recipes, catering to varying tastes, dietary needs, and cooking expertise.

## Table of Contents

* Feautures
* Installation
* Usage
* Contributing
* License

## Features

* User Authentication and Authorization
* CRUD operations on recipes
    - Create/add recipe: this functionality is for users to create or add a new recipe by providing fields for the recipe details, such as recipe name, ingredients for the recipe, instruction, cooking time and other details.
    - Read
        + view recipe: allows users to view the details of a specific recipe. It involves displaying the details of a particular recipe in a user-friendly format.
        + List recipe: this is about displaying the list of all available recipes using different criteria so that users can browse through them and find what interest them.
    - Update/edit recipe: thus feature allows users to modify existing recipes using a form to update any details of the recipe.
    - Delete/remove recipe: functionality for users to remove or delete a recipe, this action comes with a confirmation prompt message to avoid accidental deletion.
* Search functionalities: allows users to search existing recipes
* Save favorite recipes: allows users to save a recipe after creation or editing.

## Installation

### Prerequisites
* Python 3.x
* Virtual environment (recommended)
* Other dependencies are listed in requirements.txt

## Setup
* Clone the repository
    git clone https://github.com/Laracious/Recipe_book

* Navigate to the project directory
    cd Recipe_book/

* Create and activate a virtual environment (optional but recommended)
    python -m venv recipe
    source venv/bin/activate 
    On Windows, use venv\Scripts\activate

* Install dependencies
    pip install -r requirements.txt
* Run the application
    export FLASK_APP=app.py
    flask run

## Usage
* Register a new user
* Log in and explore recipes
* Add, edit, or delete a recipe
* Search for specific recipes

## Contributing
*Reporting bugs
* Suggesting enhancements
* Submitting pull requests
* Code style guide

## License
This project is licensed under the [MIT License - see the ](LICENSE.md) file for details.