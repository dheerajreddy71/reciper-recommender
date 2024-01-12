## Food Recipe Recommender

### What is it ?

An item based recommder system for food recipes based on their ingredients

### What data it is based on ?

It is based on the public data available on kaggle: [Raw Recipes](https://www.kaggle.com/code/aayushmishra1512/food-recommender/input?select=RAW_recipes.csv)

### How the item based recommendation system works ?

#### step 1.

The ingredients are first embedded using AI models which are in sentence form. In NLP, sentence embedding refers to a numeric representation of a sentence in the form of a vector of real numbers, which encodes meaningful semantic information

![](https://miro.medium.com/v2/resize:fit:828/format:webp/1*ytRLNPOlDQ7kV6XhwH4baA.png)

##### 1.1 what model is used for embedding the sentences ?

[MiniLM: Small and Fast Pre-trained Models for Language Understanding and Generation](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased)

More models on this [link](https://www.sbert.net/docs/pretrained_models.html#model-overview)

2. After the ingredients are embedded (in vector form), the cosine similarity is calculated between the user search query and rest of the recipes. Basically finding the angle between two vectors, lesser the angle more similar they are and vice versa

![](https://storage.googleapis.com/lds-media/images/cosine-similarity-vectors.original.jpg)

### Demo

![demo1](https://github.com/kavyajeetbora/recipe_recommender/assets/38955297/ca259da4-436d-434d-9754-90cc277e1280)

### App is deployed on streamlit

The app is deployed on streamlit server

[Run the app](https://kavyajeetbora-recipe-recommender-app-bo2dv0.streamlit.app/)

### TODO

- Show the nutrition values
