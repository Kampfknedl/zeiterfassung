from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
import os
import datetime
import db

KV = '''
RootWidget:
    orientation: 'vertical'
    spacing: 4

    # Row 1: customer selection - responsive
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '140dp'
        spacing: 4
        Label:
            text: 'Kunde:'
            size_hint_y: None
            height: '30dp'
        Spinner:
            id: customer_spinner
            text: root.customers[0] if root.customers else '—'
            values: root.customers
            size_hint_y: None
            height: '40dp'
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: 4
            Button:
                text: '+ Kunde'
                on_release: root.add_customer()
            Button:
                text: 'Kunden verwalten'
                on_release: root.open_customer_management()

    # Row 2: activity, date, hours - responsive
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '200dp'
        spacing: 4
        Label:
            text: 'Tätigkeit:'
            size_hint_y: None
            height: '30dp'
        TextInput:
            id: activity_input
            multiline: False
            size_hint_y: None
            height: '40dp'
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: 4
            Label:
                text: 'Datum:'
                size_hint_x: None
                width: '60dp'
            TextInput:
                id: date_input
                text: ''
                hint_text: 'dd.mm.yyyy'
                multiline: False
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: 4
            Label:
                text: 'Std:'
                size_hint_x: None
                width: '40dp'
            TextInput:
                id: hours_input
                text: '1.0'
                input_filter: 'float'
                multiline: False
            Button:
                text: 'Eintrag'
                on_release: root.add_entry(activity_input.text, hours_input.text)

    # Row 3: actions
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '120dp'
        spacing: 4
        Button:
            text: 'Report (PDF)'
            size_hint_y: None
            height: '40dp'
            on_release: root.export_pdf()
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: 4
            Button:
                id: start_btn
                text: 'Start'
                on_release: root.start_timer()
            Button:
                id: pause_btn
                text: 'Pause'
                disabled: True
                on_release: root.pause_timer()
            Button:
                id: stop_btn
                text: 'Stop'
                on_release: root.stop_timer()

    Label:
        text: 'Letzte Einträge:'
        size_hint_y: None
        height: '30dp'

    ScrollView:
        do_scroll_x: False
        BoxLayout:
            id: entries_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 4

    Label:
        text: 'made by Benedikt Bernhart'
        size_hint_y: None
        height: '20dp'
        font_size: '10sp'
        color: 0.5, 0.5, 0.5, 1
'''


