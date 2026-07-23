import base64
from io import BytesIO
from PIL import Image
import streamlit as st

# --- Helper Function to Convert Image to Base64 ---
def get_image_base64(image_path_or_pil):
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil)
    else:
        img = image_path_or_pil
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# --- HTML Report Generator Function ---
def generate_html_report(vehicle_img_b64):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Mitsubishi Financial Matrix Report - Destinator (PR)</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333333;
                line-height: 1.4;
                margin: 20px;
                background-color: #ffffff;
            }}
            .header-container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #cc0000;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .header-title h1 {{
                color: #cc0000;
                margin: 0;
                font-size: 24px;
            }}
            .header-title p {{
                margin: 5px 0 0 0;
                font-size: 14px;
                color: #555555;
            }}
            .vehicle-img {{
                max-width: 280px;
                height: auto;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            h2 {{
                color: #222222;
                font-size: 16px;
                border-bottom: 1px solid #cccccc;
                padding-bottom: 5px;
                margin-top: 25px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 15px;
                font-size: 13px;
            }}
            th, td {{
                border: 1px solid #dddddd;
                padding: 8px 10px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
                color: #222222;
            }}
            .highlight-box {{
                background-color: #f9f9f9;
                border-left: 4px solid #cc0000;
                padding: 10px 15px;
                margin-bottom: 15px;
                font-size: 14px;
            }}
            .highlight-box p {{
                margin: 4px 0;
            }}
            ul {{
                margin: 5px 0;
                padding-left: 20px;
                font-size: 13px;
            }}
            li {{
                margin-bottom: 4px;
            }}
            @media print {{
                body {{
                    margin: 0;
                    background-color: #ffffff;
                }}
                .no-print {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>

        <div class="header-container">
            <div class="header-title">
                <h1>📄 Mitsubishi Financial Matrix Report</h1>
                <p><strong>Unit Selected:</strong> Destinator — Variant PR (2026)</p>
                <p><strong>Financial Institution:</strong> DIB Expat</p>
                <p><strong>Flat Interest Rate (ROI):</strong> 2.5000%</p>
                <p><strong>Down Payment Ratio:</strong> 20%</p>
            </div>
            <div>
                <img src="{vehicle_img_b64}" alt="Destinator Variant PR" class="vehicle-img">
            </div>
        </div>

        <h2>1. Base Vehicle Price & Tax Breakdown</h2>
        <table>
            <tr>
                <th>Vehicle Model / Variant</th>
                <th>Base Unit Price (Excl. VAT)</th>
                <th>VAT (5%)</th>
                <th>Total Unit Price (Incl. VAT)</th>
            </tr>
            <tr>
                <td>Destinator (PR)</td>
                <td>95,900.00 AED</td>
                <td>4,795.00 AED</td>
                <td>100,695.00 AED</td>
            </tr>
        </table>

        <div class="highlight-box">
            <p><strong>TOTAL VEHICLE VALUE (INCL. ADDONS):</strong> 118,128.45 AED</p>
            <p><strong>GROSS DOWN PAYMENT REQ.:</strong> 23,625.69 AED</p>
            <p><strong>VEHICLE FINANCE AMOUNT:</strong> 94,502.76 AED</p>
        </div>

        <h2>2. Loan Installment Breakdowns</h2>
        <p style="color: #008000; font-weight: bold; font-size: 13px;">🟢 Primary Asset Vehicle Financing</p>
        <table>
            <tr>
                <th>Asset Term (Years)</th>
                <th>Flat ROI %</th>
                <th>Principal Loan Block</th>
                <th>Total Interest Accrued</th>
                <th>Monthly Vehicle EMI</th>
            </tr>
            <tr><td>1 Years (12 Mos)</td><td>2.5000%</td><td>94,502.76 AED</td><td>2,362.57 AED</td><td>8,072.11 AED</td></tr>
            <tr><td>2 Years (24 Mos)</td><td>2.5000%</td><td>94,502.76 AED</td><td>4,725.14 AED</td><td>4,134.50 AED</td></tr>
            <tr><td>3 Years (36 Mos)</td><td>2.5000%</td><td>94,502.76 AED</td><td>7,087.71 AED</td><td>2,821.96 AED</td></tr>
            <tr><td>4 Years (48 Mos)</td><td>2.5000%</td><td>94,502.76 AED</td><td>9,450.28 AED</td><td>2,165.69 AED</td></tr>
            <tr><td>5 Years (60 Mos)</td><td>2.5000%</td><td>94,502.76 AED</td><td>11,812.85 AED</td><td>1,771.93 AED</td></tr>
        </table>

        <p style="color: #0000ff; font-weight: bold; font-size: 13px;">🔵 Down Payment Loan Financing Options</p>
        <table>
            <tr>
                <th>Term</th>
                <th>Financed Balance</th>
                <th>Total Interest</th>
                <th>Monthly EMI</th>
            </tr>
            <tr><td>3 Months (0.00% ROI)</td><td>22,625.69 AED</td><td>0.00 AED</td><td>7,541.90 AED</td></tr>
            <tr><td>12 Months (5.25% ROI)</td><td>22,625.69 AED</td><td>1,187.85 AED</td><td>1,984.46 AED</td></tr>
            <tr><td>24 Months (6.30% ROI)</td><td>22,625.69 AED</td><td>2,850.84 AED</td><td>1,061.52 AED</td></tr>
        </table>

        <h2>3. Accessories Breakdown</h2>
        <table>
            <tr>
                <th>Selected Accessories / Services</th>
                <th>Individual Price (Base)</th>
                <th>VAT Amount (5%)</th>
                <th>Total Cost (incl. VAT)</th>
            </tr>
            <tr><td>FO Ceramic+ Intr&Extr CeramicGold WdwTnt</td><td>2,700.00 AED</td><td>135.00 AED</td><td>2,835.00 AED</td></tr>
            <tr><td>Routine Maintenance Contract (RMC-10-70)</td><td>6,600.00 AED</td><td>330.00 AED</td><td>6,930.00 AED</td></tr>
            <tr><td>Vehicle Replacement Insurance (VRI)</td><td>3,653.46 AED</td><td>0.00 AED (VAT Pre-incl.)</td><td>3,653.46 AED</td></tr>
            <tr><td>Vehicle Insurance</td><td>4,014.99 AED</td><td>0.00 AED (VAT Pre-incl.)</td><td>4,014.99 AED</td></tr>
        </table>

        <h2>4. Out-of-Pocket Cash Outlay Summary</h2>
        <div class="highlight-box">
            <p><strong>Showroom Reservation Fee:</strong> 1,000.00 AED (Paid Upfront)</p>
            <p><strong>Remaining Down Payment Balance:</strong> 22,625.69 AED (Financed via Loan Plan)</p>
            <p><strong>Registration Documentation Fee:</strong> 600.00 AED</p>
            <p><strong>DP Processing Fee (DP PF):</strong> 315.00 AED</p>
            <p><strong>Bank Processing Fee (Bank PF):</strong> 992.28 AED</p>
            <p style="color: #cc0000; font-size: 15px; margin-top: 8px;"><strong>ACTUAL UPFRONT CASH REQUIRED AT SHOWROOM HANDOVER: 2,907.28 AED</strong></p>
        </div>

        <h2>5. Application Requirements & Disclosures</h2>
        <p><strong>Required Documentation Checklist:</strong></p>
        <ul>
            <li>Passport Copy, Digital Visa & Address Page For Indian Passport, Page #44 For Philippines Passport.</li>
            <li>Emirates ID Card Copy Both Sides.</li>
            <li>Labour Card / Free Zone / Employer ID.</li>
            <li>Copy of the UAE Driver's License Both Sides.</li>
            <li>Current Dated Salary Certificate from The Employer.</li>
            <li>Pay Slips For The Last 3 Months - [If Variance In Salary].</li>
            <li>IBAN.</li>
        </ul>

    </body>
    </html>
    """
    return html_content

# --- Streamlit UI Integration ---
st.title("Mitsubishi Financial Matrix Report Generator")

# Placeholder for vehicle image load (Replace with your actual image variable or path if available)
# Using a blank/dummy fallback or loaded image simulation here:
try:
    # Assuming local file or stream exists, else use a placeholder or handle gracefully
    # For demonstration, we use a sample image handler or string path
    car_image_b64 = get_image_base64("path_to_your_vehicle_image.png") 
except Exception:
    # Fallback blank small transparent png encoded if file missing in demo block
    car_image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

st.markdown("---")
st.subheader("📥 Export Report Options")

# Generate HTML data string
html_data = generate_html_report(car_image_b64)

# Streamlit Download Button for HTML
st.download_button(
    label="Download HTML Report (for PDF/Print)",
    data=html_data,
    file_name="Mitsubishi_Financial_Matrix_Report_Destinator_PR.html",
    mime="text/html",
    help="Click to download the complete report layout as an HTML file. You can open it in any browser and press Ctrl+P / Cmd+P to save as PDF."
)
