import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df
from matplotlib import pyplot as plt

from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Diabetes Dashboard", fillable=True)


with ui.sidebar(title="Filter controls"):
    ui.input_slider("year", "Year", min=2015, max=2022, step=1, value=(2015, 2022))

    ui.input_checkbox_group(
        "race",
        "Race",
        choices=["AfricanAmerican", "Asian", "Caucasian", "Hispanic", "Other"],
        selected=["AfricanAmerican", "Asian", "Caucasian", "Hispanic", "Other"],
    )

    ui.input_checkbox_group(
        "gender",
        "Gender",
        choices=["Male", "Female", "Other"],
        selected=["Male", "Female", "Other"],
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("chart-pie")):
        "Presentase Penderita Diabetes"

        @render.text
        def count_diabetes():
            return f"{filtered_df()['diabetes'].mean() * 100:.1f}%"

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Rata-rata Umur Penderita Diabetes"

        @render.text
        def average_age_diabetes():
            return f"{filtered_df()[filtered_df()['diabetes'] == 1]['age'].mean():.1f}"
        
        # def count_age_affected_by_diabetes():
        #     return f"{filtered_df()[filtered_df()['diabetes'] == 1]['age'].mean():.1f}"
        

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Rata-rata Gula Darah Penderita Diabetes"

        @render.text
        def average_glucose_diabetes():
            return f"{filtered_df()[filtered_df()['diabetes'] == 1]['blood_glucose_level'].mean():.1f} mg/dL"


with ui.layout_columns(min_height="80vh"):
    with ui.card(full_screen=True):
        ui.card_header("Jumlah Kasus Diabetes per Tahun")

        count_diabetes_by_year = 'count_diabetes_by_year'

        @render.plot
        def length_depth():
            return sns.lineplot(
                data=filtered_df(),
                x="year",
                y="diabetes",
                estimator=sum,
                errorbar=None,
            )

    with ui.card(full_screen=True):
        ui.card_header("Data Diabetes")

        @render.data_frame
        def summary_statistics():
            cols = [
                "year",
                "gender",
                "age",
                "bmi",
                "hbA1c_level",
                "location",
                "diabetes",
                "blood_glucose_level",
                "race",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)
        
with ui.layout_columns(min_height="50vh"):
    # Add Gender Pie Chart
    with ui.card(full_screen=True):
        ui.card_header("Jumlah Kasus Diabetes per Gender")

        @render.plot
        def gender_pie_chart():
            gender_counts = filtered_df()["gender"].value_counts()
            return plt.pie(
                gender_counts,
                labels=gender_counts.index,
                autopct='%1.1f%%',
                startangle=140
        )
    with ui.card(full_screen=True):
        ui.card_header("Jumlah Kasus Berdasarkan Ras")

        @render.plot
        def gender_pie_race():
            race_counts = filtered_df()["race"].value_counts()
            return plt.pie(
                race_counts,
                labels=race_counts.index,
                autopct='%1.1f%%',
                startangle=140
        )

    with ui.card(full_screen=True):
        ui.card_header("Jumlah penderita diabetes dan Perokok")

        @render.plot
        def diabetes_smoker():
            return plt.pie(
                filtered_df()["smoking_history"].value_counts(),
                labels=filtered_df()["smoking_history"].value_counts().index,
                autopct='%1.1f%%',
                startangle=140
            )

with ui.layout_columns(min_height="80vh"):
    # Distribution of Age
    with ui.card(full_screen=True):
        ui.card_header("Distribusi Umur Penderita Diabetes")

        @render.plot
        def age_distribution():
            return sns.histplot(
                data=filtered_df(),
                x="age",
                hue="diabetes",
                multiple="stack",
                bins=20,
            )
    
    with ui.card(full_screen=True):
        ui.card_header("Distribusi BMI Penderita Diabetes")

        @render.plot
        def bmi_distribution():
            return sns.histplot(
                data=filtered_df(),
                x="bmi",
                hue="diabetes",
                multiple="stack",
                bins=20,
            )
        
with ui.layout_columns(min_height="80vh"):
     with ui.card(full_screen=True):
        ui.card_header("Blood Glucose Level Distribution")

        @render.plot
        def blood_glucose_level_distribution():
            return sns.histplot(
                data=filtered_df(),
                x="blood_glucose_level",
                hue="diabetes",
                multiple="stack",
                bins=20,
            )

ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[
        (df["year"] >= input.year()[0]) & 
        (df["year"] <= input.year()[1]) &
        df["race"].str.replace("race:", "").isin(input.race()) &
        df["gender"].isin(input.gender())
    ]
    return filt_df


#  python -m shiny run .\app.py