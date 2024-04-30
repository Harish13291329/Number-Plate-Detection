import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

class NumberPlateDetectorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Plate Detection")
        self.master.geometry("600x400")  # Set window size

        # Set background color
        self.background_color = self.random_color()
        self.master.config(bg=self.background_color)

        # Car owner names and car names
        self.car_owners = ["John Doe", "Jane Smith", "David Johnson", "Emily Brown", "Michael Wilson"]
        self.car_names = ["Benz", "Skoda", "Toyota", "Suzuki", "Audi"]

        self.create_widgets()

    def create_widgets(self):
        # Center the window
        self.master.eval('tk::PlaceWindow . center')

        # Button to open file dialog
        self.open_button = tk.Button(self.master, text="Select Image", command=self.process_image)
        self.open_button.config(font=("Arial", 14))
        self.open_button.pack(pady=20)

        # Button to display car owner's name and car name
        self.info_button = tk.Button(self.master, text="Show Car Info", command=self.display_car_info, state="disabled")
        self.info_button.config(font=("Arial", 14))
        self.info_button.pack(pady=20)

        # Result label
        self.result_label = tk.Label(self.master, text="")
        self.result_label.config(font=("Arial", 14))
        self.result_label.pack()

        # Image display label
        self.image_label = tk.Label(self.master)
        self.image_label.pack()

    def process_image(self):
        self.open_button.config(bg="blue")  # Flash the button color
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.detect_number_plate(file_path)
            except Exception as e:
                print("Error:", e)
                self.display_error_image()

    def detect_number_plate(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the pre-trained Haar cascade classifier for license plate detection
        plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

        # Detect license plates in the image
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))

        # If no plates detected, display the original image
        if len(plates) == 0:
            self.result_label.config(text="No number plate")
            self.display_original_image(image_path)
            self.info_button.config(state="disabled")  # Disable the "Show Car Info" button
        else:
            self.result_label.config(text="Number plate detected")
            # Draw rectangles around the detected plates
            for (x, y, w, h) in plates:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Convert image from OpenCV format to PIL format for displaying in Tkinter
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # Display the image with detected plates
            self.image_label.config(image=image)
            self.image_label.image = image
            self.info_button.config(state="normal")  # Enable the "Show Car Info" button

    def display_original_image(self, image_path):
        # Open the image using PIL
        original_image = Image.open(image_path)
        original_image.thumbnail((400, 400))  # Resize the image to fit in the window
        original_image = ImageTk.PhotoImage(original_image)

        # Display the original image
        self.image_label.config(image=original_image)
        self.image_label.image = original_image
        self.result_label.config(text="No number plate")

    def random_color(self):
        colors = ["#FF5733", "#33FF7F", "#3384FF", "#FF33FF", "#FFFF33"]
        return random.choice(colors)

    def display_car_info(self):
        self.info_button.config(bg="blue")  # Flash the button color
        # Randomly select car owner name and car name
        car_owner_name = random.choice(self.car_owners)
        car_name = random.choice(self.car_names)
        messagebox.showinfo("Car Information", f"Car Owner: {car_owner_name}\nCar Name: {car_name}")

    def display_error_image(self):
        error_image_path = "C:/Users/Harish/Downloads/3674270-200.png"
        error_image = Image.open(error_image_path)
        error_image.thumbnail((400, 400))
        error_image = ImageTk.PhotoImage(error_image)

        # Display the error image
        self.image_label.config(image=error_image)
        self.image_label.image = error_image
        self.result_label.config(text="Error processing image")

def main():
    root = tk.Tk()
    app = NumberPlateDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
