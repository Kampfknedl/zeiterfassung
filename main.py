from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
import os
import datetime
import db

KV = '''
<RootWidget>:
    orientation: 'vertical'
    spacing: 8
    padding: 12
    canvas.before:
        Color:
            rgba: 0.97, 0.97, 0.97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Row 1: customer selection - responsive
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '150dp'
        spacing: 6
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]
        padding: 10
        Label:
            text: 'Kunde'
            size_hint_y: None
            height: '28dp'
            font_size: '14sp'
            bold: True
            color: 0.3, 0.3, 0.3, 1
            halign: 'left'
            text_size: self.size
        Spinner:
            id: customer_spinner
            text: root.customers[0] if root.customers else '—'
            values: root.customers
            size_hint_y: None
            height: '44dp'
            background_normal: ''
            background_color: 0.95, 0.95, 0.95, 1
            color: 0.2, 0.2, 0.2, 1
            font_size: '15sp'
        BoxLayout:
            size_hint_y: None
            height: '44dp'
            spacing: 8
            Button:
                text: '+ Kunde'
                on_release: root.add_customer()
                background_normal: ''
                background_color: 0.4, 0.6, 0.8, 1
                color: 1, 1, 1, 1
                font_size: '14sp'
            Button:
                text: 'Kunden verwalten'
                on_release: root.open_customer_management()
                background_normal: ''
                background_color: 0.6, 0.6, 0.6, 1
                color: 1, 1, 1, 1
                font_size: '14sp'

    # Row 2: activity, date, hours - responsive
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '220dp'
        spacing: 6
        padding: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]
        Label:
            text: 'Tätigkeit'
            size_hint_y: None
            height: '28dp'
            font_size: '14sp'
            bold: True
            color: 0.2, 0.2, 0.2, 1
            halign: 'left'
            text_size: self.size
        TextInput:
            id: activity_input
            multiline: False
            size_hint_y: None
            height: '44dp'
            font_size: '15sp'
            padding: [12, 10]
            background_normal: ''
            background_color: 0.95, 0.95, 0.95, 1
        BoxLayout:
            size_hint_y: None
            height: '44dp'
            spacing: 8
            Label:
                text: 'Datum'
                size_hint_x: None
                width: '70dp'
                font_size: '14sp'
                bold: True
                color: 0.2, 0.2, 0.2, 1
            TextInput:
                id: date_input
                text: ''
                hint_text: 'dd.mm.yyyy'
                multiline: False
                font_size: '15sp'
                padding: [12, 10]
                background_normal: ''
                background_color: 0.95, 0.95, 0.95, 1
        BoxLayout:
            size_hint_y: None
            height: '44dp'
            spacing: 8
            Label:
                text: 'Std'
                size_hint_x: None
                width: '50dp'
                font_size: '14sp'
                bold: True
                color: 0.2, 0.2, 0.2, 1
            TextInput:
                id: hours_input
                text: '1.0'
                input_filter: 'float'
                multiline: False
                font_size: '15sp'
                padding: [12, 10]
                background_normal: ''
                background_color: 0.95, 0.95, 0.95, 1
            Button:
                text: '+ Eintrag'
                on_release: root.add_entry(activity_input.text, hours_input.text)
                background_normal: ''
                background_color: 0.4, 0.7, 0.5, 1
                color: 1, 1, 1, 1
                font_size: '15sp'
                bold: True

    # Row 3: CSV Export & Timer
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '130dp'
        spacing: 6
        padding: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]
        Button:
            text: 'PDF Export erstellen'
            size_hint_y: None
            height: '50dp'
            on_release: root.export_pdf_with_dialog()
            background_normal: ''
            background_color: 0.7, 0.5, 0.5, 1
            color: 1, 1, 1, 1
            font_size: '16sp'
            bold: True
        BoxLayout:
            size_hint_y: None
            height: '48dp'
            spacing: 8
            Button:
                id: start_btn
                text: 'Start'
                on_release: root.start_timer()
                background_normal: ''
                background_color: 0.4, 0.7, 0.5, 1
                color: 1, 1, 1, 1
                font_size: '14sp'
                bold: True
            Button:
                id: pause_btn
                text: 'Pause'
                disabled: True
                on_release: root.pause_timer()
                background_normal: ''
                background_color: 0.8, 0.7, 0.4, 1
                color: 1, 1, 1, 1
                font_size: '14sp'
                bold: True
            Button:
                id: stop_btn
                text: 'Stop'
                on_release: root.stop_timer()
                background_normal: ''
                background_color: 0.8, 0.5, 0.5, 1
                color: 1, 1, 1, 1
                font_size: '14sp'
                bold: True

    BoxLayout:
        orientation: 'vertical'
        spacing: 6
        padding: [10, 6, 10, 6]
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10]
        Label:
            text: 'Letzte Einträge'
            size_hint_y: None
            height: '32dp'
            font_size: '14sp'
            bold: True
            color: 0.2, 0.2, 0.2, 1
            halign: 'left'
            text_size: self.size
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: entries_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 6

    Label:
        text: 'made by Benedikt Bernhart'
        size_hint_y: None
        height: '24dp'
        font_size: '11sp'
        color: 0.6, 0.6, 0.6, 1
'''


