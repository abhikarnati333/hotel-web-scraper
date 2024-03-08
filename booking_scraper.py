from playwright.sync_api import sync_playwright
import pandas as pd
import tkinter as tk
from tkinter import ttk

def fetch_input():
    checkin_date = checkin_var.get()
    checkout_date = checkout_var.get()
    location = location_var.get()
    adults = adults_var.get()
    children = children_var.get()
    rooms = rooms_var.get()

    with sync_playwright() as p:
        # Custom Booking.com URL
        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss={location}&ssne={location}&ssne_untouched={location}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults={adults}&no_rooms={rooms}&group_children={children}&sb_travel_purpose=leisure'

        # Launching Browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
                    
        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        # Hotel Info
        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)
        
        # Exporting Hotel Data      
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        
        browser.close()

# Create main window
root = tk.Tk()
root.title("Hotel Booking")

# Create and place labels and entry widgets for input parameters
tk.Label(root, text="Check-in Date:").grid(row=0, column=0, padx=10, pady=5)
checkin_var = tk.StringVar()
checkin_entry = tk.Entry(root, textvariable=checkin_var)
checkin_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Checkout Date:").grid(row=1, column=0, padx=10, pady=5)
checkout_var = tk.StringVar()
checkout_entry = tk.Entry(root, textvariable=checkout_var)
checkout_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Location:").grid(row=2, column=0, padx=10, pady=5)
location_var = tk.StringVar()
location_entry = tk.Entry(root, textvariable=location_var)
location_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Adults:").grid(row=3, column=0, padx=10, pady=5)
adults_var = tk.StringVar()
adults_entry = tk.Entry(root, textvariable=adults_var)
adults_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Children:").grid(row=4, column=0, padx=10, pady=5)
children_var = tk.StringVar()
children_entry = tk.Entry(root, textvariable=children_var)
children_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Rooms:").grid(row=5, column=0, padx=10, pady=5)
rooms_var = tk.StringVar()
rooms_entry = tk.Entry(root, textvariable=rooms_var)
rooms_entry.grid(row=5, column=1, padx=10, pady=5)

# Create and place a button to trigger the script with user input
fetch_button = ttk.Button(root, text="Fetch Data", command=fetch_input)
fetch_button.grid(row=6, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
