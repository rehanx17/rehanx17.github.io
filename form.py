import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from fpdf import FPDF
from datetime import datetime

class ReceiptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Receipt Generator")
        self.items = []
        
        # Customer Information
        tk.Label(root, text="Customer Name:").grid(row=0, column=0, padx=10, pady=5)
        self.customer_name_entry = tk.Entry(root)
        self.customer_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Product Information
        tk.Label(root, text="Product Name:").grid(row=1, column=0, padx=10, pady=5)
        self.product_name_entry = tk.Entry(root)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Price per Item:").grid(row=3, column=0, padx=10, pady=5)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        add_item_button = tk.Button(root, text="Add Item", command=self.add_item)
        add_item_button.grid(row=4, column=0, padx=10, pady=10)

        generate_receipt_button = tk.Button(root, text="Generate Receipt", command=self.generate_receipt)
        generate_receipt_button.grid(row=4, column=1, padx=10, pady=10)

        # Receipt Display
        self.receipt_text = tk.Text(root, width=50, height=15)
        self.receipt_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_item(self):
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not product_name or not quantity or not price:
            messagebox.showerror("Input Error", "Please fill all fields")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid quantity or price")
            return

        # Add item to the list and clear entry fields
        self.items.append((product_name, quantity, price))
        self.product_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        self.update_receipt()

    def update_receipt(self):
        self.receipt_text.delete(1.0, tk.END)
        receipt_content = "Receipt:\n"
        receipt_content += f"{'Item':20}{'Qty':5}{'Price':10}{'Total':10}\n"
        receipt_content += "-" * 50 + "\n"
        subtotal = 0

        for item, qty, price in self.items:
            total_price = qty * price
            subtotal += total_price
            receipt_content += f"{item:20}{qty:<5}{price:<10.2f}{total_price:<10.2f}\n"

        tax = subtotal * 0.05
        total = subtotal + tax

        receipt_content += "-" * 50 + "\n"
        receipt_content += f"Subtotal: {subtotal:.2f}\n"
        receipt_content += f"Tax (5%): {tax:.2f}\n"
        receipt_content += f"Total: {total:.2f}\n"

        self.receipt_text.insert(tk.END, receipt_content)

    def generate_receipt(self):
        customer_name = self.customer_name_entry.get()

        if not customer_name or not self.items:
            messagebox.showerror("Input Error", "Please enter customer details and add at least one item.")
            return

        # Choose location to save receipt
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return
        
        # Generate the PDF receipt
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, f'Receipt for {customer_name}', ln=True, align='C')
        pdf.ln(10)

        pdf.set_font('Arial', '', 10)
        pdf.cell(200, 10, f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 10, 'Item', 1)
        pdf.cell(20, 10, 'Qty', 1)
        pdf.cell(40, 10, 'Price', 1)
        pdf.cell(40, 10, 'Total', 1)
        pdf.ln(10)

        subtotal = 0
        pdf.set_font('Arial', '', 10)
        for item, qty, price in self.items:
            total_price = qty * price
            subtotal += total_price
            pdf.cell(60, 10, item, 1)
            pdf.cell(20, 10, str(qty), 1)
            pdf.cell(40, 10, f'{price:.2f}', 1)
            pdf.cell(40, 10, f'{total_price:.2f}', 1)
            pdf.ln(10)

        tax = subtotal * 0.05
        total = subtotal + tax
        pdf.ln(5)
        pdf.cell(60, 10, f'Subtotal: {subtotal:.2f}', ln=True)
        pdf.cell(60, 10, f'Tax (5%): {tax:.2f}', ln=True)
        pdf.cell(60, 10, f'Total: {total:.2f}', ln=True)

        # Save the PDF
        pdf.output(save_path)
        messagebox.showinfo("Success", f"Receipt saved as {save_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiptApp(root)
    root.mainloop()