class RootWidget(BoxLayout):
    customers = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer_start = None
        self._timer_paused_time = 0  # accumulated paused seconds
        self._pause_start = None      # when pause was pressed

    def on_kv_post(self, base_widget):
        # Ensure DB initialized before attempting queries
        db.init_db(self.get_db_path())
        self.load_customers()
        self.refresh_entries()
        # Debug: print ids and children for visibility troubleshooting
        try:
            print("RootWidget ids:", list(self.ids.keys()))
            print("RootWidget children count:", len(self.children))
            print("Customers:", self.customers)
        except Exception:
            pass
        # set default date for manual entries
        try:
            self.ids.date_input.text = datetime.date.today().strftime("%d.%m.%Y")
        except Exception:
            pass
        # setup activity suggestions
        try:
            self._activity_dropdown = None
            self.ids.activity_input.bind(text=self.on_activity_text)
            self.ids.activity_input.bind(focus=self.on_activity_focus)
        except Exception:
            pass
        # bind customer spinner change to refresh entries
        try:
            self.ids.customer_spinner.bind(text=self.on_customer_changed)
        except Exception:
            pass

    def show_error(self, title, message):
        # Show a scrollable error popup and also write a log file for easier sharing
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.scrollview import ScrollView
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            root = BoxLayout(orientation='vertical', spacing=8)
            sv = ScrollView(size_hint=(1, 1))
            lbl = Label(text=message, size_hint_y=None)
            # enable wrapping
            lbl.bind(width=lambda inst, w: setattr(inst, 'text_size', (w, None)))
            # estimate height based on content length
            lbl.bind(texture_size=lambda inst, ts: setattr(inst, 'height', ts[1] + 20))
            sv.add_widget(lbl)
            root.add_widget(sv)
            btn = Button(text='OK', size_hint_y=None, height='40dp')
            root.add_widget(btn)
            popup = Popup(title=title, content=root, size_hint=(.9, .7))
            btn.bind(on_release=popup.dismiss)
            popup.open()
        except Exception:
            # As a last resort, try a minimal popup
            try:
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                Popup(title=title, content=Label(text=message[:500]), size_hint=(.9, .6)).open()
            except Exception:
                pass

    def write_error_log(self, text):
        try:
            out_dir = self.get_documents_dir()
            os.makedirs(out_dir, exist_ok=True)
            p = os.path.join(out_dir, 'zeiterfassung_error.log')
            with open(p, 'a', encoding='utf-8') as f:
                f.write('\n=== ERROR ===\n')
                f.write(datetime.datetime.now().isoformat() + '\n')
                f.write(text)
                f.write('\n')
            return p
        except Exception:
            return None

    def on_customer_changed(self, instance, value):
        """Called when customer spinner selection changes - refresh entries list"""
        self.refresh_entries()

    def on_activity_focus(self, instance, value):
        # dismiss dropdown when focus lost
        if not value and getattr(self, '_activity_dropdown', None):
            try:
                self._activity_dropdown.dismiss()
            except Exception:
                pass

    def on_activity_text(self, instance, value):
        prefix = (value or '').strip()
        if not prefix:
            if getattr(self, '_activity_dropdown', None):
                try:
                    self._activity_dropdown.dismiss()
                except Exception:
                    pass
            return
        # fetch suggestions
        suggestions = db.get_recent_activities(self.get_db_path(), prefix=prefix, limit=8)
        if not suggestions:
            if getattr(self, '_activity_dropdown', None):
                try:
                    self._activity_dropdown.dismiss()
                except Exception:
                    pass
            return
        self.show_activity_dropdown(suggestions, instance)

    def show_activity_dropdown(self, suggestions, target_widget):
        from kivy.uix.dropdown import DropDown
        from kivy.uix.button import Button
        # dismiss older
        if getattr(self, '_activity_dropdown', None):
            try:
                self._activity_dropdown.dismiss()
            except Exception:
                pass
        dd = DropDown()
        for s in suggestions:
            btn = Button(text=s, size_hint_y=None, height='36dp')
            btn.bind(on_release=lambda btn: dd.select(btn.text))
            dd.add_widget(btn)

        def on_select(instance, selection):
            try:
                target_widget.text = selection
            except Exception:
                pass
            try:
                dd.dismiss()
            except Exception:
                pass

        dd.bind(on_select=on_select)
        # open dropdown under the target widget
        dd.open(target_widget)
        self._activity_dropdown = dd

    def get_db_path(self):
        app_dir = App.get_running_app().user_data_dir
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, 'stundenerfassung.db')

    def get_db_dir(self):
        return os.path.dirname(self.get_db_path())

    def get_documents_dir(self):
        # Prefer Android public Documents; fallback to OS Documents or app data
        try:
            from jnius import autoclass
            Environment = autoclass('android.os.Environment')
            docs = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS)
            return docs.getAbsolutePath()
        except Exception:
            try:
                return os.path.join(os.path.expanduser('~'), 'Documents')
            except Exception:
                return self.get_db_dir()

    def get_downloads_dir(self):
        # Try Android public Downloads directory; fallback to OS Downloads or app data
        try:
            from jnius import autoclass
            Environment = autoclass('android.os.Environment')
            downloads = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            return downloads.getAbsolutePath()
        except Exception:
            try:
                return os.path.join(os.path.expanduser('~'), 'Downloads')
            except Exception:
                return self.get_db_dir()

    def share_pdf(self, filepath):
        # Open Android share intent for the PDF file
        if not os.path.exists(filepath):
            self.show_error('Fehler', f'Datei nicht gefunden: {filepath}')
            return
            
        try:
            from jnius import autoclass, cast
            PythonJavaClass = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            
            # Try to use FileProvider for secure sharing (Android 7+)
            try:
                FileProvider = autoclass('androidx.core.content.FileProvider')
                context = PythonJavaClass.mActivity
                authority = f"{context.getPackageName()}.fileprovider"
                java_file = File(filepath)
                file_uri = FileProvider.getUriForFile(context, authority, java_file)
            except Exception as e:
                # Fallback to direct file:// URI for older Android or if FileProvider fails
                print(f"FileProvider failed ({e}), using direct URI")
                java_file = File(filepath)
                file_uri = Uri.fromFile(java_file)

            # Create share intent
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.putExtra(Intent.EXTRA_STREAM, file_uri)
            intent.setType("application/pdf")
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

            # Start share intent chooser (shows WhatsApp, Email, etc.)
            chooser = Intent.createChooser(intent, "Report teilen über...")
            PythonJavaClass.mActivity.startActivity(chooser)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            error_msg = f"Fehler beim Teilen: {str(e)}\n\n{tb}"
            self.show_error('Fehler', error_msg)
            self.write_error_log(error_msg)

    def load_customers(self):
        path = self.get_db_path()
        self.customers = db.get_customers(path)

    def add_customer(self):
        # Simple form to add customer with address/email/phone
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        content = BoxLayout(orientation='vertical', spacing=8)
        name_input = TextInput(multiline=False, hint_text='Name')
        address_input = TextInput(multiline=False, hint_text='Adresse')
        email_input = TextInput(multiline=False, hint_text='Email')
        phone_input = TextInput(multiline=False, hint_text='Telefon')
        btn = BoxLayout(size_hint_y=None, height='40dp')
        btn_ok = Button(text='Speichern')
        btn_cancel = Button(text='Abbrechen')
        content.add_widget(name_input)
        content.add_widget(address_input)
        content.add_widget(email_input)
        content.add_widget(phone_input)
        btn.add_widget(btn_ok)
        btn.add_widget(btn_cancel)
        content.add_widget(btn)
        popup = Popup(title='Neuer Kunde', content=content, size_hint=(.9, .6))

        def do_add(*a):
            name = name_input.text.strip()
            if name:
                path = self.get_db_path()
                # add customer and update details
                db.add_customer(path, name)
                db.update_customer(path, name, address_input.text.strip(), email_input.text.strip(), phone_input.text.strip())
                self.load_customers()
                popup.dismiss()

        btn_ok.bind(on_release=do_add)
        btn_cancel.bind(on_release=lambda *x: popup.dismiss())
        popup.open()

    def open_customer_management(self):
        # Popup to list and edit customers
        from kivy.uix.popup import Popup
        from kivy.uix.recycleview import RecycleView
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput

        layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        from kivy.uix.label import Label
        for name in self.customers:
            row = BoxLayout(size_hint_y=None, height='40dp')
            lbl = Label(text=name)
            edit_btn = Button(text='Bearbeiten', size_hint_x=None, width='100dp')
            del_btn = Button(text='Löschen', size_hint_x=None, width='80dp')

            def make_edit(n):
                def _edit(*a):
                    self.open_edit_customer(n, popup)
                return _edit

            def make_delete(n):
                def _delete(*a):
                    path = self.get_db_path()
                    db.delete_customer(path, n)
                    self.load_customers()
                    popup.dismiss()
                    self.open_customer_management()
                return _delete

            edit_btn.bind(on_release=make_edit(name))
            del_btn.bind(on_release=make_delete(name))
            row.add_widget(lbl)
            row.add_widget(edit_btn)
            row.add_widget(del_btn)
            layout.add_widget(row)

        from kivy.uix.scrollview import ScrollView
        sv = ScrollView(size_hint=(1, .8))
        sv.add_widget(layout)
        root = BoxLayout(orientation='vertical')
        root.add_widget(sv)
        close = Button(text='Schließen', size_hint_y=None, height='40dp')
        root.add_widget(close)
        popup = Popup(title='Kunden verwalten', content=root, size_hint=(.95, .9))
        close.bind(on_release=popup.dismiss)
        popup.open()

    def open_edit_customer(self, name, parent_popup=None):
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        info = db.get_customer(self.get_db_path(), name)
        if not info:
            return
        _, name, address, email, phone = info
        content = BoxLayout(orientation='vertical', spacing=8)
        name_input = TextInput(text=name, multiline=False)
        address_input = TextInput(text=address or '', multiline=False)
        email_input = TextInput(text=email or '', multiline=False)
        phone_input = TextInput(text=phone or '', multiline=False)
        btn = BoxLayout(size_hint_y=None, height='40dp')
        ok = Button(text='Speichern')
        cancel = Button(text='Abbrechen')
        btn.add_widget(ok)
        btn.add_widget(cancel)
        content.add_widget(name_input)
        content.add_widget(address_input)
        content.add_widget(email_input)
        content.add_widget(phone_input)
        content.add_widget(btn)
        popup = Popup(title=f'Kunde bearbeiten: {name}', content=content, size_hint=(.9, .6))

        def do_save(*a):
            new_name = name_input.text.strip()
            # update name and details
            db.update_customer_full(self.get_db_path(), name, new_name=new_name, address=address_input.text.strip(), email=email_input.text.strip(), phone=phone_input.text.strip())
            # Note: We don't update the primary key name changes extensively here for simplicity
            self.load_customers()
            popup.dismiss()
            if parent_popup:
                parent_popup.dismiss()

        ok.bind(on_release=do_save)
        cancel.bind(on_release=lambda *x: popup.dismiss())
        popup.open()

    def add_entry(self, activity, hours):
        customer = self.ids.customer_spinner.text
        try:
            hours_f = float(hours)
        except Exception:
            hours_f = 1.0
        # allow manual date entry in format dd.mm.yyyy for backdating
        date_text = (self.ids.date_input.text or '').strip()
        start = None
        end = None
        try:
            if date_text:
                dt = datetime.datetime.strptime(date_text, "%d.%m.%Y")
                # store as ISO date (no time)
                start = dt.date().isoformat()
                end = start
        except Exception:
            start = None
            end = None

        if not start:
            now = datetime.datetime.now().isoformat()
            start = now
            end = now

        path = self.get_db_path()
        db.add_entry(path, customer, activity or 'Keine Angabe', start, end, hours_f)
        self.refresh_entries()

    def start_timer(self):
        customer = self.ids.customer_spinner.text
        if not customer or customer == '—':
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title='Fehler', content=Label(text='Bitte Kunde auswählen'), size_hint=(.6, .3)).open()
            return
        if self._timer_start is not None:
            # already running
            return
        self._timer_start = datetime.datetime.now()
        self._timer_paused_time = 0
        self._pause_start = None
        # disable start, enable pause and stop
        try:
            self.ids.start_btn.disabled = True
            self.ids.pause_btn.disabled = False
            self.ids.stop_btn.disabled = False
        except Exception:
            pass

    def pause_timer(self):
        if self._timer_start is None:
            return
        if self._pause_start is None:
            # Start pause
            self._pause_start = datetime.datetime.now()
            try:
                self.ids.pause_btn.text = 'Fortsetzen'
            except Exception:
                pass
        else:
            # Resume from pause
            pause_duration = (datetime.datetime.now() - self._pause_start).total_seconds()
            self._timer_paused_time += pause_duration
            self._pause_start = None
            try:
                self.ids.pause_btn.text = 'Pause'
            except Exception:
                pass

    def stop_timer(self):
        if self._timer_start is None:
            return
        end = datetime.datetime.now()
        
        # Calculate active time (excluding pauses)
        total_seconds = (end - self._timer_start).total_seconds()
        if self._pause_start is not None:
            # Currently paused - add current pause duration
            total_seconds -= (end - self._pause_start).total_seconds()
        total_seconds -= self._timer_paused_time
        
        raw_hours = total_seconds / 3600.0
        # round up to nearest 0.25 hours
        import math
        billed = math.ceil(raw_hours / 0.25) * 0.25
        # create entry
        path = self.get_db_path()
        db.add_entry(path, self.ids.customer_spinner.text, self.ids.activity_input.text or 'Keine Angabe', self._timer_start.isoformat(), end.isoformat(), billed)
        # reset timer and buttons
        self._timer_start = None
        self._timer_paused_time = 0
        self._pause_start = None
        try:
            self.ids.start_btn.disabled = False
            self.ids.pause_btn.disabled = True
            self.ids.pause_btn.text = 'Pause'
            self.ids.stop_btn.disabled = True
        except Exception:
            pass
        # show confirmation
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        Popup(title='Erfasst', content=Label(text=f'Erfasst: {billed:.2f} Std (aufgerundet)'), size_hint=(.7, .3)).open()
        self.refresh_entries()

    def export_pdf(self):
        # Export PDF report for selected customer using pure-Python fpdf2 (Android-friendly)
        selected_customer = self.ids.customer_spinner.text
        if not selected_customer or selected_customer == '—':
            self.show_error('Fehler', 'Bitte Kunde auswählen')
            return
        try:
            from fpdf import FPDF
        except Exception as e:
            self.show_error('PDF-Fehler', f'PDF-Bibliothek fehlt: {e}')
            return

        # Proactively check fontTools availability as fpdf2 may require it on some paths
        try:
            import fontTools  # type: ignore
        except Exception as e:
            self.show_error('PDF-Fehler', f"fontTools konnte nicht geladen werden: {e}\nBitte App neu installieren, neue APK verwenden, oder Internetverbindung beim ersten Start sicherstellen.")
            return

        try:
            out_dir = self.get_documents_dir()
            os.makedirs(out_dir, exist_ok=True)
            filename = os.path.join(out_dir, f"report_{selected_customer.replace(' ', '_')}.pdf")

            pdf = FPDF("P", "mm", "A4")
            pdf.set_title(f"Report - {selected_customer}")
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Header - use built-in font that works on Android
            pdf.set_font("Helvetica", "B", 16)
            # Encode strings to latin-1 safe characters
            safe_customer = selected_customer.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 10, f"Report fuer: {safe_customer}", ln=True)

            cust = db.get_customer(self.get_db_path(), selected_customer)
            addr = (cust[2] if cust and cust[2] else '').encode('latin-1', 'replace').decode('latin-1')
            email = (cust[3] if cust and cust[3] else '').encode('latin-1', 'replace').decode('latin-1')
            phone = (cust[4] if cust and cust[4] else '').encode('latin-1', 'replace').decode('latin-1')
            pdf.set_font("Helvetica", size=10)
            if addr:
                pdf.cell(0, 6, f"Adresse: {addr}", ln=True)
            if email:
                pdf.cell(0, 6, f"Email: {email}", ln=True)
            if phone:
                pdf.cell(0, 6, f"Telefon: {phone}", ln=True)
            pdf.ln(4)

            rows = db.get_entries(self.get_db_path(), selected_customer)
            if not rows:
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                Popup(title='Info', content=Label(text='Keine Einträge für den ausgewählten Kunden'), size_hint=(.6, .3)).open()
                return

            # Group entries by month (YYYY-MM)
            from collections import defaultdict
            months_data = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]  # e.g., "2025-01-15"
                try:
                    month_key = date_str[:7]  # "2025-01"
                except Exception:
                    month_key = "Undatiert"
                months_data[month_key].append(r)

            # Sort months chronologically
            sorted_months = sorted(months_data.keys(), reverse=True)

            grand_total = 0.0

            # Process each month
            for month_key in sorted_months:
                rows_in_month = months_data[month_key]
                month_total = 0.0

                # Month header
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 10, f"Monat: {month_key}", ln=True)

                # Table header
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(100, 7, "Tätigkeit", border=1)
                pdf.cell(40, 7, "Datum", border=1)
                pdf.cell(30, 7, "Stunden", border=1, ln=True)

                # Table rows for month
                pdf.set_font("Helvetica", size=9)
                for r in rows_in_month:
                    # Safely encode all text to latin-1
                    act = (r[2] or '')[:60].encode('latin-1', 'replace').decode('latin-1')
                    date = (r[3] or '')[:10]
                    hrs = float(r[5] or 0)
                    pdf.cell(100, 7, act, border=1)
                    pdf.cell(40, 7, date, border=1)
                    pdf.cell(30, 7, f"{hrs:.2f}", border=1, ln=True)
                    month_total += hrs

                # Month subtotal
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(140, 7, f"Monatssumme: {month_total:.2f}", border=1, ln=True)
                grand_total += month_total
                pdf.ln(4)

            # Grand total
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, f"Gesamtstunden: {grand_total:.2f}", ln=True)

            pdf.output(filename)

            # Show success popup with share button
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            content = BoxLayout(orientation='vertical', spacing=8)
            content.add_widget(Label(text=f'Report erstellt:', size_hint_y=None, height='30dp'))
            content.add_widget(Label(text=filename, size_hint_y=None, height='40dp'))
            btn_box = BoxLayout(size_hint_y=None, height='40dp', spacing=8)
            share_btn = Button(text='Teilen')
            close_btn = Button(text='OK')
            btn_box.add_widget(share_btn)
            btn_box.add_widget(close_btn)
            content.add_widget(btn_box)
            popup = Popup(title='Erfolg', content=content, size_hint=(.85, .35))

            def do_share(*a):
                self.share_pdf(filename)
                popup.dismiss()

            share_btn.bind(on_release=do_share)
            close_btn.bind(on_release=popup.dismiss)
            popup.open()

        except Exception as e:
            import traceback
            error_msg = f"Fehler beim PDF-Export:\n{str(e)}\n\n{traceback.format_exc()}"
            self.show_error('PDF-Fehler', error_msg)
            self.write_error_log(error_msg)

    def refresh_entries(self):
        # ensure UI has been built and ids available
        if 'customer_spinner' not in self.ids or 'entries_box' not in self.ids:
            return
        customer = self.ids.customer_spinner.text
        path = self.get_db_path()
        box = self.ids.entries_box
        # clear existing
        box.clear_widgets()
        if not customer or customer == '—':
            return
        rows = db.get_entries(path, customer)
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        for r in rows:
            entry_id = r[0]
            act = r[2] or ''
            date = (r[3] or '')[:10]
            hours = f"{r[5]:.2f}"
            text = f"{act} — {date} — {hours} Std"
            btn = Button(text=text, size_hint_y=None, height='40dp')
            # bind popup with delete
            btn.bind(on_release=lambda inst, eid=entry_id: self.open_entry_popup(eid))
            box.add_widget(btn)

    def open_entry_popup(self, entry_id):
        info = None
        for r in db.get_entries(self.get_db_path()):
            if r[0] == entry_id:
                info = r
                break
        if not info:
            return
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView
        
        content = BoxLayout(orientation='vertical', spacing=8)
        act = info[2] or ''
        start = info[3] or ''
        end = info[4] or ''
        hours = f"{info[5]:.2f}"
        notes = info[6] or ''
        
        content.add_widget(Label(text=f"Tätigkeit: {act}", size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f"Start: {start}", size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f"Ende: {end}", size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f"Std: {hours}", size_hint_y=None, height='30dp'))
        
        content.add_widget(Label(text="Kommentar:", size_hint_y=None, height='25dp'))
        notes_input = TextInput(text=notes, multiline=True, size_hint_y=0.4)
        content.add_widget(notes_input)
        
        btns = BoxLayout(size_hint_y=None, height='40dp', spacing=4)
        save_btn = Button(text='Speichern')
        del_btn = Button(text='Löschen')
        cancel_btn = Button(text='Abbrechen')
        btns.add_widget(save_btn)
        btns.add_widget(del_btn)
        btns.add_widget(cancel_btn)
        content.add_widget(btns)
        
        popup = Popup(title='Eintrag bearbeiten', content=content, size_hint=(.95, .7))

        def do_save(*a):
            db.update_entry(self.get_db_path(), entry_id, notes_input.text)
            popup.dismiss()
            self.refresh_entries()

        def do_delete(*a):
            db.delete_entry(self.get_db_path(), entry_id)
            popup.dismiss()
            self.refresh_entries()

        save_btn.bind(on_release=do_save)
        del_btn.bind(on_release=do_delete)
        cancel_btn.bind(on_release=lambda *a: popup.dismiss())
        popup.open()


class PoCApp(App):
    def build(self):
        # Let the Builder create the RootWidget from the KV and return that instance
        root = Builder.load_string(KV)
        return root

    def on_start(self):
        path = os.path.join(self.user_data_dir, 'stundenerfassung.db')
        db.init_db(path)
        print(f"Kivy PoC DB path: {path}")
        # Debug: print app root widget details
        try:
            root = self.root
            print("App root:", type(root), "children:", len(root.children))
        except Exception:
            pass


if __name__ == '__main__':
    PoCApp().run()
