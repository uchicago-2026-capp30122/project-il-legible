import pandas as pd
import altair as alt

FILENAME = "../final_data/sponsors.csv"
main_df = pd.read_csv(FILENAME)
MAIN_COLOR = "maroon"
SIZE = 60

def total_donations_hist(df):

    chart = (
        alt.Chart(df)
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x = alt.X(
                "total_all",
                title="Total Donation Amounts",
                bin=alt.Bin(maxbins=50),
                axis=alt.Axis(
                    tickMinStep=2_000_000,
                    labelExpr="datum.value % 10000000 === 0 ? format(datum.value, '~s') : ''")
                    ),
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False))
            )
        .properties(title=f"Total Donation Amounts of Primary Sponsors in 102nd & 103rd Sessions")
        )
    
    return chart


def average_donation_hist(df):

    chart = (
        alt.Chart(df)
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x = alt.X(
                "avg_donation_all",
                title="Average Donation Amount",
                bin=alt.Bin(maxbins=50),
                axis=alt.Axis(format="~s")
                ),
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False))
                )
        .properties(title=f"Average Donation Amount of Primary Sponsors in 102nd & 103rd Sessions")
        )
    
    return chart

def num_bills_total_donations_scatter(df):
    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )

    base = (
        alt.Chart(df)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.total_all : datum.total_L3"
            )
        )

    points = (
        base
        .mark_circle(size=SIZE, color=MAIN_COLOR)
        .encode(
            x = alt.X("donation_x:Q", title="Total Donation Amount"),
            y = alt.Y("num_bills", title="Number of Bills Introduced"),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("total_all", title="All-time Donations"),
                alt.Tooltip("total_L3", title="Last 3 years Donations"),
                alt.Tooltip("num_bills", title="Bills Introduced")
                ]
            )
        )
    
    line = (
        base
        .transform_regression("donation_x", "num_bills")
        .mark_line(color="black")
        .encode(
            x = "donation_x:Q",
            y = "num_bills:Q"
        )
    )

    chart = (
        (points + line)
        .interactive()
        .properties(title="Total Donations vs Number of Bills Introduced in 102nd & 103rd Sessions")
    )

    return chart

def num_bills_total_donations_scatter_wo_outliers(df):
    df_filtered = df[~df["name"].isin(["Emanuel Welch", "Don Harmon"])]
    
    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )

    base = (
        alt.Chart(df_filtered)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.total_all : datum.total_L3"
            )
        )

    points = (
        base
        .mark_circle(size=SIZE, color=MAIN_COLOR)
        .encode(
            x = alt.X("donation_x:Q", title="Total Donation Amount"),
            y = alt.Y("num_bills", title="Number of Bills Introduced"),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("total_all", title="All-time Donations"),
                alt.Tooltip("total_L3", title="Last 3 years Donations"),
                alt.Tooltip("num_bills", title="Bills Introduced")
                ]
            )
        )
    
    line = (
        base
        .transform_regression("donation_x", "num_bills")
        .mark_line(color="black")
        .encode(
            x = "donation_x:Q",
            y = "num_bills:Q"
        )
    )

    chart = (
        (points + line)
        .interactive()
        .properties(title="Total Donations vs Number of Bills Introduced in 102nd & 103rd Sessions")
    )

    return chart


def bills_introduced_legislator(df: pd.DataFrame, name: str) -> alt.Chart:
    """
    Create a bar graph showing the number of bills introduced by a specific legislator
    compared to an average.

    Inputs:
        df: Dataframe with legislator and bill data
        name: Legislator's name
    
    Returns:
        An Altair Chart
    """
    legislator_bills = df[df["name"] == name]["num_bills"].mean()
    median_bills = df["num_bills"].median()

    legislator_df = pd.DataFrame({
        "names": ["Median", name],
        "num_bills": [median_bills, legislator_bills]
    })
    
    chart=(
        alt.Chart(legislator_df)
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x = alt.X("names", title="Legislator", axis=alt.Axis(labelAngle=0)),
            y = alt.Y("num_bills", title="Number of Bills Introduced"))
        .properties(title="Bills Introduced in 102nd & 103rd Sessions",
            width = 300,
            height = 400
        )
    )

    return chart


