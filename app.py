import streamlit as st
import pandas as pd
import datetime
import os
import plotly.express as px


RECORDS_PATH = "records/records.csv"

def load_or_create_records():
    if os.path.exists(RECORDS_PATH):
        df = pd.read_csv(RECORDS_PATH, parse_dates=["Date"])
        df["Date"] = df["Date"].dt.date  # Convert to date without time
        return df
    else:
        return pd.DataFrame(columns=["Date", "Balance", "Deposits", "ClearedFunds"])

def format_with_commas(value):
    return f"£{value:,.2f}"

def main():
    st.title("Cleared Cash App")

    today = datetime.date.today()

    # Load existing records or create new DataFrame
    records = load_or_create_records()

    # Check if an entry for today already exists
    if not records[records["Date"] == today].empty:
        st.warning("An entry for today already exists. You can only add one entry per day.")
        can_add_entry = False
    else:
        can_add_entry = True

    # File uploader
    uploaded_file = st.file_uploader("Upload Exported_payments.csv", type="csv")

    if uploaded_file is not None and can_add_entry:
        df = pd.read_csv(uploaded_file)
        active = df[df["Job Status"] == "Active"]
        active_paid = active[active["Status"] == "PAID"]
        deposits = active_paid["Total Amount"].sum()

        # Get current balance from user
        balance = st.number_input("Enter Bank Balance:", min_value=0.0, format="%.2f")

        if st.button("Process"):
            cleared_funds = balance - deposits

            # Display summary
            st.subheader("Summary")
            st.write(f"Balance: {format_with_commas(balance)}")
            st.write(f"Deposits: {format_with_commas(deposits)}")
            st.write(f"Cleared Funds: {format_with_commas(cleared_funds)}")

            # Create new record
            new_record = pd.DataFrame({
                "Date": [today],
                "Balance": [balance],
                "Deposits": [deposits],
                "ClearedFunds": [cleared_funds]
            })

            # Append new record and sort by date
            records = pd.concat([records, new_record], ignore_index=True)
            records["Date"] = pd.to_datetime(records["Date"]).dt.date  # Ensure Date is date type without time
            records = records.sort_values("Date", ascending=False)

            # Save updated records
            records.to_csv(RECORDS_PATH, index=False)

            st.success("New record added successfully!")

    # Display records
    if not records.empty:
        st.subheader("Records")
        st.dataframe(records.style.format({
            "Balance": format_with_commas,
            "Deposits": format_with_commas,
            "ClearedFunds": format_with_commas
        }))

        # Create and display line graph
        st.subheader("Financial Trends")
        fig = px.line(records.sort_values("Date"), x="Date", y=["Balance", "Deposits", "ClearedFunds"],
                      title="Financial Trends Over Time")
        fig.update_layout(yaxis_title="Amount (£)")
        st.plotly_chart(fig)

    else:
        st.info("No records available. Please upload the Exported_payments.csv file and process data to add records.")

if __name__ == "__main__":
    main()
