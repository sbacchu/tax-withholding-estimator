import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import streamlit as st

def calculate_tax(income, filing_status, dependents):
    # Simple tax brackets for example purposes (US Tax Brackets for 2023)
    tax_brackets = {
        "single": [(10275, 0.10), (41775, 0.12), (89075, 0.22), (170050, 0.24), (215950, 0.32), (539900, 0.35), (float('inf'), 0.37)],
        "married_joint": [(20550, 0.10), (83550, 0.12), (178150, 0.22), (340100, 0.24), (431900, 0.32), (647850, 0.35), (float('inf'), 0.37)],
        "married_separate": [(10275, 0.10), (41775, 0.12), (89075, 0.22), (170050, 0.24), (215950, 0.32), (323925, 0.35), (float('inf'), 0.37)],
        "head_of_household": [(14650, 0.10), (55900, 0.12), (89050, 0.22), (170050, 0.24), (215950, 0.32), (539900, 0.35), (float('inf'), 0.37)]
    }

    standard_deductions = {
        "single": 12950,
        "married_joint": 25900,
        "married_separate": 12950,
        "head_of_household": 19400
    }

    taxable_income = max(0, income - standard_deductions[filing_status] - (dependents * 2000))

    tax = 0
    for bracket in tax_brackets[filing_status]:
        if taxable_income > bracket[0]:
            tax += bracket[0] * bracket[1]
            taxable_income -= bracket[0]
        else:
            tax += taxable_income * bracket[1]
            break

    return tax

def main():
    st.title("Tax Withholding Estimator")

    income = st.number_input("Annual Income ($)", min_value=0)
    filing_status = st.selectbox("Filing Status", ["single", "married_joint", "married_separate", "head_of_household"])
    dependents = st.number_input("Number of Dependents", min_value=0)
    current_withholding = st.number_input("Current Annual Withholding ($)", min_value=0)

    if st.button("Calculate"):
        estimated_tax = calculate_tax(income, filing_status, dependents)
        withholding_difference = current_withholding - estimated_tax

        st.write(f"**Estimated Tax Liability:** ${estimated_tax:,.2f}")
        if withholding_difference > 0:
            st.write(f"**You are over-withholding by:** ${withholding_difference:,.2f}")
            st.write("Consider reducing your withholding to increase your take-home pay.")
        else:
            st.write(f"**You are under-withholding by:** ${-withholding_difference:,.2f}")
            st.write("Consider increasing your withholding to avoid a tax bill at the end of the year.")

if __name__ == "__main__":
    main()

