import streamlit as st
import pandas as pd
import base64
import os

# ==========================================
# PLACEHOLDER CONFIGURATION & MOCK DATA (Ensure these exist in your environment)
# ==========================================
# (Assuming VEHICLE_IMAGES, v_data, selected_name, selected_code, selected_year, 
# selected_bank, bank_rate, down_payment_pct, base_vehicle_price, base_vehicle_vat, 
# total_base_vehicle_price, full_vehicle_value_including_addons, calculated_downpayment, 
# finance_amount, finance_dp_option, checked_addons_list, dp_processing_fee, 
# bank_processing_fee, etc. are defined in your broader app context)

def find_valid_image_path(img_file):
    if os.path.exists(img_file):
        return img_file
    return None

def get_image_base64(resolved_path):
    with open(resolved_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"

# ==========================================
# HTML/PDF REPORT GENERATOR FUNCTION
# ==========================================
def generate_html_report(
    selected_name,
    selected_code,
    selected_year,
    selected_bank,
    bank_rate,
    down_payment_pct,
    base_vehicle_price,
    base_vehicle_vat,
    total_base_vehicle_price,
    full_vehicle_value_including_addons,
    calculated_downpayment,
    finance_amount,
    vehicle_emi_results,
    finance_dp_option,
    dp_results,
    checked_addons_list,
    grand_total_cash_outlay,
    registration_fee,
    dp_processing_fee,
    bank_processing_fee,
    reservation_fee,
    img_b64,
):
    acc_rows_html = ""
    if checked_addons_list:
        for addon in checked_addons_list:
            item_price = addon["price"]
            item_vat = item_price * 0.05 if addon["vat_taxable"] else 0.0
            total_item_cost = item_price + item_vat
            vat_text = (
                f"{item_vat:,.2f} AED"
                if addon["vat_taxable"]
                else "0.00 AED (VAT Pre-incl.)"
            )
            acc_rows_html += f"""
            <tr>
                <td>{addon['name']}</td>
                <td>{item_price:,.2f} AED</td>
                <td>{vat_text}</td>
                <td>{total_item_cost:,.2f} AED</td>
            </tr>
            """
    else:
        acc_rows_html = '<tr><td colspan="4" style="text-align:center;">No optional accessories selected.</td></tr>'

    emi_rows_html = ""
    for row in vehicle_emi_results:
        emi_rows_html += f"""
        <tr>
            <td>{row['Asset Term (Years)']}</td>
            <td>{row['Flat ROI %']}</td>
            <td>{row['Principal Loan Block']}</td>
            <td>{row['Total Interest Accrued']}</td>
            <td>{row['Monthly Vehicle EMI']}</td>
        </tr>
        """

    dp_section_html = ""
    if finance_dp_option and dp_results:
        dp_rows_html = ""
        for opt in dp_results:
            dp_rows_html += f"""
            <tr>
                <td>{opt['Term']}</td>
                <td>{opt['Financed Balance']}</td>
                <td>{opt['Total Interest']}</td>
                <td>{opt['Monthly EMI']}</td>
            </tr>
            """
        dp_section_html = f"""
        <h3>Down Payment Loan Financing Options</h3>
        <table>
            <thead>
                <tr>
                    <th>Term</th>
                    <th>Financed Balance</th>
                    <th>Total Interest</th>
                    <th>Monthly EMI</th>
                </tr>
            </thead>
            <tbody>
                {dp_rows_html}
            </tbody>
        </table>
        """

    img_tag = (
        f'<img src="{img_b64}" alt="Vehicle Image" style="max-width: 350px; display: block; margin: 0 auto 20px auto;" />'
        if img_b64
        else ""
    )

    metrics_grid_html = f"""
    <table style="width: 100%; border-collapse: separate; border-spacing: 15px 0; margin: 20px -15px;">
        <tr>
            <td style="width: 33.33%; background-color: #F4F0EA; padding: 15px; border-radius: 8px; border: none; border-left: 4px solid #191919; vertical-align: top;">
                <div style="font-size: 11px; text-transform: uppercase; color: #555; font-weight: bold; margin-bottom: 5px;">Total Vehicle Value (incl. Addons)</div>
                <div style="font-size: 16px; font-weight: bold; color: #191919;">{full_vehicle_value_including_addons:,.2f} AED</div>
            </td>
            <td style="width: 33.33%; background-color: #F4F0EA; padding: 15px; border-radius: 8px; border: none; border-left: 4px solid #191919; vertical-align: top;">
                <div style="font-size: 11px; text-transform: uppercase; color: #555; font-weight: bold; margin-bottom: 5px;">Gross Down Payment Req.</div>
                <div style="font-size: 16px; font-weight: bold; color: #191919;">{calculated_downpayment:,.2f} AED</div>
            </td>
            <td style="width: 33.33%; background-color: #F4F0EA; padding: 15px; border-radius: 8px; border: none; border-left: 4px solid #191919; vertical-align: top;">
                <div style="font-size: 11px; text-transform: uppercase; color: #555; font-weight: bold; margin-bottom: 5px;">Vehicle Finance Amount</div>
                <div style="font-size: 16px; font-weight: bold; color: #191919;">{finance_amount:,.2f} AED</div>
            </td>
        </tr>
    </table>
    """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Mitsubishi Financial Matrix Report</title>
    <style>
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #191919;
        background-color: #FBF9F6;
        margin: 0;
        padding: 30px;
        line-height: 1.6;
    }}
    .report-container {{
        max-width: 900px;
        margin: auto;
        background: #ffffff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    h1 {{
        text-align: center;
        font-size: 24px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 5px;
    }}
    .subtitle {{
        text-align: center;
        font-size: 14px;
        color: #555;
        margin-bottom: 30px;
    }}
    h2 {{
        font-size: 16px;
        border-bottom: 2px solid #191919;
        padding-bottom: 5px;
        margin-top: 30px;
        text-transform: uppercase;
    }}
    h3 {{
        font-size: 14px;
        margin-top: 20px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 13px;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }}
    th {{
        background-color: #F4F0EA;
        font-weight: bold;
    }}
    .outlay-box {{
        background-color: #F4F0EA;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #191919;
        margin-top: 20px;
    }}
    .checklist-box {{
        background-color: #F4F0EA;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #191919;
        margin-top: 20px;
        font-size: 13px;
    }}
    .print-btn-container {{
        text-align: center;
        margin-bottom: 30px;
    }}
    .print-btn {{
        background-color: #191919;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        border-radius: 4px;
        cursor: pointer;
    }}
    @media print {{
        .print-btn-container {{ display: none; }}
        body {{ background: white; padding: 0; }}
        .report-container {{ box-shadow: none; padding: 0; }}
    }}
    </style>
    </head>
    <body>
    <div class="print-btn-container">
    <button class="print-btn" onclick="window.print()">Print/Save as PDF</button>
    </div>
    <div class="report-container">
    {img_tag}
    <h1>Mitsubishi Financial Matrix Report</h1>
    <div class="subtitle">Unit Selected: {selected_name} - Variant {selected_code} ({selected_year}) | Institution: {selected_bank} | Flat ROI: {bank_rate*100:.4f}%</div>
    
    <h2>1. Base Vehicle Price & Tax Breakdown</h2>
    <table>
    <tr>
    <th>Vehicle Model / Variant</th>
    <th>Base Unit Price (Excl. VAT)</th>
    <th>VAT (5%)</th>
    <th>Total Unit Price (Incl. VAT)</th>
    </tr>
    <tr>
    <td>{selected_name} ({selected_code})</td>
    <td>{base_vehicle_price:,.2f} AED</td>
    <td>{base_vehicle_vat:,.2f} AED</td>
    <td>{total_base_vehicle_price:,.2f} AED</td>
    </tr>
    </table>
    
    {metrics_grid_html}
    
    <h2>2. Loan Installment Breakdowns</h2>
    <h3>Primary Asset Vehicle Financing</h3>
    <table>
    <thead>
    <tr>
    <th>Asset Term (Years)</th>
    <th>Flat ROI %</th>
    <th>Principal Loan Block</th>
    <th>Total Interest Accrued</th>
    <th>Monthly Vehicle EMI</th>
    </tr>
    </thead>
    <tbody>
    {emi_rows_html}
    </tbody>
    </table>
    {dp_section_html}
    
    <h2>3. Accessories Breakdown</h2>
    <table>
    <thead>
    <tr>
    <th>Selected Accessories / Services</th>
    <th>Individual Price (Base)</th>
    <th>VAT Amount (5%)</th>
    <th>Total Cost (incl. VAT)</th>
    </tr>
    </thead>
    <tbody>
    {acc_rows_html}
    </tbody>
    </table>
    
    <h2>4. Out-of-Pocket Cash Outlay Summary</h2>
    <p>
    <strong>Showroom Reservation Fee:</strong> {reservation_fee:,.2f} AED<br>
    <strong>Registration Documentation Fee:</strong> {registration_fee:,.2f} AED<br>
    <strong>DP Processing Fee (DP PF):</strong> {dp_processing_fee:,.2f} AED<br>
    <strong>Bank Processing Fee (Bank PF):</strong> {bank_processing_fee:,.2f} AED
    </p>
    <div class="outlay-box">
    <span style="font-size: 11px; text-transform: uppercase; color: #555; font-weight: bold; display: block;">Actual Upfront Cash Required at Showroom Handover</span>
    <span style="font-size: 22px; font-weight: bold; color: #191919;">{grand_total_cash_outlay:,.2f} AED</span>
    </div>
    
    <h2>5. Application Requirements & Disclosures</h2>
    <div class="checklist-box">
    <strong>Required Documentation Checklist:</strong>
    <ul>
    <li>Passport Copy, Digital Visa & Address Page For Indian Passport, Page #44 For Philippines Passport.</li>
    <li>Emirates ID Card Copy Both Sides.</li>
    <li>Labour Card / Free Zone / Employer ID.</li>
    <li>Copy of the UAE Driver's License Both Sides.</li>
    <li>Current Dated Salary Certificate from The Employer.</li>
    <li>Pay Slips For The Last 3 Months (Or 6 Months For Commission-Based Income).</li>
    <li>IBAN.</li>
    </ul>
    <p style="font-size: 11px; color: #555; margin-top: 10px;">
    <strong>Disclaimer:</strong> All calculations, rates, and figures provided by this matrix calculator are for estimation purposes only and subject to formal bank approval, final credit evaluation, and prevailing regulatory changes in the UAE.
    </p>
    </div>
    </div>
    </body>
    </html>
    """
    return html_content


# ==========================================
# MAIN WORKSPACE RENDERING
# ==========================================
if "view_state" not in st.session_state:
    st.session_state.view_state = "summary"

if st.session_state.view_state == "input":
    st.title("Mitsubishi Financial Dashboard")
    st.info(
        "Configure variables in the sidebar panel. Then click **'Generate Summary'** to view the calculation report."
    )
elif st.session_state.view_state == "summary":
    st.title("Mitsubishi Financial Matrix Calculator")
    
    # Dummy mock context variables for fallback instantiation if not declared globally
    selected_name = globals().get("selected_name", "Xpander")
    selected_code = globals().get("selected_code", "AT")
    selected_year = globals().get("selected_year", "2026")
    selected_bank = globals().get("selected_bank", "CBD")
    bank_rate = globals().get("bank_rate", 0.035)
    down_payment_pct = globals().get("down_payment_pct", 0.20)
    base_vehicle_price = globals().get("base_vehicle_price", 75000.0)
    base_vehicle_vat = globals().get("base_vehicle_vat", 3750.0)
    total_base_vehicle_price = globals().get("total_base_vehicle_price", 78750.0)
    full_vehicle_value_including_addons = globals().get("full_vehicle_value_including_addons", 80000.0)
    calculated_downpayment = globals().get("calculated_downpayment", 16000.0)
    finance_amount = globals().get("finance_amount", 64000.0)
    finance_dp_option = globals().get("finance_dp_option", False)
    checked_addons_list = globals().get("checked_addons_list", [])
    dp_processing_fee = globals().get("dp_processing_fee", 500.0)
    bank_processing_fee = globals().get("bank_processing_fee", 1050.0)
    v_data = globals().get("v_data", {"reservation_fee": 1000.0, "registration_fee": 500.0})

    st.subheader(
        f"Unit Selected: {selected_name} - Variant {selected_code} ({selected_year})"
    )

    lookup_name = (
        "Xpander Cross"
        if (
            selected_name == "Xpander"
            and str(selected_code).strip().upper() == "XC"
        )
        else selected_name
    )

    img_b64 = None
    if 'VEHICLE_IMAGES' in globals() and lookup_name in VEHICLE_IMAGES:
        img_file = VEHICLE_IMAGES[lookup_name]
        resolved_path = find_valid_image_path(img_file)
        if resolved_path:
            st.image(resolved_path, width=420)
            img_b64 = get_image_base64(resolved_path)

    st.markdown("---")

    # Pre-calculate EMI results for UI and HTML generation
    tenures = [1, 2, 3, 4, 5]
    vehicle_emi_results = []
    for years in tenures:
        months = years * 12
        total_interest = finance_amount * bank_rate * years
        monthly_emi = (finance_amount + total_interest) / months
        vehicle_emi_results.append({
            "Asset Term (Years)": f"{years} Years ({months} Mos)",
            "Flat ROI %": f"{bank_rate*100:.4f}%",
            "Principal Loan Block": f"{finance_amount:,.2f} AED",
            "Total Interest Accrued": f"{total_interest:,.2f} AED",
            "Monthly Vehicle EMI": f"{monthly_emi:,.2f} AED",
        })

    dp_results = []
    if finance_dp_option:
        vehicle_reservation_fee = v_data["reservation_fee"]
        dp_financed_base = max(
            0.0, calculated_downpayment - vehicle_reservation_fee
        )
        dp_options = [
            {"months": 3, "rate": 0.0000, "label": "3 Months (0.00% ROI)"},
            {"months": 12, "rate": 0.0525, "label": "12 Months (5.25% ROI)"},
            {"months": 24, "rate": 0.0630, "label": "24 Months (6.30% ROI)"},
        ]
        for opt in dp_options:
            total_interest = (
                dp_financed_base * opt["rate"] * (opt["months"] / 12.0)
            )
            monthly_emi = (dp_financed_base + total_interest) / opt["months"]
            dp_results.append({
                "Term": opt["label"],
                "Financed Balance": f"{dp_financed_base:,.2f} AED",
                "Total Interest": f"{total_interest:,.2f} AED",
                "Monthly EMI": f"{monthly_emi:,.2f} AED",
            })

    registration_fee = v_data["registration_fee"]
    if finance_dp_option:
        vehicle_reservation_fee = v_data["reservation_fee"]
        grand_total_cash_outlay = (
            vehicle_reservation_fee
            + registration_fee
            + dp_processing_fee
            + bank_processing_fee
        )
    else:
        grand_total_cash_outlay = (
            calculated_downpayment
            + registration_fee
            + dp_processing_fee
            + bank_processing_fee
        )

    report_html = generate_html_report(
        selected_name=selected_name,
        selected_code=selected_code,
        selected_year=selected_year,
        selected_bank=selected_bank,
        bank_rate=bank_rate,
        down_payment_pct=down_payment_pct,
        base_vehicle_price=base_vehicle_price,
        base_vehicle_vat=base_vehicle_vat,
        total_base_vehicle_price=total_base_vehicle_price,
        full_vehicle_value_including_addons=full_vehicle_value_including_addons,
        calculated_downpayment=calculated_downpayment,
        finance_amount=finance_amount,
        vehicle_emi_results=vehicle_emi_results,
        finance_dp_option=finance_dp_option,
        dp_results=dp_results,
        checked_addons_list=checked_addons_list,
        grand_total_cash_outlay=grand_total_cash_outlay,
        registration_fee=registration_fee,
        dp_processing_fee=dp_processing_fee,
        bank_processing_fee=bank_processing_fee,
        reservation_fee=v_data["reservation_fee"],
        img_b64=img_b64,
    )

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Download Report as HTML",
            data=report_html,
            file_name=f"Mitsubishi_Financial_Matrix_{selected_name}_{selected_code}.html",
            mime="text/html",
            use_container_width=True,
        )
    with col_dl2:
        if st.button("Back to Calculator Inputs", use_container_width=True):
            st.session_state.view_state = "input"
            st.rerun()

    st.markdown("---")

    # SECTION 1: BASE VEHICLE PRICE & VAT BREAKDOWN
    st.header("1. Base Vehicle Price & Tax Breakdown")
    base_price_df = pd.DataFrame([{
        "Vehicle Model / Variant": f"{selected_name} ({selected_code})",
        "Base Unit Price (Excl. VAT)": f"{base_vehicle_price:,.2f} AED",
        "VAT (5%)": f"{base_vehicle_vat:,.2f} AED",
        "Total Unit Price (Incl. VAT)": f"{total_base_vehicle_price:,.2f} AED",
    }])
    st.table(base_price_df)

    # FINANCIAL OVERVIEW METRICS (Styled to match Actual Upfront Cash Box)
    st.subheader("Financial Overview")
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown(f"""
        <div style="background-color: #F4F0EA; padding: 1.25rem 1.5rem; border-radius: 8px; border-left: 4px solid #191919; margin-top: 0.5rem; height: 100%;">
            <span style="font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 0.85rem; color: #555555; display: block; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Total Vehicle Value (incl. Addons)
            </span>
            <span style="font-family: 'Amethysta', serif; font-size: 1.5rem; color: #191919;">
                {full_vehicle_value_including_addons:,.2f} <span style="font-size: 1rem;">AED</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div style="background-color: #F4F0EA; padding: 1.25rem 1.5rem; border-radius: 8px; border-left: 4px solid #191919; margin-top: 0.5rem; height: 100%;">
            <span style="font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 0.85rem; color: #555555; display: block; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Gross Down Payment Req.
            </span>
            <span style="font-family: 'Amethysta', serif; font-size: 1.5rem; color: #191919;">
                {calculated_downpayment:,.2f} <span style="font-size: 1rem;">AED</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""
        <div style="background-color: #F4F0EA; padding: 1.25rem 1.5rem; border-radius: 8px; border-left: 4px solid #191919; margin-top: 0.5rem; height: 100%;">
            <span style="font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 0.85rem; color: #555555; display: block; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Vehicle Finance Amount
            </span>
            <span style="font-family: 'Amethysta', serif; font-size: 1.5rem; color: #191919;">
                {finance_amount:,.2f} <span style="font-size: 1rem;">AED</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # SECTION 2: EMI BREAKDOWN MATRIX
    st.header("2. Loan Installment Breakdowns")
    st.subheader("Primary Asset Vehicle Financing")
    st.table(pd.DataFrame(vehicle_emi_results))

    if finance_dp_option:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Down Payment Loan Financing Options")
        st.table(pd.DataFrame(dp_results))

    st.markdown("---")

    # SECTION 3: ACCESSORIES BREAKDOWN
    st.header("3. Accessories Breakdown")
    addons_table_data = []
    if checked_addons_list:
        for addon in checked_addons_list:
            item_price = addon["price"]
            item_vat = (item_price * 0.05) if addon["vat_taxable"] else 0.0
            addons_table_data.append({
                "Selected Accessories / Services": addon["name"],
                "Individual Price (Base)": f"{item_price:,.2f} AED",
                "VAT Amount (5%)": (
                    f"{item_vat:,.2f} AED"
                    if addon["vat_taxable"]
                    else "0.00 AED (VAT Pre-incl.)"
                ),
                "Total Cost (incl. VAT)": f"{(item_price + item_vat):,.2f} AED",
            })
        st.table(pd.DataFrame(addons_table_data))
    else:
        st.write("*No optional accessories selected.*")

    st.markdown("---")

    # SECTION 4: TOTAL CASH OUTLAY REQUIRED
    st.header("4. Out-of-Pocket Cash Outlay Summary")
    col_out1, col_out2 = st.columns(2)
    with col_out1:
        if finance_dp_option:
            st.write(
                f"**Showroom Reservation Fee:** {v_data['reservation_fee']:,.2f} AED (Paid Upfront)"
            )
            st.write(
                f"**Remaining Down Payment Balance:** {max(0.0, calculated_downpayment - v_data['reservation_fee']):,.2f} AED (Financed via Loan Plan)"
            )
        else:
            st.write(
                f"**Full Down Payment Amount:** {calculated_downpayment:,.2f} AED (Upfront Out-of-Pocket)"
            )
        st.write(
            f"**Registration Documentation Fee:** {registration_fee:,.2f} AED"
        )
    with col_out2:
        st.write(f"**DP Processing Fee (DP PF):** {dp_processing_fee:,.2f} AED")
        st.write(f"**Bank Processing Fee (Bank PF):** {bank_processing_fee:,.2f} AED")

    st.markdown(
        f"""
        <div style="background-color: #F4F0EA; padding: 1.25rem 1.5rem; border-radius: 8px; border-left: 4px solid #191919; margin-top: 1.5rem;">
        <span style="font-family: 'Quicksand', sans-serif; font-weight: 700; font-size: 0.9rem; color: #555555; display: block; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
        Actual Upfront Cash Required at Showroom Handover
        </span>
        <span style="font-family: 'Amethysta', serif; font-size: 1.8rem; color: #191919;">
        {grand_total_cash_outlay:,.2f} <span style="font-size: 1.2rem;">AED</span>
        </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # SECTION 5: DOCUMENTATION REQUIREMENTS & DISCLOSURES
    st.header("5. Application Requirements & Disclosures")
    st.markdown(
        """
        <div style="background-color: #F4F0EA; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #191919; margin-top: 1.5rem;">
        <strong style="font-family: sans-serif; font-size: 1.1rem; color: #191919; display: block; margin-bottom: 0.75rem;">Required Documentation Checklist:</strong>
        <ul style="margin-bottom: 1rem; padding-left: 1.25rem;">
        <li>Passport Copy, Digital Visa & Address Page For Indian Passport, Page #44 For Philippines Passport.</li>
        <li>Emirates ID Card Copy Both Sides.</li>
        <li>Labour Card / Free Zone / Employer ID.</li>
        <li>Copy of the UAE Driver's License Both Sides.</li>
        <li>Current Dated Salary Certificate from The Employer.</li>
        <li>Pay Slips For The Last 3 Months (Or 6 Months For Commission-Based Income).</li>
        <li>IBAN.</li>
        </ul>
        <div class="disclaimer-text">
        <strong>Disclaimer:</strong> All calculations, rates, and figures provided by this matrix calculator are for estimation purposes only and subject to formal bank approval, final credit evaluation, and prevailing regulatory changes in the UAE.
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
