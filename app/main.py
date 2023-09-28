import streamlit as st
from src.schemas.engine import Engine
from PIL import Image
from st_clickable_images import clickable_images
from streamlit_extras import add_vertical_space as avs
import json

with open("app/config.json", "r") as file:
    json_config = json.load(file)

st.set_page_config(
    page_title=json_config["pageTitle"], # Title of the page in your browser tab
    layout="wide" # Wide mode
)


with open('app/src/assets/css/app.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

if "engine" not in st.session_state:
    st.session_state.engine: Engine = Engine()

if "active_page" not in st.session_state:
    st.session_state.active_page: int = 1
    
if "selected_claim" not in st.session_state:
    st.session_state.selected_claim: int = 0

if "entities" not in st.session_state:
    st.session_state.entities: str = None
    
if "next_steps" not in st.session_state:
    st.session_state.next_steps: str = None
    
if "summary" not in st.session_state:
    st.session_state.summary: str = None
    

st.markdown(f'<h1 style="text-align: center; font-size:65px; color:black; margin:10px;">{json_config["headerText"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<h4 style="text-align: center; color: black;"><i>{json_config["descriptionText"]}</i></h4>', unsafe_allow_html=True)
# Putting 5 vertical spaces
avs.add_vertical_space(1)

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path=json_config["logoImagePath"], width=200, height=200)


with st.sidebar:
    st.sidebar.image(my_logo)
    st.title(json_config["listHeaderText"])
    n_rows = 9
    for idx in range(n_rows):
            # print(st.session_state.engine.claims[idx])
            if st.button(st.session_state.engine.claims[idx]["title"]):
                st.session_state.active_page = 1
                st.session_state.selected_claim = idx
                st.session_state.summary: str = None
                st.session_state.next_steps: str = None
                st.session_state.entities: str = None
                st.experimental_rerun()


with st.expander(json_config["whyThisAppHeaderText"]):
     st.write(f"""
              {json_config["whyThisAppDescriptionText"]}
     """) 

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Select a claim
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if st.session_state.active_page == 0:
    n_rows = 3
    n_cols = 3
    for i in range(n_rows):
        cols = st.columns(n_cols)
        for j, col in enumerate(cols):
            claim_idx = i * n_cols + j
            with col:
                
                if st.button(st.session_state.engine.claims[claim_idx]["title"]):
                    st.session_state.active_page = 1
                    st.session_state.selected_claim = claim_idx
                    st.experimental_rerun()
        st.markdown("<hr>", unsafe_allow_html=True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# View a claim
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
elif st.session_state.active_page == 1:
    
    cols = st.columns([1, 2])

    prompt=st.text_area(
        label=json_config["textHeaderText"],
        value=st.session_state.engine.claims[st.session_state.selected_claim]["description"],
        height=300
    )

    cols = st.columns(4)
    with cols[0]:
        if st.button(json_config["summaryButtonText"]):
            summary = st.session_state.engine.query_summary(st.session_state.engine.claims[st.session_state.selected_claim]["description"])
            st.session_state.summary = summary
            st.experimental_rerun()
    with cols[1]:
        if st.button(json_config["nextStepsButtonText"]):
            next_steps = st.session_state.engine.query_next_steps(st.session_state.engine.claims[st.session_state.selected_claim]["description"])
            st.session_state.next_steps = next_steps
            st.experimental_rerun()
    with cols[2]:
        if st.button(json_config["entitiesButtonText"]):
            entities = st.session_state.engine.query_entities(st.session_state.engine.claims[st.session_state.selected_claim]["description"])
            st.session_state.entities = entities
            st.experimental_rerun()

    with cols[3]:
        if st.button(json_config["getInsightsButtonText"]):
            entities, next_steps, summary = st.session_state.engine.query_bam(st.session_state.engine.claims[st.session_state.selected_claim]["description"])
            st.session_state.entities = entities
            st.session_state.next_steps = next_steps
            st.session_state.summary = summary

    if st.session_state.summary is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<b>{json_config["summaryHeaderText"]}</b>: <i>{st.session_state.summary}</i>', unsafe_allow_html=True)
        
    st.markdown("<hr>", unsafe_allow_html=True)
    cols = st.columns([2, 1])
    with cols[0]:
        if st.session_state.next_steps is not None:
            st.markdown(f'<h4>{json_config["nextStepsHeaderText"]}</h4>', unsafe_allow_html=True)
            for next_step in st.session_state.next_steps:
                st.markdown("- " + next_step)
                
    with cols[1]:
        if st.session_state.entities is not None:  
            st.markdown(f'</br> <h4>{json_config["extractedDetailsHeaderText"]}</h4>', unsafe_allow_html=True)  
            st.markdown(f'<b>{json_config["entity1HeaderText"]}</b>: ' + st.session_state.entities[f'{json_config["entity1HeaderText"]}'], unsafe_allow_html=True)
            st.markdown(f'<b>{json_config["entity2HeaderText"]}</b>: ' + st.session_state.entities[f'{json_config["entity2HeaderText"]}'], unsafe_allow_html=True)
            st.markdown(f'<b>{json_config["entity3HeaderText"]}</b>: ' + st.session_state.entities[f'{json_config["entity3HeaderText"]}'], unsafe_allow_html=True)
            st.markdown(f'<b>{json_config["entity4HeaderText"]}</b>: ' + st.session_state.entities[f'{json_config["entity4HeaderText"]}'], unsafe_allow_html=True)

else: 
    st.session_state.active_page = 0
    st.experimental_rerun()


