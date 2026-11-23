import tkinter as tk
from tkinter import ttk
import random
import time
import csv
import os
import math

DATA_FILE = 'color_test_results.csv'

# Change this number to control iterations per color.
ITERATIONS_PER_COLOR = 10

COLOR_NAMES = [
    'Red', 'Brown', 'Green', 'Orange',
    'Yellow', 'Blue', 'Purple'
]

ORIGINAL = [
    '#FF0000', '#7F6000', '#9DE951', '#FEBC02',
    '#FFFF00', '#002F8E', '#7030A0'
]

MODIFIED = [
    '#EE4B2B', '#872309', '#AFE1AF', '#29CF23',
    '#23FA2D', '#00B0F0', '#180236'
]

FIELDS = [
    'name', 'palette', 'trial', 'target', 'target_hex', 'selected', 'selected_hex', 'correct', 'seconds'
]

class ColorTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title('Data Collection Color Test')
        self.root.geometry('850x700')
        self.root.minsize(750, 640)

        # Set main application background to white.
        self.root.configure(bg='white')

        # Configure ttk widgets to use a white theme.
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            'TFrame',
            background='white'
        )

        style.configure(
            'TLabel',
            background='white',
            foreground='black'
        )

        style.configure(
            'TButton',
            background='white',
            foreground='black',
            bordercolor='black',
            focuscolor='white'
        )

        style.map(
            'TButton',
            background=[
                ('active', 'white'),
                ('pressed', 'white')
            ],
            foreground=[
                ('active', 'black'),
                ('pressed', 'black')
            ]
        )
        # Configure results table.
        style.configure(
            'Treeview',
            background='white',
            fieldbackground='white',
            foreground='black'
        )
        style.map(
            'Treeview',
            background=[
                ('selected', 'white')
            ],
            foreground=[
                ('selected', 'black')
            ]
        )
        style.configure(
            'Treeview.Heading',
            background='white',
            foreground='black'
        )
        style.map(
            'Treeview.Heading',
            background=[
                ('active', 'white')
            ]
        )
        self.show_menu()

    def show_dialog(self, title, message, confirm=False):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.resizable(False, False)

        result = {'value': False}

        tk.Label(
            dialog,
            text=message,
            bg='white',
            fg='black',
            font=('Arial', 11),
            wraplength=350,
            justify='center'
        ).pack(padx=25, pady=25)

        buttons = tk.Frame(
            dialog,
            bg='white'
        )
        buttons.pack(pady=(0, 20))

        def close(value):
            result['value'] = value
            dialog.destroy()

        if confirm:
            tk.Button(
                buttons,
                text='Yes',
                command=lambda: close(True),
                bg='white',
                fg='black',
                activebackground='white',
                activeforeground='black',
                width=12
            ).pack(side='left', padx=5)

            tk.Button(
                buttons,
                text='No',
                command=lambda: close(False),
                bg='white',
                fg='black',
                activebackground='white',
                activeforeground='black',
                width=12
            ).pack(side='left', padx=5)

        else:
            tk.Button(
                buttons,
                text='OK',
                command=lambda: close(True),
                bg='white',
                fg='black',
                activebackground='white',
                activeforeground='black',
                width=12
            ).pack()

        dialog.protocol(
            'WM_DELETE_WINDOW',
            lambda: close(False)
        )

        dialog.update_idletasks()

        width = dialog.winfo_reqwidth()
        height = dialog.winfo_reqheight()

        x = (
            self.root.winfo_rootx()
            + (self.root.winfo_width() - width) // 2
        )
        y = (
            self.root.winfo_rooty()
            + (self.root.winfo_height() - height) // 2
        )
        dialog.geometry(
            f'{width}x{height}+{x}+{y}'
        )
        dialog.grab_set()
        self.root.wait_window(dialog)

        return result['value']

    def ask_participant(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('Participant')
        dialog.geometry('300x160')
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.resizable(False, False)

        name = tk.StringVar()
        result = {'name': None}

        tk.Label(
            dialog,
            text='Enter your name:',
            bg='white',
            fg='black',
            font=('Arial', 11)
        ).pack(pady=(20, 5))

        entry = tk.Entry(
            dialog,
            textvariable=name,
            bg='white',
            fg='black',
            insertbackground='black',
            relief='solid'
        )

        entry.pack(
            padx=20,
            fill='x'
        )

        def submit():
            result['name'] = name.get()
            dialog.destroy()

        def cancel():
            dialog.destroy()

        buttons = tk.Frame(
            dialog,
            bg='white'
        )
        buttons.pack(pady=15)

        tk.Button(
            buttons,
            text='OK',
            command=submit,
            bg='white',
            fg='black',
            activebackground='white',
            activeforeground='black',
            width=10
        ).pack(side='left', padx=5)

        tk.Button(
            buttons,
            text='Cancel',
            command=cancel,
            bg='white',
            fg='black',
            activebackground='white',
            activeforeground='black',
            width=10
        ).pack(side='left', padx=5)

        entry.focus_set()

        dialog.bind(
            '<Return>',
            lambda event: submit()
        )

        dialog.bind(
            '<Escape>',
            lambda event: cancel()
        )

        dialog.protocol(
            'WM_DELETE_WINDOW',
            cancel
        )

        dialog.grab_set()
        self.root.wait_window(dialog)

        return result['name']

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_screen()

        frame = ttk.Frame(
            self.root,
            padding=35
        )
        frame.pack(expand=True)

        ttk.Label(
            frame,
            text='Color Matching Test',
            font=('Arial', 22, 'bold')
        ).pack(pady=20)

        ttk.Button(
            frame,
            text='Start Test',
            command=self.start_test,
            width=26
        ).pack(pady=10)

        ttk.Button(
            frame,
            text='Results',
            command=self.show_results,
            width=26
        ).pack(pady=10)

        ttk.Button(
            frame,
            text='Clear Data',
            command=self.clear_data,
            width=26
        ).pack(pady=10)

    def start_test(self):
        name = self.ask_participant()

        if not name or not name.strip():
            return

        self.name = name.strip()

        self.trials = []

        for palette_name, palette in [
            ('Original', ORIGINAL),
            ('Modified', MODIFIED)
        ]:

            targets = (
                list(range(7)) * ITERATIONS_PER_COLOR
            )

            random.shuffle(targets)

            for target in targets:
                self.trials.append(
                    (palette_name, palette, target)
                )

        self.trial_index = 0
        self.session_rows = []

        self.show_trial()

    def show_trial(self):
        if self.trial_index >= len(self.trials):
            self.finish_test()
            return

        self.clear_screen()

        palette_name, palette, target = (
            self.trials[self.trial_index]
        )

        self.current_palette_name = palette_name
        self.current_target = target
        self.current_palette = palette

        ttk.Label(
            self.root,
            text=f'{palette_name} Colors',
            font=('Arial', 18, 'bold')
        ).pack(pady=(15, 5))

        ttk.Label(
            self.root,
            text=(
                f'Trial {self.trial_index + 1} '
                f'of {len(self.trials)}'
            )
        ).pack()

        ttk.Label(
            self.root,
            text='Click the outer circle that matches the center color.'
        ).pack(pady=8)

        canvas = tk.Canvas(
            self.root,
            width=650,
            height=530,
            bg='white',
            highlightthickness=0
        )

        canvas.pack(
            expand=True,
            pady=8
        )

        center_x, center_y = 325, 265

        # Target in center: larger than all seven choices.
        canvas.create_oval(
            center_x - 72,
            center_y - 72,
            center_x + 72,
            center_y + 72,
            fill=palette[target],
            outline=''
        )

        order = list(range(7))
        random.shuffle(order)

        for position, color_index in enumerate(order):

            angle = (
                (2 * math.pi * position / 7)
                - math.pi / 2
            )

            x = (
                center_x
                + 225 * math.cos(angle)
            )

            y = (
                center_y
                + 205 * math.sin(angle)
            )

            item = canvas.create_oval(
                x - 42,
                y - 42,
                x + 42,
                y + 42,
                fill=palette[color_index],
                outline=''
            )

            canvas.tag_bind(
                item,
                '<Button-1>',
                lambda event, choice=color_index:
                    self.record_answer(choice)
            )

        self.started_at = time.perf_counter()

    def record_answer(self, selected):
        elapsed = (
            time.perf_counter() - self.started_at
        )

        row = {
            'name': self.name,
            'palette': self.current_palette_name,
            'trial': self.trial_index + 1,
            'target': COLOR_NAMES[self.current_target],
            'target_hex': MODIFIED[self.current_target] if (self.current_palette_name == "Modified") else ORIGINAL[self.current_target],
            'selected': COLOR_NAMES[selected],
            'selected_hex': MODIFIED[selected] if (self.current_palette_name == "Modified") else ORIGINAL[selected],
            'correct': int(
                selected == self.current_target
            ),
            'seconds': f'{elapsed:.3f}'
        }
        print(row)
        self.session_rows.append(row)

        self.trial_index += 1

        self.show_trial()

    def finish_test(self):
        exists = (
            os.path.isfile(DATA_FILE)
            and os.path.getsize(DATA_FILE) > 0
        )

        with open(
            DATA_FILE,
            'a',
            newline='',
            encoding='utf-8'
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=FIELDS
            )

            if not exists:
                writer.writeheader()

            writer.writerows(
                self.session_rows
            )
        
        correct = sum(
            int(row['correct']) for row in self.session_rows
        )

        total = len(self.session_rows)

        self.show_dialog(
            'Test Complete',
            (
                f'Thank you, {self.name}!\n\n'
                f'Correct: {correct}/{total}\n'
                f'Accuracy: {correct / total * 100:.1f}%\n\n'
                f'Results saved.'
            )
        )

        self.show_menu()

    def read_results(self):
        if not os.path.isfile(DATA_FILE):
            return []

        with open(
            DATA_FILE,
            newline='',
            encoding='utf-8'
        ) as file:

            return list(
                csv.DictReader(file)
            )
        
    def show_results(self):
        self.clear_screen()

        ttk.Label(
            self.root,
            text='Participant Results',
            font=('Arial', 20, 'bold')
        ).pack(pady=18)

        rows = self.read_results()

        if not rows:
            ttk.Label(
                self.root,
                text='No results saved yet.'
            ).pack(pady=25)

        else:
            # Group results by participant.
            grouped = {}

            for row in rows:
                key = row['name']

                grouped.setdefault(
                    key,
                    []
                ).append(row)

            columns = (
                'Name',
                'Palette',
                'Correct',
                'Accuracy',
                'Avg Time'
            )

            tree = ttk.Treeview(
                self.root,
                columns=columns,
                show='headings',
                height=19
            )

            for col in columns:
                tree.heading(
                    col,
                    text=col
                )

                tree.column(
                    col,
                    width=130 if col != 'Name' else 150,
                    anchor='center'
                )

            # Display individual palette results and overall results.
            for name, group in grouped.items():

                for palette in ['Original', 'Modified']:

                    palette_group = [
                        row for row in group
                        if row['palette'] == palette
                    ]

                    if not palette_group:
                        continue

                    total = len(palette_group)

                    correct = sum(
                        int(row['correct'])
                        for row in palette_group
                    )

                    avg = sum(
                        float(row['seconds'])
                        for row in palette_group
                    ) / total

                    tree.insert(
                        '',
                        'end',
                        values=(
                            name,
                            palette,
                            f'{correct}/{total}',
                            f'{100 * correct / total:.1f}%',
                            f'{avg:.2f}s'
                        )
                    )

                # Calculate combined results for both palettes.
                total = len(group)

                correct = sum(
                    int(row['correct'])
                    for row in group
                )

                avg = sum(
                    float(row['seconds'])
                    for row in group
                ) / total

                tree.insert(
                    '',
                    'end',
                    values=(
                        name,
                        'Overall (Both)',
                        f'{correct}/{total}',
                        f'{100 * correct / total:.1f}%',
                        f'{avg:.2f}s'
                    ),
                    tags=('overall',)
                )

            # Keep overall results white and bold.
            tree.tag_configure(
                'overall',
                background='white',
                foreground='black',
                font=('Arial', 10, 'bold')
            )

            tree.pack(
                fill='both',
                expand=True,
                padx=18,
                pady=8
            )

            # Display participant count.
            ttk.Label(
                self.root,
                text=f'{len(grouped)} participant(s).'
            ).pack()

        ttk.Button(
            self.root,
            text='Back to Menu',
            command=self.show_menu
        ).pack(pady=20)

    def clear_data(self):
        confirm = self.show_dialog(
            'Confirm Delete',
            'Permanently delete ALL saved participant results?',
            confirm=True
        )

        if confirm:
            if os.path.isfile(DATA_FILE):
                os.remove(DATA_FILE)

            self.show_dialog(
                'Cleared',
                'All saved results have been deleted.'
            )

if __name__ == '__main__':
    root = tk.Tk()

    app = ColorTestApp(root)

    root.mainloop()
