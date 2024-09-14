import streamlit as st
from glob import glob
import pandas as pd
import utils
from googletrans import Translator, LANGUAGES

## STREAMLIT CONFIGURATION
## --------------------------------------------------------------------------------##
st.set_page_config(
    page_title="Food Recipe Recommender", page_icon=r"images/logo-color.ico"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

## Session state variables
## -------------------------------------------------------------------

if "data" not in st.session_state:
    files = glob(r"data/*.parquet")
    df = pd.read_parquet(files)
    df["ingredients"] = (
        df["ingredients"]
        .str.strip("[]")
        .str.replace("'", "")
        .str.replace('"', "")
        .str.split(",")
        .apply(lambda x: [y.strip() for y in x])
    )

    st.session_state["data"] = df

## App Layout
## -------------------------------------------------------------------

st.image(r"images/logo-no-background.png", width=400)

recipe = st.selectbox(
    label="Search the recipe:", options=st.session_state["data"]["name"], index=100
)

col1, col2 = st.columns([1, 3])
with col1:
    num_recipes = st.number_input(
        label="Number of similar recipes", min_value=3, max_value=10, step=1
    )

## Language selection
## -------------------------------------------------------------------

translator = Translator()
target_language = st.selectbox(
    "Select Language",
    options=list(LANGUAGES.values()),
    index=0
)
target_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(target_language)]

## Find similarity
## -------------------------------------------------------------------

if "result" not in st.session_state:
    st.session_state["result"] = None

def assign_values():
    st.session_state["result"] = utils.find_similar_recipe(
        recipe, st.session_state["data"], num_recipes
    )

search = st.button(label="Search", on_click=assign_values)

## Display the results
## -------------------------------------------------------------------

if search:
    x = st.session_state["data"].iloc[0]
    for i, row_index in enumerate(range(st.session_state["result"].shape[0])):
        dfx = st.session_state["result"].iloc[row_index]

        with st.expander(
            translator.translate(
                f"{i+1}. {dfx['name'].capitalize()} | Similarity :blue[{dfx['similarity']}] %",
                dest=target_language_code
            ).text
        ):
            tab_1, tab_2, tab_3 = st.tabs(
                [
                    translator.translate("Summary", dest=target_language_code).text,
                    translator.translate("Ingredients", dest=target_language_code).text,
                    translator.translate("Recipe", dest=target_language_code).text
                ]
            )

            with tab_1:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        label=translator.translate("Calories", dest=target_language_code).text,
                        value=dfx["calories"]
                    )

                with col2:
                    st.metric(
                        label=translator.translate("Number of Steps", dest=target_language_code).text,
                        value=dfx["n_steps"]
                    )

                with col3:
                    st.metric(
                        label=translator.translate("Number of Ingredients", dest=target_language_code).text,
                        value=dfx["n_ingredients"]
                    )

                with col4:
                    st.metric(
                        label=translator.translate("Cooking Time", dest=target_language_code).text,
                        value=f"{dfx['minutes']} Mins"
                    )

                fig = utils.plot_nutrition(dfx)
                st.plotly_chart(fig)

            with tab_2:
                st.text(
                    translator.translate(
                        f"Number of Ingredients: {dfx['n_ingredients']}",
                        dest=target_language_code
                    ).text
                )
                for i, step in enumerate(dfx["ingredients"]):
                    st.markdown(f"{i+1}. {translator.translate(step, dest=target_language_code).text}")

            with tab_3:
                st.text(translator.translate("Recipe", dest=target_language_code).text)
                for i, step in enumerate(dfx["steps"]):
                    st.markdown(f"{i+1}. {translator.translate(step, dest=target_language_code).text}")

