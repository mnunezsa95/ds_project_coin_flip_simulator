import pandas as pd
import scipy.stats
import streamlit as st
import time

# these are stateful variables; preserved as Streamlin reruns this script
if "experiment_no" not in st.session_state:
    st.session_state["experiment_no"] = 0

if "df_experiment_results" not in st.session_state:
    st.session_state["df_experiment_results"] = pd.DataFrame(
        columns=["no", "iterations", "mean"]
    )

# Header of the application
st.header("Tossing a Coin")

# Chart widget
chart = st.line_chart([0.5])


# function to toss a coin
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None  # Start mean off as null
    outcome_no = 0  # start outcome number as 0
    outcome_1_count = 0  # start count as 0

    for r in trial_outcomes:
        outcome_no += 1  # Add 1 for every iteration
        if r == 1:
            outcome_1_count += 1  # Add 1 if r == 1
        mean = outcome_1_count / outcome_no  # calculate mean
        chart.add_rows([mean])  # add mean to the chart
        time.sleep(0.05)

    return mean  # return the mean value


# Slider Widget
number_of_trials = st.slider("Number of trials?", 1, 1000, 10)
start_button = st.button("Run")


if start_button:  # Run if the start button is True (clicked)
    st.write(f"Running the experient of {number_of_trials} trials.")
    st.session_state["experiment_no"] += 1
    mean = toss_coin(number_of_trials)
    st.session_state["df_experiment_results"] = pd.concat(
        [
            st.session_state["df_experiment_results"],
            pd.DataFrame(
                data=[[st.session_state["experiment_no"], number_of_trials, mean]],
                columns=["no", "iterations", "mean"],
            ),
        ],
        axis=0,
    )
    st.session_state["df_experiment_results"] = st.session_state[
        "df_experiment_results"
    ].reset_index(drop=True)

st.write(st.session_state["df_experiment_results"])
