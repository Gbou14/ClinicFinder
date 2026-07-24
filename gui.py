"""Desktop interface for ClinicFinder.

Run with: python gui.py
"""

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from main import run_discovery
from src.api.usage import build_usage_report
from src.config.settings import (
    GOOGLE_MONTH_TO_DATE_GEOCODING,
    GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH,
)


class ClinicFinderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ClinicFinder")
        self.resizable(False, False)
        self.export_path = None
        self.cost_report = []

        container = ttk.Frame(self, padding=20)
        container.grid()

        ttk.Label(container, text="ClinicFinder", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(container, text="Find qualifying clinics within a 30-mile radius.").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        ttk.Label(container, text="ZIP code").grid(row=2, column=0, sticky="w")
        self.zip_code = tk.StringVar()
        ttk.Entry(container, textvariable=self.zip_code, width=18).grid(
            row=2, column=1, sticky="ew", padx=(12, 0)
        )

        ttk.Label(container, text="Clinics to export").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.target_count = tk.IntVar(value=20)
        ttk.Spinbox(container, from_=10, to=50, textvariable=self.target_count, width=16).grid(
            row=3, column=1, sticky="ew", padx=(12, 0), pady=(10, 0)
        )

        self.enrich_emails = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            container,
            text="Find and validate emails (slower)",
            variable=self.enrich_emails,
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))

        self.run_button = ttk.Button(container, text="Find Clinics", command=self.start_run)
        self.run_button.grid(row=5, column=0, sticky="w", pady=(18, 0))
        self.open_button = ttk.Button(
            container, text="Open Export Folder", command=self.open_export_folder, state="disabled"
        )
        self.open_button.grid(row=5, column=1, sticky="e", pady=(18, 0))
        self.cost_button = ttk.Button(
            container, text="View API Cost Report", command=self.show_cost_report, state="disabled"
        )
        self.cost_button.grid(row=6, column=0, sticky="w", pady=(8, 0))

        self.status = tk.StringVar(value="Ready")
        ttk.Label(container, textvariable=self.status, wraplength=390).grid(
            row=7, column=0, columnspan=2, sticky="w", pady=(14, 0)
        )

    def start_run(self):
        zip_code = self.zip_code.get().strip()
        if not (zip_code.isdigit() and len(zip_code) == 5):
            messagebox.showerror("Invalid ZIP code", "Enter a five-digit US ZIP code.")
            return
        target_count = self.target_count.get()
        if not 10 <= target_count <= 50:
            messagebox.showerror("Invalid clinic count", "Choose a number from 10 to 50.")
            return

        self.run_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.cost_button.configure(state="disabled")
        self.status.set("Searching Google Places…")
        worker = threading.Thread(
            target=self.run_worker,
            args=(zip_code, target_count, self.enrich_emails.get()),
            daemon=True,
        )
        worker.start()

    def run_worker(self, zip_code, target_count, enrich_emails):
        try:
            clinics, export_path = run_discovery(zip_code, target_count, enrich_emails)
        except Exception as error:
            self.after(0, self.run_failed, str(error))
            return
        self.after(0, self.run_complete, len(clinics), export_path)

    def run_complete(self, count, export_path):
        self.export_path = Path(export_path).resolve()
        self.cost_report = build_usage_report({
            "Geocoding": GOOGLE_MONTH_TO_DATE_GEOCODING,
            "Places Nearby Search Pro": GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH,
        })
        self.status.set(f"Done: {count} clinics exported to {self.export_path.name}")
        self.run_button.configure(state="normal")
        self.open_button.configure(state="normal")
        self.cost_button.configure(state="normal")

    def run_failed(self, error):
        self.status.set("Run failed")
        self.run_button.configure(state="normal")
        messagebox.showerror("ClinicFinder error", error)

    def open_export_folder(self):
        if self.export_path:
            os.startfile(self.export_path.parent)

    def show_cost_report(self):
        window = tk.Toplevel(self)
        window.title("API Cost Report")
        window.resizable(False, False)
        frame = ttk.Frame(window, padding=16)
        frame.grid()
        ttk.Label(frame, text="API Cost Report", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        for index, report in enumerate(self.cost_report, start=1):
            ttk.Label(frame, text=report["Google Maps SKU"], font=("Segoe UI", 10, "bold")).grid(
                row=index * 2 - 1, column=0, columnspan=2, sticky="w", pady=(12, 2)
            )
            details = (
                f"Calls this run: {report['Calls this run']}\n"
                f"Free calls remaining: {report['Free calls remaining']:,}\n"
                f"Estimated cost after free cap: ${report['Estimated cost after free cap (USD)']:.2f}"
            )
            ttk.Label(frame, text=details, justify="left").grid(
                row=index * 2, column=0, columnspan=2, sticky="w"
            )

        ttk.Label(
            frame,
            text="This is an estimate. The Google Cloud Billing report is authoritative.",
            foreground="#666666",
        ).grid(row=len(self.cost_report) * 2 + 1, column=0, columnspan=2, sticky="w", pady=(14, 0))


if __name__ == "__main__":
    ClinicFinderApp().mainloop()
