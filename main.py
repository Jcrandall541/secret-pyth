# Run `python main.py` in the terminal
import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime, timedelta
import threading
import time

class SolscanTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Solscan Token Tracker")
        self.root.configure(bg='black')
        
        # Store running totals for different timeframes
        self.totals = {
            '1min': {},
            '5min': {}
        }
        
        # Create main container
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create notebook for different timeframes
        style = ttk.Style()
        style.configure('Custom.TNotebook', background='black')
        style.configure('Custom.TNotebook.Tab', background='grey', foreground='white')
        
        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        
        # Create frames for different timeframes
        self.frames = {}
        for timeframe in ['1min', '5min']:
            frame = tk.Frame(self.notebook, bg='black')
            self.frames[timeframe] = frame
            self.notebook.add(frame, text=f'{timeframe} View')
            
            # Create treeview for each timeframe
            tree = ttk.Treeview(frame, columns=('Token', 'Buys', 'Sells', 'Net Volume'), show='headings')
            tree.heading('Token', text='Token')
            tree.heading('Buys', text='Buys (SOL)')
            tree.heading('Sells', text='Sells (SOL)')
            tree.heading('Net Volume', text='Net Volume')
            
            # Configure treeview colors
            style.configure('Treeview', 
                          background='black',
                          foreground='white',
                          fieldbackground='black')
            style.configure('Treeview.Heading',
                          background='grey',
                          foreground='white')
            
            tree.pack(expand=True, fill='both')
            self.frames[timeframe + '_tree'] = tree
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_transactions)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def get_top_tokens(self):
        """Fetch top 50 tokens from Solscan API"""
        try:
            # Note: This is a placeholder URL - you'll need to use the actual Solscan API endpoint
            url = "https://api.solscan.io/tokens"
            response = requests.get(url)
            data = response.json()
            return data['tokens'][:50]  # Return top 50 tokens
        except Exception as e:
            print(f"Error fetching tokens: {e}")
            return []
    
    def get_token_transactions(self, token_address, timeframe):
        """Fetch token transactions from Solscan API"""
        try:
            # Note: This is a placeholder URL - you'll need to use the actual Solscan API endpoint
            url = f"https://api.solscan.io/transactions"{eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MjE3OTMyMjE0NjEsImVtYWlsIjoiY3JhbmRhbGxqZXJlbXkxQGdtYWlsLmNvbSIsImFjdGlvbiI6InRva2VuLWFwaSIsImFwaVZlcnNpb24iOiJ2MiIsImlhdCI6MTcyMTc5MzIyMX0.lS1u_L5wNjUo8Y-wTZrRhNoSYu-RshhWrsh7Dt-Mgyw}"
            params = {
                'timeframe': timeframe
            }
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def update_display(self, timeframe):
        """Update the treeview display for a specific timeframe"""
        tree = self.frames[timeframe + '_tree']
        
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # Add updated data
        for token, data in self.totals[timeframe].items():
            tree.insert('', 'end', values=(
                token,
                f"{data['buys']:.3f}",
                f"{data['sells']:.3f}",
                f"{data['buys'] - data['sells']:.3f}"
            ))
    
    def monitor_transactions(self):
        """Main monitoring loop"""
        while self.monitoring:
            tokens = self.get_top_tokens()
            
            for token in tokens:
                # Process 1min timeframe
                transactions_1min = self.get_token_transactions(token['address'], '1min')
                self.process_transactions('1min', token['symbol'], transactions_1min)
                
                # Process 5min timeframe
                transactions_5min = self.get_token_transactions(token['address'], '5min')
                self.process_transactions('5min', token['symbol'], transactions_5min)
            
            # Update displays
            for timeframe in ['1min', '5min']:
                self.update_display(timeframe)
            
            # Wait before next update
            time.sleep(60)  # Update every minute
    
    def process_transactions(self, timeframe, token_symbol, transactions):
        """Process transactions and update running totals"""
        if token_symbol not in self.totals[timeframe]:
            self.totals[timeframe][token_symbol] = {'buys': 0, 'sells': 0}
        
        for tx in transactions:
            if tx['type'] == 'buy':
                self.totals[timeframe][token_symbol]['buys'] += float(tx['amount'])
            elif tx['type'] == 'sell':
                self.totals[timeframe][token_symbol]['sells'] += float(tx['amount'])
    
    def cleanup(self):
        """Cleanup method to be called when closing the application"""
        self.monitoring = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Root()
    app = SolscanTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.mainloop()
# Note: Python is lazy loaded so the first run will take a moment,
# But after cached, subsequent loads are super fast! ⚡️

import platform
print(f"Hello Python v{platform.python_version()}!")