def bill_success_legislator(df: pd.DataFrame, name: str) -> alt.Chart:
    """
    Create a pie chart (my apologies in advance) showing the number of bills 
    introduced by a specific legislator compared to an average.

    Inputs:
        df: Dataframe with legislator and bill data
        name: Legislator's name
    
    Returns:
        An Altair Chart
    """
    legislator_passed = df[df["name"] == name]["pct_bills_passed"].mean()

    bill_success_df = pd.DataFrame({
        "Legend": ["Passed", "Failed"],
        "num_bills": [legislator_passed, 1 - legislator_passed]
    })

    base=(
        alt.Chart(bill_success_df)
        .encode(
            theta="num_bills",
            color=alt.Color(
                "Legend",
                scale=alt.Scale(
                    domain=["Passed", "Failed"],
                    range=["#062F8E", "#7C7C7C"]
                    ),
                legend=alt.Legend(
                    titleFontSize=18,
                    labelFontSize=18
                    )
                ))   
        .properties(title="Bill Passage",
            width = 200,
            height = 250
        )
    )

    pie = base.mark_arc(color=MAIN_COLOR, outerRadius= 100)
    # text = base.mark_text(radius=120, size=20).encode(text="num_bills")

    return pie

def num_bills_entity_donations_scatter(df):
    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )

    base = (
        alt.Chart(df)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.amt_allcond_all : datum.amt_allcond_L3"
            )
        )

    points = (
        base
        .mark_circle(size=SIZE, color=MAIN_COLOR)
        .encode(
            x = alt.X("donation_x:Q", title="Donation Amount from Entities"),
            y = alt.Y("num_bills", title="Number of Bills Introduced"),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("amt_allcond_all", title="All-time Entity Donations"),
                alt.Tooltip("amt_allcond_L3", title="Last 3 years Entity Donations"),
                alt.Tooltip("num_bills", title="Bills Introduced")
                ]
            )
        )
    
    line = (
        base
        .transform_regression("donation_x", "num_bills")
        .mark_line(color="black")
        .encode(
            x = "donation_x:Q",
            y = "num_bills:Q"
        )
    )

    chart = (
        (points + line)
        .interactive()
        .properties(title="Entity Donations vs Number of Bills Introduced in 102nd & 103rd Sessions")
    )

    return chart

def bill_passage_pct_entity_donations_scatter(df):
    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )

    base = (
        alt.Chart(df)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.pct_c_allcond_all : datum.pct_c_allcond_L3"
            )
        )

    points = (
        base
        .mark_circle(size=SIZE, color=MAIN_COLOR)
        .encode(
            x = alt.X("donation_x:Q", title="Percentage of Donation Counts from Entities"),
            y = alt.Y("pct_bills_passed", title="Bill Passage Rate"),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("pct_c_allcond_all", title="All-time Entity Donation Percentage"),
                alt.Tooltip("pct_c_allcond_L3", title="Last 3 years Entity Donation Percentage"),
                alt.Tooltip("pct_bills_passed", title="Bill Passage Rate")
                ]
            )
        )
    
    line = (
        base
        .transform_regression("donation_x", "pct_bills_passed")
        .mark_line(color="black")
        .encode(
            x = "donation_x:Q",
            y = "pct_bills_passed:Q"
        )
    )

    chart = (
        (points + line)
        .interactive()
        .properties(title="Entity Donation Percentage vs Bill Passage Rate in 102nd & 103rd Sessions")
    )

    return chart

def large_donation_barchart(df, name):
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": ["Large Donations", "Small Donations"],
        "percent_all": [
            float(person["pct_c_above_all"]) * 100,
            100 - float(person["pct_c_above_all"]) * 100
        ],
        "percent_L3": [
            float(person["pct_c_above_L3"]) * 100,
            100 - float(person["pct_c_above_L3"]) * 100
        ],
    })

    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )
    
    base = (
        alt.Chart(chart_df)
        .add_params(donation_choice)
        .transform_calculate(
            pct_selected="DonationWindow == 'All time' ? datum.percent_all : datum.percent_L3"
        )
    )

    bars = (
        base
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x=alt.X(
                "pct_selected:Q",
                title="",
                scale=alt.Scale(domain=[0,100]),
                axis=alt.Axis(grid=False)
                ),
            y=alt.Y("category:N", title="")
            )
        )
    
    labels = (
        base
        .mark_text(
            align="left",
            dx=3
        )
        .encode(
            x="pct_selected:Q",
            y="category:N",
            text=alt.Text("pct_selected:Q", format=".1f")
        )
    )
    
    chart = (bars + labels).properties(title=f"Percentage of Large vs Small Donations for {name}")
        
    return chart

