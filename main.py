import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

class ImageColorSpaceConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Color Space Converter")
        self.root.geometry("1200x800")
        self.root.minsize(1200, 800)  # Set minimum window size
        
        # Set application icon
        self.set_application_icon()
        
        # Load custom fonts
        try:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
            self.regular_font = ("fccTYPO-Regular", 11)
            self.bold_font = ("fccTYPO-Bold", 11)
        except Exception as e:
            print(f"Warning: Could not load custom fonts: {e}")
            self.regular_font = ("Arial", 11)
            self.bold_font = ("Arial", 11)
        
        # Variables
        self.original_image = None
        self.current_image = None
        self.image_path = None
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_rgb_tab()
        self.create_cielab_tab()
        self.create_hsv_tab()
        
        # Apply styling
        self.apply_styling()
        
    def set_application_icon(self):
        """Set the application icon based on platform"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "assets", "icons")
            if sys.platform == "darwin":
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
            elif sys.platform == "win32":
                icon_file = os.path.join(icon_path, "icon.ico")
                if os.path.exists(icon_file):
                    self.root.iconbitmap(icon_file)
            else:
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading application icon: {str(e)}")
        
    def create_rgb_tab(self):
        rgb_frame = ttk.Frame(self.notebook)
        self.notebook.add(rgb_frame, text="RGB Preview")
        
        # Control panel
        control_frame = ttk.Frame(rgb_frame)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(control_frame, text="📁 Load Image", command=self.load_image, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="💾 Save Image", command=self.save_image, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        # Channel selection
        channel_frame = ttk.LabelFrame(control_frame, text="Display Channel", style='Custom.TLabelframe')
        channel_frame.pack(side=tk.LEFT, padx=20)
        
        self.rgb_channel_var = tk.StringVar(value="all")
        ttk.Radiobutton(channel_frame, text="All", variable=self.rgb_channel_var, 
                       value="all", command=self.update_rgb_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="R", variable=self.rgb_channel_var, 
                       value="R", command=self.update_rgb_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="G", variable=self.rgb_channel_var, 
                       value="G", command=self.update_rgb_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="B", variable=self.rgb_channel_var, 
                       value="B", command=self.update_rgb_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # Color information display
        color_frame = ttk.LabelFrame(control_frame, text="Color Information", style='Custom.TLabelframe')
        color_frame.pack(side=tk.LEFT, padx=20)
        
        self.color_label = ttk.Label(color_frame, text="Hover over image to see RGB values", 
                                   font=self.regular_font, foreground='blue')
        self.color_label.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready to load image", font=self.bold_font)
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # Image display area
        self.canvas_frame = ttk.Frame(rgb_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events for color information
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        
    def create_cielab_tab(self):
        cielab_frame = ttk.Frame(self.notebook)
        self.notebook.add(cielab_frame, text="CIELab Conversion")
        
        # Control panel
        control_frame = ttk.Frame(cielab_frame)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(control_frame, text="🔄 Convert to CIELab", command=self.convert_to_cielab, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="💾 Save CIELab", command=self.save_cielab, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        # Channel selection
        channel_frame = ttk.LabelFrame(control_frame, text="Display Channel", style='Custom.TLabelframe')
        channel_frame.pack(side=tk.LEFT, padx=20)
        
        self.cielab_channel_var = tk.StringVar(value="all")
        ttk.Radiobutton(channel_frame, text="All", variable=self.cielab_channel_var, 
                       value="all", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="L", variable=self.cielab_channel_var, 
                       value="L", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="a", variable=self.cielab_channel_var, 
                       value="a", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="b", variable=self.cielab_channel_var, 
                       value="b", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # Display mode toggle
        display_frame = ttk.LabelFrame(control_frame, text="Display Mode", style='Custom.TLabelframe')
        display_frame.pack(side=tk.LEFT, padx=20)
        
        self.cielab_display_mode = tk.StringVar(value="rgb")
        ttk.Radiobutton(display_frame, text="RGB View", variable=self.cielab_display_mode, 
                       value="rgb", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(display_frame, text="Raw Data", variable=self.cielab_display_mode, 
                       value="raw", command=self.update_cielab_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # CIELab image display
        self.cielab_canvas = tk.Canvas(cielab_frame, bg="white")
        self.cielab_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # CIELab data
        self.cielab_image = None
        
    def create_hsv_tab(self):
        hsv_frame = ttk.Frame(self.notebook)
        self.notebook.add(hsv_frame, text="HSV Conversion")
        
        # Control panel
        control_frame = ttk.Frame(hsv_frame)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(control_frame, text="🔄 Convert to HSV", command=self.convert_to_hsv, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="💾 Save HSV", command=self.save_hsv, 
                  style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        # Channel selection
        channel_frame = ttk.LabelFrame(control_frame, text="Display Channel", style='Custom.TLabelframe')
        channel_frame.pack(side=tk.LEFT, padx=20)
        
        self.hsv_channel_var = tk.StringVar(value="all")
        ttk.Radiobutton(channel_frame, text="All", variable=self.hsv_channel_var, 
                       value="all", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="H", variable=self.hsv_channel_var, 
                       value="H", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="S", variable=self.hsv_channel_var, 
                       value="S", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(channel_frame, text="V", variable=self.hsv_channel_var, 
                       value="V", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # Display mode toggle
        display_frame = ttk.LabelFrame(control_frame, text="Display Mode", style='Custom.TLabelframe')
        display_frame.pack(side=tk.LEFT, padx=20)
        
        self.hsv_display_mode = tk.StringVar(value="rgb")
        ttk.Radiobutton(display_frame, text="RGB View", variable=self.hsv_display_mode, 
                       value="rgb", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(display_frame, text="Raw Data", variable=self.hsv_display_mode, 
                       value="raw", command=self.update_hsv_display, style='Custom.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # HSV image display
        self.hsv_canvas = tk.Canvas(hsv_frame, bg="white")
        self.hsv_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # HSV data
        self.hsv_image = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    messagebox.showerror("Error", "Failed to load image")
                    return
                    
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                self.current_image = self.original_image.copy()
                self.display_image()
                self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                
                # Clear converted images
                self.cielab_image = None
                self.hsv_image = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                
    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Convert back to BGR for OpenCV
                save_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, save_image)
                messagebox.showinfo("Success", "Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                
    def on_mouse_move(self, event):
        if self.current_image is None:
            return
            
        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 600
            
        img_height, img_width = self.current_image.shape[:2]
        
        # Calculate scaling
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y)
        
        # Calculate image coordinates (accounting for centering)
        x_offset = (canvas_width - int(img_width * scale)) // 2
        y_offset = (canvas_height - int(img_height * scale)) // 2
        
        img_x = int((canvas_x - x_offset) / scale)
        img_y = int((canvas_y - y_offset) / scale)
        
        # Check if coordinates are within image bounds
        if 0 <= img_x < img_width and 0 <= img_y < img_height:
            # Get RGB values from original image
            rgb_values = self.current_image[img_y, img_x]
            r, g, b = rgb_values
            
            # Convert to hex color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Get current channel selection
            channel = self.rgb_channel_var.get()
            
            # Update color label based on channel
            if channel == "R":
                color_text = f"Red Channel: {r} | Position({img_x}, {img_y})"
            elif channel == "G":
                color_text = f"Green Channel: {g} | Position({img_x}, {img_y})"
            elif channel == "B":
                color_text = f"Blue Channel: {b} | Position({img_x}, {img_y})"
            else:  # "all"
                color_text = f"RGB({r}, {g}, {b}) | Hex: {hex_color} | Position({img_x}, {img_y})"
            
            self.color_label.config(text=color_text)
        else:
            self.color_label.config(text="Hover over image to see RGB values")
            
    def on_mouse_leave(self, event):
        self.color_label.config(text="Hover over image to see RGB values")
        
    def display_image(self):
        if self.current_image is None:
            return
            
        self.update_rgb_display()
        
    def update_rgb_display(self):
        if self.current_image is None:
            return
            
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 600
            
        img_height, img_width = self.current_image.shape[:2]
        
        # Calculate scaling to fit canvas
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Get display image based on channel selection
        display_image = self.current_image.copy()
        channel = self.rgb_channel_var.get()
        
        if channel == "R":
            # Display only red channel
            display_image = display_image[:, :, 0]
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "G":
            # Display only green channel
            display_image = display_image[:, :, 1]
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "B":
            # Display only blue channel
            display_image = display_image[:, :, 2]
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        # else "all" - keep original RGB image
        
        # Resize image
        resized_image = cv2.resize(display_image, (new_width, new_height))
        
        # Convert to PIL Image
        pil_image = Image.fromarray(resized_image)
        self.photo = ImageTk.PhotoImage(pil_image)
        
        # Display on canvas (centered)
        self.canvas.delete("all")
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.photo)
        
    def convert_to_cielab(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
            
        try:
            # Convert RGB to CIELab
            self.cielab_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2LAB)
            self.update_cielab_display()
            messagebox.showinfo("Success", "Image converted to CIELab color space")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to CIELab: {str(e)}")
            
    def update_cielab_display(self):
        if self.cielab_image is None:
            return
            
        display_image = self.cielab_image.copy()
        channel = self.cielab_channel_var.get()
        display_mode = self.cielab_display_mode.get()
        
        if channel == "L":
            # Display L channel (grayscale)
            display_image = display_image[:, :, 0]
            if display_mode == "raw":
                # Show raw L values (0-100 range)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "a":
            # Display a channel (green-red)
            display_image = display_image[:, :, 1]
            if display_mode == "raw":
                # Show raw a values (-128 to 127 range)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # RGB view - normalize for better visualization
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "b":
            # Display b channel (blue-yellow)
            display_image = display_image[:, :, 2]
            if display_mode == "raw":
                # Show raw b values (-128 to 127 range)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # RGB view - normalize for better visualization
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        else:
            # Display all channels
            if display_mode == "raw":
                # Show raw CIELab data (may look unusual)
                # Normalize each channel for display
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # Convert back to RGB for display
                display_image = cv2.cvtColor(display_image, cv2.COLOR_LAB2RGB)
            
        # Resize for display
        canvas_width = self.cielab_canvas.winfo_width()
        canvas_height = self.cielab_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 600
            
        img_height, img_width = display_image.shape[:2]
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized_image = cv2.resize(display_image, (new_width, new_height))
        pil_image = Image.fromarray(resized_image)
        self.cielab_photo = ImageTk.PhotoImage(pil_image)
        
        # Display on canvas (centered)
        self.cielab_canvas.delete("all")
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2
        self.cielab_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.cielab_photo)
        
    def save_cielab(self):
        if self.cielab_image is None:
            messagebox.showwarning("Warning", "No CIELab image to save")
            return
            
        # Ask user which format to save
        choice = messagebox.askyesno("Save Format", 
                                   "Save as raw CIELab data (may not display correctly in other apps)?\n\n"
                                   "Yes = Raw CIELab data\n"
                                   "No = Converted to RGB")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if choice:
                    # Save the actual CIELab data
                    cv2.imwrite(file_path, self.cielab_image)
                    messagebox.showinfo("Success", "CIELab image saved successfully (raw CIELab data)")
                else:
                    # Convert to RGB for saving
                    save_image = cv2.cvtColor(self.cielab_image, cv2.COLOR_LAB2BGR)
                    cv2.imwrite(file_path, save_image)
                    messagebox.showinfo("Success", "CIELab image saved successfully (converted to RGB)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save CIELab image: {str(e)}")
                
    def convert_to_hsv(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
            
        try:
            # Convert RGB to HSV
            self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)
            self.update_hsv_display()
            messagebox.showinfo("Success", "Image converted to HSV color space")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to HSV: {str(e)}")
            
    def update_hsv_display(self):
        if self.hsv_image is None:
            return
            
        display_image = self.hsv_image.copy()
        channel = self.hsv_channel_var.get()
        display_mode = self.hsv_display_mode.get()
        
        if channel == "H":
            # Display H channel (hue)
            display_image = display_image[:, :, 0]
            if display_mode == "raw":
                # Show raw H values (0-179 range in OpenCV)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # RGB view - normalize for better visualization
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "S":
            # Display S channel (saturation)
            display_image = display_image[:, :, 1]
            if display_mode == "raw":
                # Show raw S values (0-255 range)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # RGB view - normalize for better visualization
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        elif channel == "V":
            # Display V channel (value/brightness)
            display_image = display_image[:, :, 2]
            if display_mode == "raw":
                # Show raw V values (0-255 range)
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # RGB view - normalize for better visualization
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2RGB)
        else:
            # Display all channels
            if display_mode == "raw":
                # Show raw HSV data (may look unusual)
                # Normalize each channel for display
                display_image = cv2.normalize(display_image, None, 0, 255, cv2.NORM_MINMAX)
            else:
                # Convert back to RGB for display
                display_image = cv2.cvtColor(display_image, cv2.COLOR_HSV2RGB)
            
        # Resize for display
        canvas_width = self.hsv_canvas.winfo_width()
        canvas_height = self.hsv_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 600
            
        img_height, img_width = display_image.shape[:2]
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized_image = cv2.resize(display_image, (new_width, new_height))
        pil_image = Image.fromarray(resized_image)
        self.hsv_photo = ImageTk.PhotoImage(pil_image)
        
        # Display on canvas (centered)
        self.hsv_canvas.delete("all")
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2
        self.hsv_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.hsv_photo)
        
    def save_hsv(self):
        if self.hsv_image is None:
            messagebox.showwarning("Warning", "No HSV image to save")
            return
            
        # Ask user which format to save
        choice = messagebox.askyesno("Save Format", 
                                   "Save as raw HSV data (may not display correctly in other apps)?\n\n"
                                   "Yes = Raw HSV data\n"
                                   "No = Converted to RGB")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if choice:
                    # Save the actual HSV data
                    cv2.imwrite(file_path, self.hsv_image)
                    messagebox.showinfo("Success", "HSV image saved successfully (raw HSV data)")
                else:
                    # Convert to RGB for saving
                    save_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_HSV2BGR)
                    cv2.imwrite(file_path, save_image)
                    messagebox.showinfo("Success", "HSV image saved successfully (converted to RGB)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save HSV image: {str(e)}")
                
    def apply_styling(self):
        """Apply custom styling to the application"""
        try:
            # Configure styles
            style = ttk.Style()
            
            # Configure button styles
            style.configure('Large.TButton', 
                          font=self.bold_font,
                          padding=(10, 5))
            
            # Configure label styles
            style.configure('Title.TLabel', 
                          font=self.bold_font,
                          foreground='#2c3e50')
            
            # Configure frame styles
            style.configure('Card.TFrame', 
                          relief='raised',
                          borderwidth=1)
            
            # Configure LabelFrame styles
            style.configure('Custom.TLabelframe', 
                          font=self.regular_font)
            style.configure('Custom.TLabelframe.Label', 
                          font=self.regular_font)
            
            # Configure Radiobutton styles
            style.configure('Custom.TRadiobutton', 
                          font=self.regular_font)
            
        except Exception as e:
            print(f"Warning: Could not apply custom styling: {e}")

def main():
    root = tk.Tk()
    
    app = ImageColorSpaceConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 