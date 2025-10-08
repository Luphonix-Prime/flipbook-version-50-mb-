import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import pygame
import os
import fitz
import subprocess
import math

class FlipbookPDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Flipbook Viewer")
        self.root.geometry("1400x800")
        self.root.configure(bg='#8B9DA8')
        
        try:
            pygame.mixer.init()
            self.audio_available = True
        except:
            self.audio_available = False
        
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        self.is_fullscreen = False
        self.page_images = []
        self.thumbnail_images = []
        self.flip_animation_running = False
        
        self.page_turn_sound = None
        self.sound_enabled = True
        
        self.setup_ui()
        if self.audio_available:
            self.load_sounds()
    
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg='#8B9DA8')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        self.sidebar = tk.Frame(main_container, bg='#2C3E50', width=150)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        sidebar_title = tk.Label(
            self.sidebar,
            text="PAGES",
            font=('Arial', 10, 'bold'),
            bg='#2C3E50',
            fg='white',
            pady=10
        )
        sidebar_title.pack()
        
        self.thumbnail_canvas = tk.Canvas(self.sidebar, bg='#2C3E50', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=self.thumbnail_canvas.yview)
        self.thumbnail_frame = tk.Frame(self.thumbnail_canvas, bg='#2C3E50')
        
        self.thumbnail_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.thumbnail_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.thumbnail_canvas.create_window((0, 0), window=self.thumbnail_frame, anchor='nw')
        
        self.thumbnail_frame.bind('<Configure>', lambda e: self.thumbnail_canvas.configure(
            scrollregion=self.thumbnail_canvas.bbox('all')))
        
        content_area = tk.Frame(main_container, bg='#8B9DA8')
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        top_bar = tk.Frame(content_area, bg='#6C7A89', height=50)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        self.title_label = tk.Label(
            top_bar,
            text="Load a PDF to begin",
            font=('Arial', 14, 'bold'),
            bg='#6C7A89',
            fg='white'
        )
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.page_label = tk.Label(
            top_bar,
            text="pages: 0 / 0",
            font=('Arial', 12),
            bg='#6C7A89',
            fg='white'
        )
        self.page_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.canvas_container = tk.Frame(content_area, bg='#8B9DA8')
        self.canvas_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.canvas = tk.Canvas(self.canvas_container, bg='#8B9DA8', highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        control_panel = tk.Frame(content_area, bg='#34495E', height=80)
        control_panel.pack(fill=tk.X)
        control_panel.pack_propagate(False)
        
        btn_container = tk.Frame(control_panel, bg='#34495E')
        btn_container.pack(expand=True)
        
        btn_style = {
            'font': ('Arial', 10, 'bold'),
            'bg': '#3498DB',
            'fg': 'white',
            'activebackground': '#2980B9',
            'relief': tk.FLAT,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2',
            'bd': 0
        }
        
        self.prev_btn = tk.Button(
            btn_container,
            text="◀ Previous",
            command=self.prev_page,
            state=tk.DISABLED,
            **btn_style
        )
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        load_btn = tk.Button(
            btn_container,
            text="📁 Load PDF",
            command=self.load_pdf,
            bg='#27AE60',
            activebackground='#229954',
            **{k:v for k,v in btn_style.items() if k not in ['bg', 'activebackground']}
        )
        load_btn.grid(row=0, column=1, padx=5)
        
        zoom_out_btn = tk.Button(
            btn_container,
            text="Zoom -",
            command=self.zoom_out,
            **btn_style
        )
        zoom_out_btn.grid(row=0, column=2, padx=5)
        
        zoom_in_btn = tk.Button(
            btn_container,
            text="Zoom +",
            command=self.zoom_in,
            **btn_style
        )
        zoom_in_btn.grid(row=0, column=3, padx=5)
        
        fullscreen_btn = tk.Button(
            btn_container,
            text="⛶ Fullscreen",
            command=self.toggle_fullscreen,
            **btn_style
        )
        fullscreen_btn.grid(row=0, column=4, padx=5)
        
        self.next_btn = tk.Button(
            btn_container,
            text="Next ▶",
            command=self.next_page,
            state=tk.DISABLED,
            **btn_style
        )
        self.next_btn.grid(row=0, column=5, padx=5)
        
        print_btn = tk.Button(
            btn_container,
            text="🖨 Print",
            command=self.print_pdf,
            bg='#E67E22',
            activebackground='#D35400',
            **{k:v for k,v in btn_style.items() if k not in ['bg', 'activebackground']}
        )
        print_btn.grid(row=0, column=6, padx=5)
        
        download_btn = tk.Button(
            btn_container,
            text="💾 Download",
            command=self.download_pdf,
            bg='#8E44AD',
            activebackground='#7D3C98',
            **{k:v for k,v in btn_style.items() if k not in ['bg', 'activebackground']}
        )
        download_btn.grid(row=0, column=7, padx=5)
        
        export_btn = tk.Button(
            btn_container,
            text="📦 Export as exe",
            command=self.export_to_exe,
            bg='#16A085',
            activebackground='#138D75',
            **{k:v for k,v in btn_style.items() if k not in ['bg', 'activebackground']}
        )
        export_btn.grid(row=0, column=8, padx=5)
    
    def load_sounds(self):
        try:
            if os.path.exists('sounds/page_turn.wav'):
                self.page_turn_sound = pygame.mixer.Sound('sounds/page_turn.wav')
        except Exception as e:
            print(f"Sound loading error: {e}")
    
    def play_page_sound(self):
        if self.audio_available and self.sound_enabled and self.page_turn_sound:
            try:
                self.page_turn_sound.play()
            except:
                pass
    
    def load_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            if self.pdf_document:
                self.pdf_document.close()
            
            self.pdf_document = fitz.open(file_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            self.zoom_level = 1.0  # Reset zoom level
            
            filename = os.path.basename(file_path)
            self.title_label.config(text=filename)
            
            # Update canvas before loading
            self.canvas.update_idletasks()
            
            self.load_thumbnails()
            
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
            
            # Give a moment for UI to update before rendering
            self.root.after(100, self.show_page_with_flip)
            
            messagebox.showinfo("Success", f"Loaded PDF with {self.total_pages} pages!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {e}\n\nPlease make sure the PDF file is valid and not corrupted.")
    
    def load_thumbnails(self):
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        
        self.thumbnail_images = []
        
        for page_num in range(self.total_pages):
            page = self.pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            thumb_photo = ImageTk.PhotoImage(img)
            self.thumbnail_images.append(thumb_photo)
            
            thumb_frame = tk.Frame(self.thumbnail_frame, bg='#34495E', bd=1, relief=tk.RAISED)
            thumb_frame.pack(pady=5, padx=5)
            
            thumb_btn = tk.Button(
                thumb_frame,
                image=thumb_photo,
                command=lambda p=page_num: self.goto_page(p),
                bg='#34495E',
                activebackground='#2C3E50',
                bd=0
            )
            thumb_btn.pack()
            
            page_num_label = tk.Label(
                thumb_frame,
                text=f"{page_num + 1:02d}",
                font=('Arial', 8),
                bg='#34495E',
                fg='white'
            )
            page_num_label.pack()
    
    def goto_page(self, page_num):
        if 0 <= page_num < self.total_pages:
            self.current_page = page_num
            self.show_page_with_flip()
            self.play_page_sound()
    
    def show_page_with_flip(self):
        if not self.pdf_document or self.flip_animation_running:
            return
        
        self.flip_animation_running = True
        self.animate_page_flip_transition()
    
    def animate_page_flip_transition(self):
        """Smooth transition before main flip animation"""
        self.animate_page_flip()
    
    def animate_page_flip(self):
        page = self.pdf_document[self.current_page]
        
        # Force canvas update to get proper dimensions
        self.canvas.update_idletasks()
        
        zoom = fitz.Matrix(self.zoom_level * 2, self.zoom_level * 2)
        pix = page.get_pixmap(matrix=zoom)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        max_width = self.canvas.winfo_width() - 40
        max_height = self.canvas.winfo_height() - 40
        
        if max_width <= 1 or max_height <= 1:
            max_width = 1000
            max_height = 700
        
        # Maintain aspect ratio while fitting in canvas
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Create 3D flip animation effect
        self.create_3d_flip_animation(img)
        
        self.page_label.config(text=f"pages: {self.current_page + 1} / {self.total_pages}")
        
        self.flip_animation_running = False
    
    def create_3d_flip_animation(self, img):
        """Create realistic 3D page flip animation"""
        frames = 15  # Number of animation frames
        
        for i in range(frames):
            progress = i / frames
            
            # Calculate perspective transformation
            angle = progress * 180  # 0 to 180 degrees
            
            # Create flipped image with perspective
            flipped_img = self.apply_3d_perspective(img, angle, progress)
            
            photo = ImageTk.PhotoImage(flipped_img)
            
            self.canvas.delete('all')
            
            x = max(self.canvas.winfo_width() // 2, flipped_img.width // 2 + 20)
            y = max(self.canvas.winfo_height() // 2, flipped_img.height // 2 + 20)
            
            self.canvas.create_image(x, y, image=photo, anchor='center')
            self.canvas.image = photo
            
            self.root.update()
            self.root.after(30)  # Smooth animation delay
        
        # Final image with curl effect
        curl_img = self.add_page_curl_effect(img)
        photo = ImageTk.PhotoImage(curl_img)
        
        self.canvas.delete('all')
        
        x = max(self.canvas.winfo_width() // 2, curl_img.width // 2 + 20)
        y = max(self.canvas.winfo_height() // 2, curl_img.height // 2 + 20)
        
        self.canvas.create_image(x, y, image=photo, anchor='center')
        self.canvas.image = photo
    
    def apply_3d_perspective(self, img, angle, progress):
        """Apply 3D perspective transformation to simulate page turning"""
        width, height = img.size
        
        # Calculate perspective scale
        scale_x = abs(math.cos(math.radians(angle)))
        
        # Create new image with perspective
        new_width = max(int(width * scale_x), 1)
        
        if new_width < 5:
            new_width = 5
        
        # Resize with perspective effect
        perspective_img = img.resize((new_width, height), Image.Resampling.LANCZOS)
        
        # Create canvas for final image
        canvas_img = Image.new('RGB', (width, height), color=(139, 157, 168))
        
        # Calculate position to center the perspective image
        x_offset = (width - new_width) // 2
        
        # Paste perspective image
        canvas_img.paste(perspective_img, (x_offset, 0))
        
        # Add shadow effect for depth
        shadow_img = self.add_flip_shadow(canvas_img, progress, angle)
        
        return shadow_img
    
    def add_flip_shadow(self, img, progress, angle):
        """Add shadow effect during page flip for realism"""
        shadow_img = img.copy()
        draw = ImageDraw.Draw(shadow_img)
        
        width, height = img.size
        
        # Shadow intensity based on flip progress
        if angle < 90:
            # Left side shadow (page leaving)
            shadow_alpha = int(100 * (1 - progress))
            for i in range(int(width * 0.2)):
                alpha = shadow_alpha * (1 - i / (width * 0.2))
                gray = int(200 - alpha * 0.5)
                draw.line([(i, 0), (i, height)], fill=(gray, gray, gray))
        else:
            # Right side shadow (page arriving)
            shadow_alpha = int(100 * progress)
            for i in range(int(width * 0.2)):
                pos = width - i - 1
                alpha = shadow_alpha * (1 - i / (width * 0.2))
                gray = int(200 - alpha * 0.5)
                draw.line([(pos, 0), (pos, height)], fill=(gray, gray, gray))
        
        return shadow_img
    
    def add_page_curl_effect(self, img):
        """Enhanced realistic page curl effect with gradient shadows"""
        width, height = img.size
        
        curl_img = img.copy()
        draw = ImageDraw.Draw(curl_img)
        
        # Larger, more realistic curl
        curl_width = int(width * 0.18)
        curl_height = int(height * 0.30)
        
        # Main curl shadow with gradient
        shadow_polygon = [
            (width - curl_width, height - curl_height),
            (width, height - curl_height // 3),
            (width, height),
            (width - curl_width // 3, height)
        ]
        
        # Enhanced shadow layers for depth
        for i in range(40):
            offset = i * 1.5
            alpha = int(140 - (i * 3.5))
            gray = 170 - (i * 4)
            
            offset_polygon = [
                (shadow_polygon[0][0] + offset, shadow_polygon[0][1] + offset),
                (shadow_polygon[1][0], shadow_polygon[1][1] + offset // 2),
                shadow_polygon[2],
                (shadow_polygon[3][0] + offset // 2, shadow_polygon[3][1])
            ]
            
            draw.polygon(offset_polygon, fill=(gray, gray, gray))
        
        # Curl fold with realistic lighting
        curl_polygon = [
            (width - curl_width, height - curl_height),
            (width - 8, height - curl_height // 4),
            (width - 3, height - 8),
            (width - curl_width // 2, height - 3)
        ]
        
        # Gradient on curl surface
        for i in range(20):
            gray = 230 - (i * 6)
            offset_curl = [
                (curl_polygon[0][0] + i, curl_polygon[0][1] + i),
                (curl_polygon[1][0] - i//2, curl_polygon[1][1] + i//3),
                (curl_polygon[2][0] - i//3, curl_polygon[2][1] - i//3),
                (curl_polygon[3][0] + i//2, curl_polygon[3][1] - i//4)
            ]
            draw.polygon(offset_curl, fill=(gray, gray, min(gray + 15, 255)))
        
        # Bright highlight on curl edge
        highlight_line = [
            (width - curl_width, height - curl_height),
            (width - curl_width // 2, height - 5)
        ]
        draw.line(highlight_line, fill=(250, 250, 250), width=4)
        
        # Curl edge definition
        edge_line = [
            (width - 10, height - curl_height // 4),
            (width - 4, height - 10)
        ]
        draw.line(edge_line, fill=(180, 180, 185), width=3)
        
        # Add subtle inner shadow for depth
        inner_shadow = [
            (width - curl_width + 5, height - curl_height + 5),
            (width - 15, height - curl_height // 3 + 5)
        ]
        draw.line(inner_shadow, fill=(140, 140, 140), width=2)
        
        return curl_img
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page_with_flip()
            self.play_page_sound()
    
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page_with_flip()
            self.play_page_sound()
    
    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 0.2, 3.0)
        if self.pdf_document:
            self.show_page_with_flip()
    
    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 0.2, 0.5)
        if self.pdf_document:
            self.show_page_with_flip()
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
        if self.is_fullscreen:
            self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        else:
            self.root.unbind('<Escape>')
    
    def print_pdf(self):
        if not self.pdf_document:
            messagebox.showwarning("No PDF", "Please load a PDF first!")
            return
        
        try:
            import platform
            import tempfile
            
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            self.pdf_document.save(temp_pdf.name)
            temp_pdf.close()
            
            system = platform.system()
            if system == 'Windows':
                os.startfile(temp_pdf.name, 'print')
            elif system == 'Darwin':
                subprocess.run(['lpr', temp_pdf.name])
            else:
                subprocess.run(['lp', temp_pdf.name])
            
            messagebox.showinfo("Print", "PDF sent to default printer!")
        except Exception as e:
            messagebox.showwarning("Print Error", f"Could not print: {e}\n\nPlease download and print manually.")
    
    def download_pdf(self):
        if not self.pdf_document:
            messagebox.showwarning("No PDF", "Please load a PDF first!")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if save_path:
            try:
                self.pdf_document.save(save_path)
                messagebox.showinfo("Success", f"PDF saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {e}")
    
    def export_to_exe(self):
        import platform
        current_os = platform.system()
        
        if current_os != 'Windows':
            response = messagebox.askyesno(
                "Export to EXE",
                f"⚠️ Warning: You are on {current_os}\n\n"
                "Windows .exe should be built on Windows.\n"
                "Building on Linux/Mac will create a Linux/Mac executable.\n\n"
                "To build Windows .exe:\n"
                "1. Download all files\n"
                "2. Run on Windows PC\n"
                "3. Execute: python build_exe.py\n\n"
                "Continue with current OS build?"
            )
            if not response:
                return
        
        response = messagebox.askyesno(
            "Export to EXE",
            "This will create a standalone executable.\n\n"
            "The process will:\n"
            "1. Run PyInstaller to build the .exe\n"
            "2. Create output in 'dist' folder\n"
            "3. File size: ~20-30 MB\n\n"
            f"Target OS: {current_os}\n\n"
            "Continue?"
        )
        
        if response:
            try:
                if os.path.exists('build_exe.py'):
                    subprocess.Popen(['python3', 'build_exe.py'])
                    messagebox.showinfo(
                        "Build Started",
                        "EXE build process started!\n\n"
                        "Check the terminal for progress.\n"
                        f"Output will be in: dist/FlipbookPDFViewer{'exe' if current_os == 'Windows' else ''}\n\n"
                        "This may take 1-2 minutes..."
                    )
                else:
                    messagebox.showerror("Error", "build_exe.py not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start build: {e}")

def main():
    root = tk.Tk()
    app = FlipbookPDFViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
