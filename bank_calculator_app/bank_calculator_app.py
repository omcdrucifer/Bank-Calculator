import customtkinter as ctk
import sys
import json
from collections import namedtuple

import customtkinter as ctk
import json
from collections import namedtuple

class BankProductGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Save and Loan Calculator")
        self.root.geometry("800x600")

        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        self.product_type_var = ctk.StringVar(value="money_market")
        ctk.CTkLabel(input_frame, text="Select Product Type:").pack(pady=5)
        for product in ["Money Market", "Certificate of Deposit", "Loan"]:
            value = product.lower().replace(" ", "_")
            if product == "Certificate of Deposit":
                value = "certificate"  # Adjust to match the method check

            ctk.CTkRadioButton(input_frame, text=product, variable=self.product_type_var, value=value).pack(pady=5)

        self.balance_entry = self.create_entry(input_frame, "Deposit/Principal Balance:")
        self.term_entry = self.create_entry(input_frame, "Term (months/years):")
        self.rate_entry = self.create_entry(input_frame, "Annual Interest/Dividend Rate (%):")

        ctk.CTkButton(input_frame, text="Submit", command=self.create_product).pack(pady=10)

        results_frame = ctk.CTkFrame(self.root)
        results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.result_text = ctk.CTkTextbox(results_frame, height=20, width=70)
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

    def validate_inputs(self):
        try:
            balance = float(self.balance_entry.get())
            term = int(self.term_entry.get())
            rate = float(self.rate_entry.get())
            return balance, term, rate
        except ValueError:
            self.result_text.insert(ctk.END, "Please enter valid numbers for balance, term, and rate.\n")
            return None

    def create_entry(self, frame, label_text):
        ctk.CTkLabel(frame, text=label_text).pack(pady=5)
        entry = ctk.CTkEntry(frame)
        entry.pack(pady=5)
        return entry

    def create_product(self):
        product_type = self.product_type_var.get()
        if product_type == "money_market":
            self.create_money_market_product()
        elif product_type == "certificate":
            self.create_certificate_product()
        elif product_type == "loan":
            self.create_loan_product()
        else:
            self.result_text.insert(ctk.END, "Invalid product type selected.\n")

        def validate_inputs(self):
            try:
                balance = float(self.balance_entry.get())
                term = int(self.term_entry.get())
                rate = float(self.rate_entry.get())
                return balance, term, rate
            except ValueError:
                self.result_text.insert(ctk.END, "Please enter valid numbers for balance, term, and rate.\n")
                return None

    def calculate_compound_interest(self, balance, rate, term_months):
        n = 12  # Monthly compounding
        r = rate / 100
        t = term_months / 12
        A = balance * (1 + r / n) ** (n * t)
        return A - balance, A

    def create_money_market_product(self):
        self.result_text.delete(1.0, ctk.END)
        inputs = self.validate_inputs()
        if not inputs:
            return
        balance, deposit_term_months, _ = inputs

        try:
            with open('dividend_rates.json') as json_file:
                data = json.load(json_file)
                Tier = namedtuple("Tier", ["balance_range", "rate"])
                tiers = [Tier(x["balance_range"], x["rate"]) for x in data["tiers"]]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.result_text.insert(ctk.END, f"Error reading dividend rates: {e}\n")
            return

        applicable_rate = 0
        for tier in tiers:
            balance_range = tier.balance_range.split('-')
            if len(balance_range) == 2:
                lower_bound, upper_bound = map(int, balance_range)
                if lower_bound <= balance <= upper_bound:
                    applicable_rate = tier.rate
                    break
            else:
                if balance >= int(balance_range[0].replace('+', '')):
                    applicable_rate = tier.rate
                    break

        dividends_earned, new_balance = self.calculate_compound_interest(balance, applicable_rate, deposit_term_months)
        self.result_text.insert(ctk.END, f"\nMoney Market Account:\n")
        self.result_text.insert(ctk.END, f"Initial Balance: ${balance}\n")
        self.result_text.insert(ctk.END, f"Dividends Earned: ${round(dividends_earned, 2)}\n")
        self.result_text.insert(ctk.END, f"New Balance: ${round(new_balance, 2)}\n")    

    def create_certificate_product(self):
        self.result_text.delete(1.0, ctk.END)
        inputs = self.validate_inputs()
        if not inputs:
            return
        balance, deposit_term_months, apr = inputs

        dividends_earned, new_balance = self.calculate_compound_interest(balance, apr, deposit_term_months)
        self.result_text.insert(ctk.END, f"\nCertificate of Deposit:\n")
        self.result_text.insert(ctk.END, f"Initial Balance: ${balance}\n")
        self.result_text.insert(ctk.END, f"Dividends Earned: ${round(dividends_earned, 2)}\n")
        self.result_text.insert(ctk.END, f"New Balance: ${round(new_balance, 2)}\n")

    def create_loan_product(self):
        self.result_text.delete(1.0, ctk.END)
        inputs = self.validate_inputs()
        if not inputs:
            return
        principal, loan_term_years, annual_interest_rate = inputs

        monthly_interest_rate = annual_interest_rate / 12 / 100
        total_payments = loan_term_years * 12
        monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)

        total_amount_paid = monthly_payment * total_payments
        total_interest_paid = total_amount_paid - principal

        self.result_text.insert(ctk.END, f"\nLoan Product:\n")
        self.result_text.insert(ctk.END, f"Principal: ${principal}\n")
        self.result_text.insert(ctk.END, f"Monthly Payment: ${round(monthly_payment, 2)}\n")
        self.result_text.insert(ctk.END, f"Total Interest Paid: ${round(total_interest_paid, 2)}\n")
        self.result_text.insert(ctk.END, f"Total Amount Paid: ${round(total_amount_paid, 2)}\n")
    
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("800x600")

    app = BankProductGUI(root)

    root.mainloop()