class RootWidget(BoxLayout):
    customers = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer_start = None
        self._timer_paused_time = 0  # accumulated paused seconds
        self._pause_start = None      # when pause was pressed
        self._pdf_export_path = None  # User-selected PDF export directory

    def on_kv_post(self, base_widget):
        # Ensure DB initialized before attempting queries
        try:
            db.init_db(self.get_db_path())
        except Exception as e:
            print(f"DB init error: {e}")
        
        try:
            self.load_customers()
        except Exception as e:
            print(f"Load customers error: {e}")
            self.customers = ['—']  # Fallback
        
        try:
            self.refresh_entries()
        except Exception as e:
            print(f"Refresh entries error: {e}")
        
        # Debug: print ids and children for visibility troubleshooting
        try:
            print("RootWidget ids:", list(self.ids.keys()))
            print("RootWidget children count:", len(self.children))
            print("Customers:", self.customers)
        except Exception as e:
            print(f"Debug print error: {e}")
        
        # set default date for manual entries
        try:
            self.ids.date_input.text = datetime.date.today().strftime("%d.%m.%Y")
        except Exception as e:
            print(f"Date input error: {e}")
        
        # setup activity suggestions
        try:
            self._activity_dropdown = None
            self.ids.activity_input.bind(text=self.on_activity_text)
            self.ids.activity_input.bind(focus=self.on_activity_focus)
        except Exception as e:
            print(f"Activity input binding error: {e}")
        
        # bind customer spinner change to refresh entries
        try:
            self.ids.customer_spinner.bind(text=self.on_customer_changed)
        except Exception as e:
            print(f"Customer spinner binding error: {e}")

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
        # Prefer app-specific external Documents directory (no runtime permission needed)
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Environment = autoclass('android.os.Environment')

            context = PythonActivity.mActivity
            # Use app-specific external files dir: .../Android/data/<pkg>/files/Documents
            ext_dir = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS)
            if ext_dir is not None:
                docs_path = os.path.join(ext_dir.getAbsolutePath(), 'Zeiterfassung')
                os.makedirs(docs_path, exist_ok=True)
                return docs_path
        except Exception as e:
            print(f"Android external files dir failed: {e}")

        try:
            # Fallback: Desktop Documents folder (desktop usage)
            docs_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Zeiterfassung')
            os.makedirs(docs_path, exist_ok=True)
            return docs_path
        except Exception:
            # Last resort: app internal data directory
            return self.get_db_dir()

    def get_fileprovider_authority(self):
        """Return FileProvider authority matching the current package name."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            pkg = PythonActivity.mActivity.getPackageName()
            return f"{pkg}.fileprovider"
        except Exception:
            # Fallback to legacy hardcoded value to avoid crashing
            return "org.tkideneb.zeiterfassung.fileprovider"

    def save_pdf_to_public_documents(self, temp_path, base_filename):
        """Deprecated: MediaStore path handling caused compatibility issues."""
        return temp_path, None

    def show_file_viewer(self, filepath_display, customer_name, mime_type='text/csv', auto_share=False):
        # Show creation success message with sharing option
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=8, padding=10)
        content.add_widget(Label(
            text='CSV erstellt!',
            size_hint_y=None,
            height='40dp',
            font_size='16sp'
        ))
        content.add_widget(Label(
            text=f'Kunde: {customer_name}',
            size_hint_y=None,
            height='30dp'
        ))
        content.add_widget(Label(
            text='CSV wurde erfolgreich gespeichert.',
            size_hint_y=None,
            height='30dp'
        ))

        btn_box = BoxLayout(size_hint_y=None, height='50dp', spacing=8)
        share_btn = Button(text='Teilen')
        open_btn = Button(text='Oeffnen')
        close_btn = Button(text='Schliessen')
        btn_box.add_widget(share_btn)
        btn_box.add_widget(open_btn)
        btn_box.add_widget(close_btn)
        content.add_widget(btn_box)

        popup = Popup(title='Report erstellt', content=content, size_hint=(.9, .5))

        def do_share(*_):
            success = self.share_file_fileprovider(filepath_display, mime_type=mime_type)
            if success:
                popup.dismiss()
            else:
                self.show_error('Fehler', 'Datei konnte nicht geteilt werden')

        def do_open(*_):
            self.open_file(filepath_display, mime_type=mime_type)
            popup.dismiss()

        share_btn.bind(on_release=do_share)
        open_btn.bind(on_release=do_open)
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

        if auto_share:
            try:
                do_share()
            except Exception:
                pass

    def open_file(self, filepath, mime_type='text/csv'):
        """Open a file with default viewer (for sharing)."""
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            java_file = File(filepath)
            
            # Try FileProvider first (Android 7+)
            try:
                    FileProvider = autoclass('androidx.core.content.FileProvider')
                    authority = self.get_fileprovider_authority()
                    uri = FileProvider.getUriForFile(PythonActivity.mActivity, authority, java_file)
            except Exception:
                # Fallback to file:// URI for older devices
                uri = Uri.fromFile(java_file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, mime_type)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

            PythonActivity.mActivity.startActivity(intent)
        except Exception as e:
            import traceback
            error_msg = f"Fehler beim Öffnen: {str(e)}\n\n{traceback.format_exc()}"
            self.show_error('Fehler', error_msg)
            self.write_error_log(error_msg)

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

    def share_file_fileprovider(self, filepath, mime_type='text/csv', is_uri=False):
        """Share a file using Android FileProvider (Android 7+) with fallback."""
        try:
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            String = autoclass('java.lang.String')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            context = PythonActivity.mActivity
            
            if is_uri or (filepath and filepath.startswith('content://')):
                # Already a content URI
                uri = Uri.parse(filepath)
            else:
                # Regular file path - convert to URI
                java_file = File(filepath)
                
                # Try FileProvider first (Android 7+, more secure)
                try:
                    FileProvider = autoclass('androidx.core.content.FileProvider')
                    authority = self.get_fileprovider_authority()
                    uri = FileProvider.getUriForFile(context, authority, java_file)
                except Exception as fp_error:
                    print(f"FileProvider for share failed: {fp_error}")
                    # Fallback to file:// URI for Android 6 and below
                    uri = Uri.fromFile(java_file)

            # Create SEND intent
            intent = Intent(Intent.ACTION_SEND)
            intent.setType(mime_type)
            intent.putExtra(Intent.EXTRA_STREAM, uri)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

            # Create chooser
            file_type = 'PDF' if mime_type == 'application/pdf' else 'Report'
            title = cast('java.lang.CharSequence', String(f'{file_type} teilen via'))
            chooser = Intent.createChooser(intent, title)
            chooser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(chooser)
            
            return True
        except Exception as e:
            import traceback
            print(f"Share failed: {e}")
            print(traceback.format_exc())
            return False

    def share_pdf(self, uri_string):
        # Legacy: still route to generic share for compatibility
        try:
            return self.share_file_fileprovider(uri_string, mime_type='text/csv')
        except Exception as e:
            import traceback
            error_msg = f"Fehler beim Teilen: {str(e)}\n\n{traceback.format_exc()}"
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
            self.show_error('Datum ungültig', 'Bitte Datum im Format dd.mm.yyyy eingeben.')
            return

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

    def export_csv(self, auto_share=False):
        selected_customer = self.ids.customer_spinner.text
        if not selected_customer or selected_customer == '—':
            self.show_error('Fehler', 'Bitte Kunde auswählen')
            return

        rows = db.get_entries(self.get_db_path(), selected_customer)
        if not rows:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title='Info', content=Label(text='Keine Einträge für den ausgewählten Kunden'), size_hint=(.6, .3)).open()
            return

        try:
            import csv
            from collections import defaultdict

            out_dir = self.get_documents_dir()
            os.makedirs(out_dir, exist_ok=True)
            base_name = f"report_{selected_customer.replace(' ', '_')}.csv"
            temp_path = os.path.join(out_dir, base_name)

            months_data = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]
                month_key = date_str[:7] if date_str else "Undatiert"
                months_data[month_key].append(r)

            sorted_months = sorted(months_data.keys(), reverse=True)
            grand_total = 0.0

            with open(temp_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Kunde', selected_customer])
                writer.writerow(['Erstellt am', datetime.datetime.now().isoformat(timespec='seconds')])
                cust = db.get_customer(self.get_db_path(), selected_customer)
                if cust and cust[2]:
                    writer.writerow(['Adresse', cust[2]])
                if cust and cust[3]:
                    writer.writerow(['Email', cust[3]])
                if cust and cust[4]:
                    writer.writerow(['Telefon', cust[4]])
                writer.writerow([])
                writer.writerow(['Monat', 'Datum', 'Tätigkeit', 'Stunden'])

                for month_key in sorted_months:
                    rows_in_month = months_data[month_key]
                    month_total = 0.0

                    for r in rows_in_month:
                        date = (r[3] or '')[:10]
                        act = r[2] or ''
                        hrs = float(r[5] or 0)
                        writer.writerow([month_key, date, act, f"{hrs:.2f}"])
                        month_total += hrs

                    writer.writerow([month_key, '', 'Monatssumme', f"{month_total:.2f}"])
                    writer.writerow([])
                    grand_total += month_total

                writer.writerow(['', '', 'Gesamtstunden', f"{grand_total:.2f}"])

            self.show_file_viewer(temp_path, selected_customer, mime_type='text/csv', auto_share=auto_share)

        except Exception as e:
            import traceback
            error_msg = f"Fehler beim CSV-Export:\n{str(e)}\n\n{traceback.format_exc()}"
            self.show_error('CSV-Fehler', error_msg)
            self.write_error_log(error_msg)

    def get_saved_pdf_path(self):
        """Retrieve saved PDF export path from settings file"""
        try:
            settings_file = os.path.join(self.get_db_dir(), 'pdf_settings.txt')
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    path = f.read().strip()
                    if path and os.path.exists(path):
                        return path
        except Exception:
            pass
        return None

    def save_pdf_path(self, path):
        """Save PDF export path to settings file"""
        try:
            settings_file = os.path.join(self.get_db_dir(), 'pdf_settings.txt')
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(path)
            self._pdf_export_path = path
        except Exception as e:
            print(f"Error saving PDF path: {e}")

    def choose_pdf_directory(self, callback):
        """Open Samsung file picker to choose PDF export directory, prioritizing OneDrive"""
        try:
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            DocumentsContract = autoclass('android.provider.DocumentsContract')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            # Create OPEN_DOCUMENT_TREE intent for directory selection
            intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
            
            # Try to set OneDrive as initial location (Samsung Devices)
            try:
                # OneDrive URI for Samsung devices
                onedrive_uri = Uri.parse("content://com.microsoft.skydrive.content.StorageAccessProvider/")
                intent.putExtra("android.provider.extra.INITIAL_URI", onedrive_uri)
            except Exception:
                pass  # If OneDrive not available, use default picker
            
            # Set flags for persistent access
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | 
                          Intent.FLAG_GRANT_WRITE_URI_PERMISSION |
                          Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION |
                          Intent.FLAG_GRANT_PREFIX_URI_PERMISSION)
            
            # Store callback for result handling
            self._directory_callback = callback
            
            # Start activity for result
            PythonActivity.mActivity.startActivityForResult(intent, 42)
            
            # Note: Activity result handling done via activity lifecycle, not binding here
            
        except Exception as e:
            import traceback
            error_msg = f"Fehler beim Öffnen des Dateiauswahldialogs:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            # Fallback to default directory
            try:
                callback(self.get_documents_dir())
            except Exception:
                pass

    def _on_directory_result(self, request_code, result_code, intent):
        """Handle directory selection result"""
        try:
            if request_code == 42 and result_code == -1:  # RESULT_OK = -1
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                DocumentsContract = autoclass('android.provider.DocumentsContract')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                if intent is not None:
                    tree_uri = intent.getData()
                    
                    # Take persistable URI permission
                    content_resolver = PythonActivity.mActivity.getContentResolver()
                    content_resolver.takePersistableUriPermission(
                        tree_uri,
                        Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                    )
                    
                    # Convert URI to usable path
                    uri_string = tree_uri.toString()
                    
                    # Save this path for future use
                    self.save_pdf_path(uri_string)
                    
                    # Call the callback
                    if hasattr(self, '_directory_callback'):
                        self._directory_callback(uri_string)
                        
        except Exception as e:
            import traceback
            print(f"Directory result error: {str(e)}\n{traceback.format_exc()}")
            # Fallback to default
            if hasattr(self, '_directory_callback'):
                self._directory_callback(self.get_documents_dir())

    def export_pdf_with_dialog(self):
        """Export CSV with file save dialog (user can choose OneDrive, etc.)"""
        try:
            # Desktop: Use tkinter file dialog
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            selected_customer = self.ids.customer_spinner.text
            default_filename = f"Zeiterfassung_{selected_customer.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            filepath = filedialog.asksaveasfilename(
                title="CSV speichern",
                defaultextension=".csv",
                filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")],
                initialfile=default_filename
            )
            
            root.destroy()
            
            if filepath:
                # Extract directory from full filepath
                export_dir = os.path.dirname(filepath)
                filename = os.path.basename(filepath)
                self.export_csv_to_path(export_dir, filename)
            else:
                print("CSV Export abgebrochen")
                
        except ImportError:
            # Android: Use Android file picker (SAF)
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                selected_customer = self.ids.customer_spinner.text
                default_filename = f"Zeiterfassung_{selected_customer.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
                intent.addCategory(Intent.CATEGORY_OPENABLE)
                intent.setType("text/csv")
                intent.putExtra(Intent.EXTRA_TITLE, default_filename)
                
                # Store customer for later use in result handler
                self._export_customer = selected_customer
                
                PythonActivity.mActivity.startActivityForResult(intent, 43)
                
            except Exception as e:
                import traceback
                print(f"Android file dialog error: {str(e)}\n{traceback.format_exc()}")
                # Fallback to default path
                default_path = self.get_documents_dir()
                self.export_csv_to_path(default_path, None)

    def write_pdf_to_uri(self, uri_string, pdf_bytes, filename):
        """Write PDF bytes to Android content URI (for OneDrive, etc.)"""
        try:
            from jnius import autoclass
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            DocumentFile = autoclass('androidx.documentfile.provider.DocumentFile')
            
            tree_uri = Uri.parse(uri_string)
            context = PythonActivity.mActivity
            content_resolver = context.getContentResolver()
            
            # Get DocumentFile from tree URI
            doc_tree = DocumentFile.fromTreeUri(context, tree_uri)
            
            if doc_tree and doc_tree.canWrite():
                # Create new PDF file in the directory
                new_file = doc_tree.createFile('application/pdf', filename)
                
                if new_file:
                    # Write PDF bytes to the file
                    output_stream = content_resolver.openOutputStream(new_file.getUri())
                    
                    # Convert Python bytes to Java byte array
                    if isinstance(pdf_bytes, bytes):
                        output_stream.write(pdf_bytes)
                    else:
                        # If it's a string, encode it
                        output_stream.write(pdf_bytes.encode('latin-1'))
                    
                    output_stream.flush()
                    output_stream.close()
                    
                    # Return the document URI as string
                    return new_file.getUri().toString()
                else:
                    raise Exception("Konnte Datei nicht erstellen")
            else:
                raise Exception("Kein Schreibzugriff auf ausgewählten Ordner")
            
        except Exception as e:
            import traceback
            print(f"Write to URI error: {str(e)}\n{traceback.format_exc()}")
            raise
        
        return None

    def export_csv_to_path(self, export_path, filename=None):
        """Export customer entries as CSV (simple, reliable format)"""
        selected_customer = self.ids.customer_spinner.text
        if not selected_customer or selected_customer == '—':
            self.show_error('Fehler', 'Bitte Kunde auswählen')
            return

        rows = db.get_entries(self.get_db_path(), selected_customer)
        if not rows:
            self.show_error('Info', 'Keine Einträge vorhanden')
            return

        try:
            import csv
            from collections import defaultdict

            # Use local directory
            if not os.path.exists(export_path):
                os.makedirs(export_path, exist_ok=True)
            
            if filename is None:
                filename = f"Zeiterfassung_{selected_customer.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            csv_path = os.path.join(export_path, filename)

            # Group entries by month
            months_data = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]
                month_key = date_str[:7] if date_str else "Undatiert"
                months_data[month_key].append(r)

            sorted_months = sorted(months_data.keys(), reverse=True)
            grand_total = 0.0

            # Write CSV file
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                
                # Header
                writer.writerow(['Zeiterfassung', selected_customer])
                writer.writerow([])
                writer.writerow([f'Erstellt am: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'])
                
                cust = db.get_customer(self.get_db_path(), selected_customer)
                if cust and cust[2]:
                    writer.writerow([f'Adresse: {cust[2]}'])
                if cust and cust[3]:
                    writer.writerow([f'Email: {cust[3]}'])
                if cust and cust[4]:
                    writer.writerow([f'Telefon: {cust[4]}'])
                
                writer.writerow([])
                writer.writerow(['Datum', 'Taetigkeit', 'Stunden'])

                # Monthly entries
                for month_key in sorted_months:
                    rows_in_month = months_data[month_key]
                    month_total = 0.0

                    writer.writerow([f'Monat: {month_key}'])
                    for r in rows_in_month:
                        date = (r[3] or '')[:10]
                        act = r[2] or ''
                        hrs = float(r[5] or 0)
                        writer.writerow([date, act, f'{hrs:.2f}'])
                        month_total += hrs

                    writer.writerow(['', f'Monatssumme {month_key}:', f'{month_total:.2f}'])
                    writer.writerow([])
                    grand_total += month_total

                # Grand total
                writer.writerow([])
                writer.writerow(['Gesamtstunden', f'{grand_total:.2f}'])

            # Automatische PDF-Konvertierung
            pdf_path = self.convert_csv_to_pdf(csv_path, selected_customer, rows, months_data, sorted_months, grand_total)
            
            self.show_success_and_open_pdf(pdf_path if pdf_path else csv_path, selected_customer, is_uri=False)

        except Exception as e:
            import traceback
            error_msg = f"Fehler beim Export:\n{str(e)}\n\n{traceback.format_exc()}"
            self.show_error('Export-Fehler', error_msg)
            self.write_error_log(error_msg)

    def convert_csv_to_pdf(self, csv_path, customer_name, rows, months_data, sorted_months, grand_total):
        """Convert CSV to PDF using reportlab"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
            
            pdf_path = csv_path.replace('.csv', '.pdf')
            
            # Create PDF
            doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                                   rightMargin=2*cm, leftMargin=2*cm,
                                   topMargin=2*cm, bottomMargin=2*cm)
            
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#4a4a4a'),
                spaceAfter=12,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#5a5a5a'),
                spaceAfter=10,
                spaceBefore=10
            )
            
            # Title
            story.append(Paragraph(f"Zeiterfassung - {customer_name}", title_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Customer info
            cust = db.get_customer(self.get_db_path(), customer_name)
            info_data = [
                ['Erstellt am:', datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]
            ]
            if cust and cust[2]:
                info_data.append(['Adresse:', cust[2]])
            if cust and cust[3]:
                info_data.append(['Email:', cust[3]])
            if cust and cust[4]:
                info_data.append(['Telefon:', cust[4]])
            
            info_table = Table(info_data, colWidths=[4*cm, 13*cm])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#5a5a5a')),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.8*cm))
            
            # Monthly entries
            for month_key in sorted_months:
                story.append(Paragraph(f"Monat: {month_key}", heading_style))
                
                rows_in_month = months_data[month_key]
                month_total = 0.0
                
                table_data = [['Datum', 'Tätigkeit', 'Stunden']]
                
                for r in rows_in_month:
                    date = (r[3] or '')[:10]
                    act = r[2] or ''
                    hrs = float(r[5] or 0)
                    table_data.append([date, act, f'{hrs:.2f}'])
                    month_total += hrs
                
                table_data.append(['', 'Monatssumme:', f'{month_total:.2f}'])
                
                t = Table(table_data, colWidths=[3.5*cm, 10*cm, 3.5*cm])
                t.setStyle(TableStyle([
                    # Header row
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7a8a9a')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    
                    # Data rows
                    ('FONT', (0, 1), (-1, -2), 'Helvetica', 10),
                    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                    ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')]),
                    
                    # Total row
                    ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 11),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e0e0e0')),
                    ('TOPPADDING', (0, -1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
                ]))
                
                story.append(t)
                story.append(Spacer(1, 0.5*cm))
            
            # Grand total
            grand_total_data = [['Gesamtstunden:', f'{grand_total:.2f}']]
            grand_table = Table(grand_total_data, colWidths=[13.5*cm, 3.5*cm])
            grand_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 14),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#7a8a9a')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#5a6a7a')),
            ]))
            story.append(Spacer(1, 0.5*cm))
            story.append(grand_table)
            
            # Build PDF
            doc.build(story)
            
            print(f"PDF erfolgreich erstellt: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            import traceback
            print(f"PDF Konvertierung fehlgeschlagen: {str(e)}\n{traceback.format_exc()}")
            return None

    def show_success_and_open_pdf(self, filepath, customer_name, is_uri=False):
        """Show success message and automatically open PDF"""
        try:
            # Automatically open the PDF
            self.open_pdf_file(filepath, is_uri=is_uri)
            
            # Show success toast/notification
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            
            # Check if it's PDF or CSV
            file_type = 'PDF' if filepath.endswith('.pdf') else 'CSV'
            
            content = BoxLayout(orientation='vertical', spacing=10, padding=15)
            content.add_widget(Label(
                text=f'{file_type} erfolgreich erstellt!',
                size_hint_y=None,
                height='50dp',
                font_size='18sp',
                bold=True,
                color=(0.4, 0.7, 0.5, 1)
            ))
            content.add_widget(Label(
                text=f'Kunde: {customer_name}',
                size_hint_y=None,
                height='30dp',
                font_size='14sp'
            ))
            content.add_widget(Label(
                text=f'{file_type} wird jetzt geöffnet...',
                size_hint_y=None,
                height='30dp',
                font_size='14sp',
                color=(0.5, 0.5, 0.5, 1)
            ))
            
            btn = Button(
                text='OK',
                size_hint_y=None,
                height='50dp',
                background_normal='',
                background_color=(0.4, 0.6, 0.8, 1),
                color=(1, 1, 1, 1),
                font_size='16sp',
                bold=True
            )
            content.add_widget(btn)
            
            popup = Popup(
                title=f'{file_type} Export',
                content=content,
                size_hint=(.85, .5),
                auto_dismiss=True
            )
            btn.bind(on_release=popup.dismiss)
            popup.open()
            
        except Exception as e:
            import traceback
            print(f"Show success error: {str(e)}\n{traceback.format_exc()}")

    def open_pdf_file(self, filepath, is_uri=False):
        """Open report CSV with default viewer using Samsung/Android intent"""
        try:
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            String = autoclass('java.lang.String')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            if is_uri:
                # Already a content URI
                uri = Uri.parse(filepath)
            else:
                # Convert file path to URI
                java_file = File(filepath)
                
                # Try FileProvider first (Android 7+)
                try:
                    FileProvider = autoclass('androidx.core.content.FileProvider')
                    authority = self.get_fileprovider_authority()
                    uri = FileProvider.getUriForFile(PythonActivity.mActivity, authority, java_file)
                except Exception as fp_error:
                    print(f"FileProvider failed: {fp_error}")
                    # Fallback to file:// URI for older devices
                    uri = Uri.fromFile(java_file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, 'text/csv')
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)

            # Create chooser for better UX
            try:
                title = cast('java.lang.CharSequence', String('CSV öffnen mit'))
                chooser = Intent.createChooser(intent, title)
                PythonActivity.mActivity.startActivity(chooser)
            except Exception:
                # Fallback: direct intent
                PythonActivity.mActivity.startActivity(intent)
            
        except Exception as e:
            import traceback
            error_msg = f"Fehler beim Öffnen der CSV:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            # Don't show error popup here - just log it
            self.write_error_log(error_msg)

    def export_pdf(self, auto_share=False):
        """Legacy PDF export function - redirects to new dialog-based export"""
        self.export_pdf_with_dialog()

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
        # Load the KV - the RootWidget class is defined above
        root = Builder.load_string(KV)
        
        # If Builder returns None, it means the KV didn't define a root widget properly
        # This should not happen with our <RootWidget>: rule, but just in case...
        if root is None:
            print("[ERROR] Builder.load_string returned None!")
            print("[ERROR] KV rule '<RootWidget>:' may not have instantiated properly")
            # Return the RootWidget directly
            root = RootWidget()
        
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