def entity_donation_barchart(df, name):
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": ["Entity Donations", "Individual Donations"],
        "percent_all": [
            float(person["pct_c_allcond_all"]) * 100,
            100 - float(person["pct_c_allcond_all"]) * 100
        ],
        "percent_L3": [
            float(person["pct_c_allcond_L3"]) * 100,
            100 - float(person["pct_c_allcond_L3"]) * 100
        ],
    })

    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )
    
    base = (
        alt.Chart(chart_df)
        .add_params(donation_choice)
        .transform_calculate(
            pct_selected="DonationWindow == 'All time' ? datum.percent_all : datum.percent_L3"
        )
    )

    bars = (
        base
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x=alt.X(
                "pct_selected:Q",
                title="",
                scale=alt.Scale(domain=[0,100]),
                axis=alt.Axis(grid=False)
                ),
            y=alt.Y("category:N", title="")
            )
        )
    
    labels = (
        base
        .mark_text(
            align="left",
            dx=3
        )
        .encode(
            x="pct_selected:Q",
            y="category:N",
            text=alt.Text("pct_selected:Q", format=".1f")
        )
    )
    
    chart = (bars + labels).properties(title=f"Percentage of Entity vs Individual Donations for {name}")
        
    return chart

def in_state_donation_barchart(df, name):
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": ["In-State Donations", "Out-of-State Donations"],
        "percent_all": [
            float(person["pct_c_IL_all"]) * 100,
            100 - float(person["pct_c_IL_all"]) * 100
        ],
        "percent_L3": [
            float(person["pct_c_IL_L3"]) * 100,
            100 - float(person["pct_c_IL_L3"]) * 100
        ],
    })

    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )
    
    base = (
        alt.Chart(chart_df)
        .add_params(donation_choice)
        .transform_calculate(
            pct_selected="DonationWindow == 'All time' ? datum.percent_all : datum.percent_L3"
        )
    )

    bars = (
        base
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x=alt.X(
                "pct_selected:Q",
                title="",
                scale=alt.Scale(domain=[0,100]),
                axis=alt.Axis(grid=False)
                ),
            y=alt.Y("category:N", title="")
            )
        )
    
    labels = (
        base
        .mark_text(
            align="left",
            dx=3
        )
        .encode(
            x="pct_selected:Q",
            y="category:N",
            text=alt.Text("pct_selected:Q", format=".1f")
        )
    )
    
    chart = (bars + labels).properties(title=f"Percentage of In-State vs Out-of-State Donations for {name}")
        
    return chart



if __name__ == "__main__":
    chart1 = total_donations_hist(main_df)
    chart1.save("total_donations_hist.html")
    print("Saved chart to total_donations_hist.html")

    chart2 = average_donation_hist(main_df)
    chart2.save("average_donation_hist.html")
    print("Saved chart to average_donation_hist.html")

    chart3 = num_bills_total_donations_scatter(main_df)
    chart3.save("num_bills_total_donations_scatter.html")
    print("Saved chart to num_bills_total_donations_scatter.html")

    chart4 = num_bills_total_donations_scatter_wo_outliers(main_df)
    chart4.save("num_bills_total_donations_scatter_wo_outliers.html")
    print("Saved chart to num_bills_total_donations_scatter_wo_outliers.html")

    chart5 = bills_introduced_legislator(main_df, "Omar Aquino")
    chart5.save("bills_introduced_legislator.html")
    print("Saved chart to bills_introduced_legislator.html")

    # We need to fix the labels (or move away from a pie chart)
    chart6 = bill_success_legislator(main_df, "Omar Aquino")
    chart6.save("bill_success_legislator.html")
    print("Saved chart to bill_success_legislator.html")

    chart7 = num_bills_entity_donations_scatter(main_df)
    chart7.save("num_bills_entity_donations_scatter.html")
    print("Saved chart to num_bills_entity_donations_scatter.html")

    chart8 = bill_passage_pct_entity_donations_scatter(main_df)
    chart8.save("bill_passage_pct_entity_donations_scatter.html")
    print("Saved chart to bill_passage_pct_entity_donations_scatter.html")

    chart9 = large_donation_barchart(main_df, "Deb Conroy")
    chart9.save("large_donation_barchart.html")
    print("Saved chart to large_donation_barchart.html")

    chart10 = entity_donation_barchart(main_df, "Deb Conroy")
    chart10.save("entity_donation_barchart.html")
    print("Saved chart to lentity_donation_barchart.html")

    chart11 = in_state_donation_barchart(main_df, "Deb Conroy")
    chart11.save("in_state_donation_barchart.html")
    print("Saved chart to in_state_donation_barchart.html")