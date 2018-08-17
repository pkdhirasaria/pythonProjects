from tkinter import *
import requests
import re

def retrive_value():

    urls = textBox.get("1.0", "end-1c")
    textBox.delete("1.0", END)
    urlValidator(urls)


def urlValidator(urls):

    #tag red for not working greeen means working
    textBox.tag_configure("green",  foreground='green')
    textBox.tag_configure("red", foreground='red')

    for key in urls.split("\n"):
        if any(re.findall(r'https|http|www', key)):
            flag = 1
            print(key)
            try:
                r = requests.get(key)
                if "Application Unavailable" in r.text:
                    tag = "red"
                    key += " -- NOT WORKING\n"
                    flag = 0
                if flag == 1:
                    key += " -- WORKING\n"
                    tag = "green"
            except Exception as e:
                tag = "red"
                key += " -- NOT WORKING\n"
            textBox.insert("end", key, tag)
        else:
            print(key)
            textBox.insert("end", key+"\n")


if __name__ == "__main__":
    root = Tk()
    root.title("URL VALIDATOR")
    textBox = Text(root, width=100, height=20, bg="white", fg="black", cursor="xterm")
    textBox.pack()
    button = Button(root, text="Check", command=retrive_value)
    button.pack()
    root.mainloop()
