import tkinter as tk
import tkinter.font as tkfont

butt_id = {}
expression = ""
result = 0
text_id = None

#____Button Function____
def button(icon,value,x1,y1,x2,y2):
    tag = f"btn_{icon}" # add the common tag to both rectangle and text so no two inputs are taken

    # Button background
    butt_name = buttons.create_rectangle(x1, y1, x2, y2, fill="#A9A9A9", outline="", tags=(tag,))
    
    # 3D shape for button
    buttons.create_line(x1, y1, x2, y1, fill="white", width=2, tags=(tag,))
    buttons.create_line(x1, y1, x1, y2, fill="white", width=2, tags=(tag,))
    buttons.create_line(x1, y2, x2, y2, fill="#404040", width=2, tags=(tag,))
    buttons.create_line(x2, y1, x2, y2, fill="#404040", width=2, tags=(tag,))
        
    # text for button
    text = buttons.create_text(((x1+x2)/2),((y1+y2)/2),text=icon,font=("Georgia",25),fill="black",tags=(tag,))
    
    # change button color to darkgray on press
    def on_press(event,val=value):
        buttons.move(tag, 1, 1)
        buttons.itemconfigure(butt_name, fill="#C0C0C0")  # slight color change when pressed
    
    def on_release(event,val=value):
        buttons.move(tag, -1, -1)
        buttons.itemconfigure(butt_name, fill="#A9A9A9")  # slight color change when pressed
        operate(val)
    
    buttons.tag_bind(tag, "<ButtonPress-1>",on_press)
    buttons.tag_bind(tag, "<ButtonRelease-1>",on_release)


#____operation of buttons____
def operate(operation):
    global expression, result, text_id


    if operation == "C":
        if expression:
            expression = expression[:-1]  # remove last character
            if text_id:
                # just update the existing text object
                Screen.itemconfig(text_id, text=expression)
        return

    elif operation == "=":
        try:
            result = eval(expression)
            expression = str(result)

            if text_id:
                Screen.delete(text_id)  # remove old text

            # Create new text starting from left
            Screen.update_idletasks()  # Ensure canvas is drawn
            font = tkfont.Font(family="Georgia",size=25, slant="italic")
            result_width = font.measure(expression)
            Screen_width = Screen.winfo_width()
            text_id = Screen.create_text(0, 50, text=expression, font=("Georgia", 25, "italic"), fill="#2C2C2C", anchor="w")

            def slide():
            # Get current x-position of text while ignoring y
                x, _ = Screen.coords(text_id)
                if x + result_width + 8 < Screen_width :  # keep moving until it reaches right edge
                    Screen.move(text_id, 5, 0)  # move 5 pixels to the right
                    Screen.after(5, slide)    # recall slide() after 20ms

            slide()

        except:
            expression = ""
            if text_id:
                Screen.itemconfig(text_id, text="Error")
            else:
                text_id = Screen.create_text(170, 50, text="Error", font=("Georgia", 25), fill="#2C2C2C")
        return


    # Add typed value to expression
    expression += str(operation)
    
    # Fix position if result was sliding
    if text_id:
        Screen.coords(text_id, 330, 50)  # move text back to right
        Screen.itemconfig(text_id, anchor="e")  # align right

    if text_id:
        # update current text
        Screen.itemconfig(text_id, text=expression)
    else:
        # first time creating the text
        text_id = Screen.create_text(330, 50, text=expression, font=("Georgia", 25,"italic"), fill="#2C2C2C",anchor="e")


#_____To write on screen_____
def write(num):
    Screen.create_text()
#_____ Main Window______

main_window = tk.Tk()
main_window.geometry("350x500")
main_window.configure(bg="#373B50")
main_window.title("SAADO Calculator")
main_window.resizable(False,False)

#____Screen of Calculator with sunken border_____
screen_frame = tk.Frame(main_window, relief="sunken", bd=10, bg="#556055")
screen_frame.pack(fill="x", pady=10)

Screen = tk.Canvas(screen_frame, height=100, bg="#4E654E", highlightthickness=0)
Screen.pack(fill="both", expand=True)

#____Buttons of Calculator_____
buttons = tk.Canvas(main_window, bg="#373B50", highlightthickness=0)
buttons.pack(fill="both", expand="True")

values = {"7":7,"8":8,"9":9,"+":"+","4":4,"5":5,"6":6,"-":"-","1":1,"2":2,"3":3,"*":"*","0":0,"C":"C","=":"=","/":"/",}

x1, y1, x2, y2 = 5, 5, 85, 85
count = 0
for key,value in values.items():
    button(key,value,x1, y1, x2, y2)
    x1 += 85
    x2 += 85
    count += 1
    if count % 4 == 0:
        x1 = 5
        x2 = 85
        y1 += 85
        y2 += 85

main_window.mainloop()