import time
from tkinter import filedialog, font, messagebox

import numpy as np
import pandas as pd
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def open_file():
    file = filedialog.askopenfile(mode='rb', filetypes=[('text files', '*.txt')], parent=root)
    if file:
        contents = file.readlines()
        contents = [i.strip() for i in contents]
        contents = [x.decode('utf-8') for x in contents]
        ans = messagebox.askquestion("Question", str(file.name) + " Uploaded.\nDo you want to proceed?", parent=root)
        if ans == "yes":
            run(contents)

# options = Options()
# options.headless = True
def run(contents):
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 120)
    messagebox.showinfo("Info", "Scrapping Started", parent=root)
    print("-----------------------------Scrapping Started---------------------------------")
    driver.get("https://www.amazon.in/")

    for j in contents:
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))).send_keys(str(j))
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='nav-search-submit-button']"))).click()
        tot_pgs = int(wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='s-pagination-item s-pagination-disabled']"))).text)

        name = []
        rating = []
        no_of_reviews = []
        price = []
        for i in range(0, tot_pgs-1):
            time.sleep(5)
            x1 = [el.text for el in (driver.find_elements(By.XPATH, "//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']/a/span"))]
            name.extend(x1)
            x2 = [el.text for el in (wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-base']"))))]
            rating.extend(x2)
            x3 = [el.text for el in (wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-base s-underline-text']"))))]
            no_of_reviews.extend(x3)
            x4 = [el.text for el in (wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@data-a-size='xl']/span/span[@class='a-price-whole']"))))]
            price.extend(x4)
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Next']"))).click()

        df = pd.DataFrame(list(zip(name, rating, no_of_reviews, price)), columns=['Name', 'Rating', 'No_of_reviews', 'Price'])

        output_file = str(j)+".xlsx"
        df.to_excel(output_file, index=False)

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))).clear()

    driver.close()
    messagebox.showinfo("Info", "Scrapping Completed", parent=root)
    print("-----------------------------Scrapping Completed-------------------------------")

root = Tk()
root.configure(bg='white', highlightbackground='black', highlightthickness=1)
root.title("Web Scrapping from Amazon")
root.resizable(False, False)
w = 700
h = 500
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

font1 = font.Font(root, family='Segoe UI', weight="bold", size=35)
font2 = font.Font(root, family='Segoe UI', weight="bold", size=16)

Label(root, text="Web Scrapping from Amazon", bg="#FFFFFF", pady=25, font=font1).place(relx=0.5, rely=0.15, anchor=CENTER)
Label(root, text="Choose Input file location: ", bg="#FFFFFF", font=font2).place(relx=0.4, rely=0.4, anchor=CENTER)
Button(root, text="Browse", height=2, width=15, command=open_file).place(relx=0.7, rely=0.4, anchor=CENTER)
# Button(root, text="Scrap", height=2, width=15, command=run).place(relx=0.5, rely=0.54, anchor=CENTER)

root.mainloop()