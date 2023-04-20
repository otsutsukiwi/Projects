from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageEnhance
import random, sys, os
from time import sleep

def typePrint(text, time=0.3): # TYPE PRINTER EFFECT
    for char in text:
        sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()
    sleep(time)

def openFile(choice): # Displays a tkinter window that opens a file dialog screen to select an image
    root = Tk()
    root.geometry("1x1+250+100")
    if choice==1:
        filepath = filedialog.askopenfilename(initialdir="ImagePIL\Images")
        root.destroy()
    elif choice==2:
        filepath = filedialog.askdirectory(initialdir="ImagePIL\Images")
        root.destroy()
    return filepath

def main(): # The main function
    os.system('cls')
    typePrint("Welcome to Image Manipulation Tool!")
    while True:
        typePrint("\nDo you want to select an image from a list or select your own image?\n[1.SELECT] [2.LIST] [3.EXIT]")
        choice = input().lower()
        if choice=="1": # If user chooses 1 it goes to the openFile function 
            while True:
                try: # If they do not select an image it repeats the loop
                    file_path = openFile(1) 
                    selection(file_path)
                    edits(file_path)
                    quit()
                except:
                    typePrint("Invalid input!")
        elif choice=="2": # If user choose 2 it prints out a list of all imgaes in the Images folder
            print()
            img_folder_dir = "Images\\" # CHANGE THE DIRECTORY IF IT DOESNT WORK!!!!
            images = {}
            count = 0
            for x, y, files in os.walk(img_folder_dir):
                for file in files:
                    images[str(count + 1)] = img_folder_dir + file # Places image paths/names in a dictionary from 1 - len(imagelist)
                    count += 1
                    bob = str(count) + ". " + file
                    typePrint(bob, 0.001)
            while True:
                typePrint("Which image do you want to select?\nType 'bob' to randomize")
                image_select = input()
                if image_select=="bob": # if user enters bob it selects a random image
                    rand = random.randint(1,len(images))
                    file_path = images[str(rand)]
                    selection(file_path)
                    edits(file_path)
                    quit()
                else:
                    try: # if user doens't enter a correct number or a valid memeber of list of images it repeats loop
                        index = int(image_select)
                        file_path = images[str(index)]
                        selection(file_path)
                        edits(file_path)
                        quit()
                    except (ValueError, KeyError):
                        typePrint("Invalid input!")
        elif choice=="3": # If user chooses 3 it quits the program
            os.system('cls')
            typePrint("Exiting program...")
            quit()
        else:
            typePrint("Invalid input!")

def selection(path): # Displays the image
    image = Image.open(path)
    image.show()

