import tkinter as tk
from tkinter import scrolledtext, ttk, font
import asyncio
import threading
import re
from google.genai import types
from agent import runner, memory_service, get_or_create_session

# Constants
USER_ID = "Noah_Haag"
SESSION_ID = "Job_Search"

# Theme Colors
BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
INPUT_BG = "#3c3f41"
ACCENT_COLOR = "#4a90e2"
BUTTON_BG = "#3c3f41"
BUTTON_FG = "#ffffff"
CODE_BG = "#1e1e1e"
CODE_FG = "#d4d4d4"

class AgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent V2 Lite UI")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)

        self.configure_styles()

        # Main Layout - PanedWindow
        self.paned_window = ttk.PanedWindow(root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Chat History Frame
        chat_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(chat_frame, weight=3)

        # Chat History Text Area
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame, 
            state='disabled', 
            wrap=tk.WORD, 
            font=("Segoe UI", 11),
            bg=BG_COLOR,
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            selectbackground=ACCENT_COLOR,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # Configure Tags for Rich Text
        self.chat_history.tag_config("user_header", foreground="#98c379", font=("Segoe UI", 10, "bold"))
        self.chat_history.tag_config("agent_header", foreground="#61afef", font=("Segoe UI", 10, "bold"))
        self.chat_history.tag_config("system_header", foreground="#e06c75", font=("Segoe UI", 10, "bold"))
        self.chat_history.tag_config("bold", font=("Segoe UI", 11, "bold"))
        self.chat_history.tag_config("code", background=CODE_BG, foreground=CODE_FG, font=("Consolas", 10))
        self.chat_history.tag_config("separator", foreground="#555555")

        # Input Area Frame
        input_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(input_frame, weight=1)

        # Input Text
        self.user_input = tk.Text(
            input_frame, 
            height=5, 
            wrap=tk.WORD, 
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind keys
        self.user_input.bind("<Return>", self.on_enter_pressed)
        self.user_input.bind("<Shift-Return>", lambda e: None)

        # Send Button
        self.send_btn = tk.Button(
            input_frame, 
            text="SEND", 
            command=self.send_message, 
            bg=ACCENT_COLOR, 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#357abd",
            activeforeground="white",
            width=10,
            cursor="hand2"
        )
        self.send_btn.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Initializing...")
        self.status_bar = tk.Label(
            root, 
            textvariable=self.status_var, 
            bg="#21252b", 
            fg="#abb2bf", 
            bd=0, 
            anchor=tk.W,
            padx=10,
            pady=5,
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Asyncio Loop
        self.loop = asyncio.new_event_loop()
        self.agent_thread = threading.Thread(target=self.start_async_loop, daemon=True)
        self.agent_thread.start()

        # Initialize Session
        self.run_async(self.initialize_session())

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TPanedwindow", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR)

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_async(self, coro):
        asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def initialize_session(self):
        try:
            self.session = await get_or_create_session(USER_ID, SESSION_ID)
            await memory_service.add_session_to_memory(self.session)
            self.schedule_ui_update(self.update_status, "Agent Connected. Ready.")
            self.schedule_ui_update(self.append_message, "System", "Agent connected successfully.")
        except Exception as e:
            self.schedule_ui_update(self.update_status, f"Error connecting: {e}")
            self.schedule_ui_update(self.append_message, "System", f"Error: {e}")

    def on_enter_pressed(self, event):
        if event.state & 0x0001: # Shift key is down
            return None 
        self.send_message()
        return "break"

    def send_message(self):
        text = self.user_input.get("1.0", tk.END).strip()
        if not text:
            return

        self.user_input.delete("1.0", tk.END)
        self.append_message("You", text)
        self.update_status("Agent is thinking...")
        
        self.run_async(self.process_agent_turn(text))

    async def process_agent_turn(self, text):
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=text)]
        )
        
        full_response = ""
        try:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=user_message
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        text_parts = [p.text for p in event.content.parts if p.text]
                        if text_parts:
                            chunk = "\n".join(text_parts)
                            full_response = chunk
            
            if full_response:
                self.schedule_ui_update(self.append_message, "Agent", full_response)
                self.schedule_ui_update(self.update_status, "Ready.")
            else:
                 self.schedule_ui_update(self.append_message, "Agent", "(No text response)")
                 self.schedule_ui_update(self.update_status, "Ready.")

        except Exception as e:
            self.schedule_ui_update(self.append_message, "System", f"Error: {e}")
            self.schedule_ui_update(self.update_status, "Error.")

    def schedule_ui_update(self, func, *args):
        self.root.after(0, func, *args)

    def append_message(self, sender, message):
        self.chat_history.configure(state='normal')
        
        # Insert Header
        tag = "user_header" if sender == "You" else "agent_header" if sender == "Agent" else "system_header"
        self.chat_history.insert(tk.END, f"[{sender}]\n", tag)
        
        # Insert Message with Markdown Parsing
        self.insert_markdown_text(message)
        
        # Insert Separator
        self.chat_history.insert(tk.END, "\n" + "-"*50 + "\n\n", "separator")
        
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def insert_markdown_text(self, text):
        """
        Simple parser to handle **bold** and ```code blocks```.
        """
        # Split by code blocks first
        parts = re.split(r'(```[\s\S]*?```)', text)
        
        for part in parts:
            if part.startswith("```") and part.endswith("```"):
                # Code block
                code_content = part[3:-3].strip()
                self.chat_history.insert(tk.END, f"\n{code_content}\n", "code")
            else:
                # Normal text with bold parsing
                self.insert_bold_text(part)

    def insert_bold_text(self, text):
        # Split by bold markers
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                content = part[2:-2]
                self.chat_history.insert(tk.END, content, "bold")
            else:
                self.chat_history.insert(tk.END, part)

    def update_status(self, text):
        self.status_var.set(text)

if __name__ == "__main__":
    root = tk.Tk()
    app = AgentGUI(root)
    root.mainloop()
