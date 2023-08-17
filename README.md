# Magic the Gathering Recommendation System and Card Viewer
## Purpose
This is my attempt to combine the two things I love most in the world: Python and Magic The Gathering. I want to use this application to push myself in pursuit of knowledge. 

In this post-COVID age, we find ourselves on SpellTable, playing online games more often than at our LGS. Often, our opponents camera has glare or is unfocused, inhibiting our ability to read the card effects and understand it. MTG players, both new and old, go to build or tweak their decks and can't find that perfect card to synergize with their deck properly. I wanted to fix that for myself and anyone else who might wish for better too. So, join me on this journey and we will be in a world of pure card synergy!

## Project Structure

    ├── LICENSE
    ├── .gitignore
    ├── README.md                   <- The top-level README for developers/collaborators using this project.
    │ 
    │ 
    │   
    ├── src                         <- Source code folder for this project
        |
        ├── front_page.py           <- Application file recognized by Streamlit
        |
        ├── multipage.py            <- Multi-page generator object for application. Creates sidebar with each page item.
        |
        ├── requirements.txt        <- File containing all necessary dependencies for the application
        |
        ├── classes                 <- Folder for classes created for scraping API, handling data, and user_functionality in the application.
        │
        ├── pages                   <- Folder containing all current pages available to the application
        │
        └── data                    <- Datasets used and created for this project
        
--------

## How to use the app
https://mtgtracer.streamlit.app

The application is now live with it's V1.0.2 and available for anyone with the link to use. For those looking to improve upon the app, all current dependencies for it are located within the requirements.txt file.

## Currently Available Features
* Users can look up any single-faced card and return a high-resolution image of the card.
* Users can create and save a decklist as a .txt file. 
* Users will be able to see the top-10 related cards to the input card.

## Limitations/Unintended Features
* Currently, the application cannot return dual-faced cards (i.e. Jorn, God of Winter // Kaldring, the Rimestaff)

## Future Updates
We want to create a drop-down text menu that starts to autofill the card-name with 10 results of cards that start with the letters provided. \
We will continue to improve on our current limitations and expand our features as needed.