def edits(path): # The edit function
    os.system('cls')
    image = Image.open(path)
    while True:
        typePrint("What effect would you like to add to this image?\n[1.Blur]\n[2.Resize]\n[3.Rotate]\n[4.Black and White]\n[5.Image Enhance]")
        edit_choice = input()
        if edit_choice=="1": 
            while True:
                # Ask user for blur level
                typePrint("How blurry would you like your image to be?")
                blur_unit = input()
                try:
                    # Convert blur level to int and apply blur effect
                    blur_unit = int(blur_unit)
                    blur_img = image.filter(ImageFilter.BLUR).filter(ImageFilter.GaussianBlur(radius=blur_unit))
                    
                    # Create a folder to save the edited image if it doesn't exist
                    folder_path = "ImagePIL\Images\Blur"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    # Ask user to input a name for the edited image
                    typePrint("Please enter a name for your newly edited file")
                    file_name = input()

                    # Save the edited image and show it to the user
                    new_file_path = folder_path + "\\" + file_name + "_blur.png"
                    blur_img.save(new_file_path)
                    blur_img.show()

                    while True:
                        # Ask user if they want to keep editing the image or not
                        typePrint("Would you like to keep editing this image?\n(Y) or (N)")
                        edit_choice = input().lower()
                        
                        if edit_choice=="y":
                            # If the user wants to keep editing, call the edits function recursively with the new file path
                            edits(new_file_path)
                        elif edit_choice=="n":
                            while True:
                                # Ask user if they want to edit a new image or quit the program
                                typePrint("Would you like to edit a new image or quit?\n(Y) or (Q)")
                                new_choice = input().lower()

                                if new_choice=="y":
                                    # If the user wants to edit a new image, call the main function to start again
                                    main()
                                elif new_choice=="q":
                                    # If the user wants to quit the program, clear the console screen and exit
                                    os.system('cls')
                                    typePrint("GOODBYE!")
                                    quit()
                                else:
                                    typePrint("Invalid input!")
                        else:
                            typePrint("Invalid input!")
                except(ValueError, KeyError):
                    typePrint("Invalid input!")

        elif edit_choice=="2": # RESIZE EFFECT
            while True:
                typePrint("X unit : ")
                x_size_unit = input()
                typePrint("Y unit : ")
                y_size_unit = input()
                try:
                    x_size_unit = int(x_size_unit)
                    y_size_unit = int(y_size_unit)
                    resized_img = image.resize((x_size_unit, y_size_unit))
                    folder_path = "ImagePIL\Images\Size"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    typePrint("Please enter a name for your newly edited file")
                    file_name = input()
                    new_file_path = folder_path + "\\" + file_name + "_size.png"
                    resized_img.save(new_file_path)
                    resized_img.show()
                    while True:
                        typePrint("Would you like to keep editing this image?\n(Y) or (N)")
                        edit_choice = input().lower()
                        if edit_choice=="y":
                            edits(new_file_path)
                        elif edit_choice=="n":
                            while True:
                                typePrint("Would you like to edit a new image or quit?\n(Y) or (Q)")
                                new_choice = input().lower()
                                if new_choice=="y":
                                    main()
                                elif new_choice=="q":
                                    os.system('cls')
                                    typePrint("GOODBYE!")
                                    quit()
                                else:
                                    typePrint("Invalid input!")
                        else:
                            typePrint("Invalid input!")
                except(ValueError, KeyError):
                    typePrint("Invalid input!")
        
        elif edit_choice=="3": # ROTATE EFFECT
            while True:
                typePrint("Rotation unit : ")
                r_unit = input()
                try:
                    r_unit = int(r_unit)
                    rotated_img = image.rotate(r_unit)
                    folder_path = "ImagePIL\Images\Rotate"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    typePrint("Please enter a name for your newly edited file")
                    file_name = input()
                    new_file_path = folder_path + "\\" + file_name + "_rotate.png"
                    rotated_img.save(new_file_path)
                    rotated_img.show()
                    while True:
                        typePrint("Would you like to keep editing this image?\n(Y) or (N)")
                        edit_choice = input().lower()
                        if edit_choice=="y":
                            edits(new_file_path)
                        elif edit_choice=="n":
                            while True:
                                typePrint("Would you like to edit a new image or quit?\n(Y) or (Q)")
                                new_choice = input().lower()
                                if new_choice=="y":
                                    main()
                                elif new_choice=="q":
                                    os.system('cls')
                                    typePrint("GOODBYE!")
                                    quit()
                                else:
                                    typePrint("Invalid input!")
                        else:
                            typePrint("Invalid input!")
                except(ValueError, KeyError):
                    typePrint("Invalid input!")
        
        elif edit_choice=="4": # BLACK AND WHITE EFFECT
            while True:
                bw_img = image.convert("L")
                folder_path = "ImagePIL\Images\B&W"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                typePrint("Please enter a name for your newly edited file")
                file_name = input()
                new_file_path = folder_path + "\\" + file_name + "_B&W.png"
                bw_img.save(new_file_path)
                bw_img.show()
                while True:
                    typePrint("Would you like to keep editing this image?\n(Y) or (N)")
                    edit_choice = input().lower()
                    if edit_choice=="y":
                        edits(new_file_path)
                    elif edit_choice=="n":
                        while True:
                            typePrint("Would you like to edit a new image or quit?\n(Y) or (Q)")
                            new_choice = input().lower()
                            if new_choice=="y":
                                main()
                            elif new_choice=="q":
                                os.system('cls')
                                typePrint("GOODBYE!")
                                quit()
                            else:
                                typePrint("Invalid input!")
                    else:
                        typePrint("Invalid input!")
        
        elif edit_choice=="5": # IMAGEENHANCE EFFECT
            while True:
                typePrint("Contrast unit : ")
                contrast = input()
                typePrint("Brightness unit : ")
                brightness = input()
                try:
                    brightness = int(brightness)
                    contrast = int(contrast)
                    brightness_enhancer = ImageEnhance.Brightness(image)
                    bright_img = brightness_enhancer.enhance(brightness)
                    contrast_enhancer = ImageEnhance.Contrast(bright_img)
                    contrast_img = contrast_enhancer.enhance(contrast)
                    folder_path = "ImagePIL\Images\Enhanced"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    typePrint("Please enter a name for your newly edited file")
                    file_name = input()
                    new_file_path = folder_path + "\\" + file_name + "_B&W.png"
                    contrast_img.save(new_file_path)
                    contrast_img.show()
                    while True:
                        typePrint("Would you like to keep editing this image?\n(Y) or (N)")
                        edit_choice = input().lower()
                        if edit_choice=="y":
                            edits(new_file_path)
                        elif edit_choice=="n":
                            while True:
                                typePrint("Would you like to edit a new image or quit?\n(Y) or (Q)")
                                new_choice = input().lower()
                                if new_choice=="y":
                                    main()
                                elif new_choice=="q":
                                    os.system('cls')
                                    typePrint("GOODBYE!")
                                    quit()
                                else:
                                    typePrint("Invalid input!")
                        else:
                            typePrint("Invalid input!")
                except(ValueError, KeyError):
                    typePrint("Invalid input!")

main()

