"""
Zeiterfassung App - Cross-platform (iOS & Android)
Redesigned with KivyMD for native Material Design look
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem, OneLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import os
import sys
import datetime
import platform as plt
import db

# Detect platform
IS_ANDROID = plt.system() == 'Linux' and 'ANDROID_ARGUMENT' in os.environ
IS_IOS = plt.system() == 'Darwin' and sys.platform == 'ios'
IS_MOBILE = IS_ANDROID or IS_IOS


class MainScreen(MDScreen):
    """Main screen with time tracking functionality"""
    
    customers = ListProperty([])
    selected_customer = StringProperty('—')
    timer_running = False
    timer_paused = False
    elapsed_seconds = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer_start = None
        self._timer_paused_time = 0
        self._pause_start = None
        self._clock_event = None
        self.dialog = None
        # Default Export-Verzeichnis (kann vom Nutzer überschrieben werden)
        try:
            self.export_dir = self.get_documents_dir()
        except Exception:
            self.export_dir = os.path.dirname(self.get_db_path())
        
    def on_kv_post(self, base_widget):
        """Initialize after KV is loaded"""
        db.init_db(self.get_db_path())
        self.load_customers()
        self.refresh_entries()
        
    def get_db_path(self):
        """Get platform-specific database path"""
        app_dir = MDApp.get_running_app().user_data_dir
        os.makedirs(app_dir, exist_ok=True)
        return os.path.join(app_dir, 'stundenerfassung.db')
    
    def get_documents_dir(self):
        """Get platform-specific documents directory"""
        if IS_ANDROID:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Environment = autoclass('android.os.Environment')
                context = PythonActivity.mActivity
                ext_dir = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS)
                if ext_dir:
                    docs_path = os.path.join(ext_dir.getAbsolutePath(), 'Zeiterfassung')
                    os.makedirs(docs_path, exist_ok=True)
                    return docs_path
            except Exception as e:
                print(f"Android docs dir failed: {e}")
        
        # Fallback for desktop/iOS
        try:
            docs_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Zeiterfassung')
            os.makedirs(docs_path, exist_ok=True)
            return docs_path
        except Exception:
            return os.path.dirname(self.get_db_path())

    def choose_export_dir(self):
        """Let user choose an export directory (Desktop/Android, iOS optional)."""
        try:
            from plyer import filechooser
            # choose_dir returns a list of selected directories
            selection = filechooser.choose_dir()
            if selection and isinstance(selection, (list, tuple)):
                chosen = selection[0]
                if chosen:
                    os.makedirs(chosen, exist_ok=True)
                    self.export_dir = chosen
                    self.show_snackbar(f"Speicherort gesetzt: {chosen}")
                    return True
        except Exception as e:
            print(f"choose_export_dir error: {e}")
        self.show_snackbar("Kein Speicherort gewählt")
        return False
    
    def show_snackbar(self, text):
        """Show a snackbar message"""
        Snackbar(text=text, duration=2).open()
    
    def load_customers(self):
        """Load customers from database"""
        self.customers = ['—'] + db.get_customers(self.get_db_path())
        if not self.selected_customer or self.selected_customer not in self.customers:
            self.selected_customer = '—'
    
    def show_customer_menu(self, caller):
        """Show customer selection menu"""
        menu_items = [
            {
                "text": customer,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=customer: self.select_customer(x),
            } for customer in self.customers
        ]
        self.customer_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.customer_menu.open()
    
    def select_customer(self, customer):
        """Select a customer"""
        self.selected_customer = customer
        self.ids.customer_btn.text = customer
        self.customer_menu.dismiss()
        self.refresh_entries()
    
    def show_add_customer_dialog(self):
        """Show dialog to add new customer"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        name_field = MDTextField(hint_text="Name", required=True)
        address_field = MDTextField(hint_text="Adresse")
        email_field = MDTextField(hint_text="Email")
        phone_field = MDTextField(hint_text="Telefon")
        
        content.add_widget(name_field)
        content.add_widget(address_field)
        content.add_widget(email_field)
        content.add_widget(phone_field)
        
        def save_customer(*args):
            name = name_field.text.strip()
            if name:
                db.add_customer(self.get_db_path(), name)
                db.update_customer(self.get_db_path(), name, 
                                 address_field.text.strip(),
                                 email_field.text.strip(), 
                                 phone_field.text.strip())
                self.load_customers()
                self.show_snackbar(f"Kunde '{name}' hinzugefügt")
                self.dialog.dismiss()
            else:
                self.show_snackbar("Name erforderlich")
        
        self.dialog = MDDialog(
            title="Neuer Kunde",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="ABBRECHEN", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SPEICHERN", on_release=save_customer),
            ],
        )
        self.dialog.open()
    
    def show_customer_management(self):
        """Show customer management screen"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(5))
        
        scroll = MDScrollView()
        customer_list = MDList()
        
        for customer in [c for c in self.customers if c != '—']:
            item = ThreeLineListItem(
                text=customer,
                secondary_text="Bearbeiten oder löschen",
                on_release=lambda x, c=customer: self.edit_customer(c)
            )
            customer_list.add_widget(item)
        
        scroll.add_widget(customer_list)
        content.add_widget(scroll)
        
        self.dialog = MDDialog(
            title="Kunden verwalten",
            type="custom",
            content_cls=content,
            size_hint=(0.9, 0.9),
            buttons=[
                MDFlatButton(text="SCHLIEßEN", on_release=lambda x: self.dialog.dismiss()),
            ],
        )
        self.dialog.open()
    
    def edit_customer(self, customer_name):
        """Edit customer details"""
        info = db.get_customer(self.get_db_path(), customer_name)
        if not info:
            return
        
        _, name, address, email, phone = info
        
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        name_field = MDTextField(text=name, hint_text="Name", required=True)
        address_field = MDTextField(text=address or '', hint_text="Adresse")
        email_field = MDTextField(text=email or '', hint_text="Email")
        phone_field = MDTextField(text=phone or '', hint_text="Telefon")
        
        content.add_widget(name_field)
        content.add_widget(address_field)
        content.add_widget(email_field)
        content.add_widget(phone_field)
        
        def save_changes(*args):
            new_name = name_field.text.strip()
            if new_name:
                db.update_customer_full(self.get_db_path(), name, 
                                       new_name=new_name,
                                       address=address_field.text.strip(),
                                       email=email_field.text.strip(),
                                       phone=phone_field.text.strip())
                self.load_customers()
                self.show_snackbar("Kunde aktualisiert")
                self.dialog.dismiss()
                self.show_customer_management()
        
        def delete_customer(*args):
            db.delete_customer(self.get_db_path(), name)
            self.load_customers()
            self.show_snackbar(f"Kunde '{name}' gelöscht")
            self.dialog.dismiss()
            self.show_customer_management()
        
        self.dialog = MDDialog(
            title=f"Bearbeiten: {name}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="LÖSCHEN", on_release=delete_customer),
                MDFlatButton(text="ABBRECHEN", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SPEICHERN", on_release=save_changes),
            ],
        )
        self.dialog.open()
    
    def add_manual_entry(self):
        """Add manual time entry"""
        customer = self.selected_customer
        activity = self.ids.activity_input.text.strip() or 'Keine Angabe'
        
        try:
            hours = float(self.ids.hours_input.text or '1.0')
        except:
            hours = 1.0
        
        date_text = self.ids.date_input.text.strip()
        try:
            if date_text:
                dt = datetime.datetime.strptime(date_text, "%d.%m.%Y")
                start = dt.date().isoformat()
                end = start
            else:
                now = datetime.datetime.now().isoformat()
                start = now
                end = now
        except:
            now = datetime.datetime.now().isoformat()
            start = now
            end = now
        
        db.add_entry(self.get_db_path(), customer, activity, start, end, hours)
        self.show_snackbar(f"{hours:.2f} Std hinzugefügt")
        self.refresh_entries()
        
        # Clear inputs
        self.ids.activity_input.text = ''
        self.ids.hours_input.text = '1.0'
    
    def start_timer(self):
        """Start timer"""
        if self.selected_customer == '—':
            self.show_snackbar("Bitte Kunde auswählen")
            return
        
        self._timer_start = datetime.datetime.now()
        self._timer_paused_time = 0
        self._pause_start = None
        self.timer_running = True
        self.timer_paused = False
        self.elapsed_seconds = 0
        
        # Update UI
        self.ids.start_btn.disabled = True
        self.ids.pause_btn.disabled = False
        self.ids.stop_btn.disabled = False
        
        # Start clock
        self._clock_event = Clock.schedule_interval(self.update_timer, 1)
        self.show_snackbar("Timer gestartet")
    
    def update_timer(self, dt):
        """Update timer display"""
        if self._timer_start and not self._pause_start:
            total_seconds = (datetime.datetime.now() - self._timer_start).total_seconds()
            total_seconds -= self._timer_paused_time
            self.elapsed_seconds = int(total_seconds)
            
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            self.ids.timer_label.text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def pause_timer(self):
        """Pause/resume timer"""
        if not self.timer_running:
            return
        
        if not self._pause_start:
            # Pause
            self._pause_start = datetime.datetime.now()
            self.timer_paused = True
            self.ids.pause_btn.text = "FORTSETZEN"
            self.show_snackbar("Timer pausiert")
        else:
            # Resume
            pause_duration = (datetime.datetime.now() - self._pause_start).total_seconds()
            self._timer_paused_time += pause_duration
            self._pause_start = None
            self.timer_paused = False
            self.ids.pause_btn.text = "PAUSE"
            self.show_snackbar("Timer fortgesetzt")
    
    def stop_timer(self):
        """Stop timer and create entry"""
        if not self.timer_running:
            return
        
        end = datetime.datetime.now()
        
        # Calculate active time
        total_seconds = (end - self._timer_start).total_seconds()
        if self._pause_start:
            total_seconds -= (end - self._pause_start).total_seconds()
        total_seconds -= self._timer_paused_time
        
        raw_hours = total_seconds / 3600.0
        # Round up to nearest 0.25 hours
        import math
        billed = math.ceil(raw_hours / 0.25) * 0.25
        
        # Create entry
        activity = self.ids.activity_input.text.strip() or 'Keine Angabe'
        db.add_entry(self.get_db_path(), self.selected_customer, activity,
                    self._timer_start.isoformat(), end.isoformat(), billed)
        
        # Reset timer
        if self._clock_event:
            self._clock_event.cancel()
        self._timer_start = None
        self._timer_paused_time = 0
        self._pause_start = None
        self.timer_running = False
        self.timer_paused = False
        self.elapsed_seconds = 0
        
        # Update UI
        self.ids.start_btn.disabled = False
        self.ids.pause_btn.disabled = True
        self.ids.pause_btn.text = "PAUSE"
        self.ids.stop_btn.disabled = True
        self.ids.timer_label.text = "00:00:00"
        
        self.show_snackbar(f"Erfasst: {billed:.2f} Std")
        self.refresh_entries()
        
        # Clear activity input
        self.ids.activity_input.text = ''
    
    def refresh_entries(self):
        """Refresh entries list"""
        if 'entries_list' not in self.ids:
            return
        
        entries_list = self.ids.entries_list
        entries_list.clear_widgets()
        
        if self.selected_customer == '—':
            return
        
        rows = db.get_entries(self.get_db_path(), self.selected_customer)
        
        for r in rows:
            entry_id = r[0]
            activity = r[2] or ''
            date = (r[3] or '')[:10]
            hours = r[5]
            
            item = TwoLineListItem(
                text=activity,
                secondary_text=f"{date} — {hours:.2f} Std",
                on_release=lambda x, eid=entry_id: self.show_entry_dialog(eid)
            )
            entries_list.add_widget(item)
    
    def show_entry_dialog(self, entry_id):
        """Show entry details dialog"""
        info = None
        for r in db.get_entries(self.get_db_path()):
            if r[0] == entry_id:
                info = r
                break
        
        if not info:
            return
        
        activity = info[2] or ''
        start = info[3] or ''
        end = info[4] or ''
        hours = info[5]
        notes = info[6] or ''
        
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(MDLabel(text=f"Tätigkeit: {activity}"))
        content.add_widget(MDLabel(text=f"Start: {start}"))
        content.add_widget(MDLabel(text=f"Ende: {end}"))
        content.add_widget(MDLabel(text=f"Stunden: {hours:.2f}"))
        
        notes_field = MDTextField(text=notes, hint_text="Kommentar", multiline=True)
        content.add_widget(notes_field)
        
        def save_notes(*args):
            db.update_entry(self.get_db_path(), entry_id, notes_field.text)
            self.show_snackbar("Kommentar gespeichert")
            self.dialog.dismiss()
            self.refresh_entries()
        
        def delete_entry(*args):
            db.delete_entry(self.get_db_path(), entry_id)
            self.show_snackbar("Eintrag gelöscht")
            self.dialog.dismiss()
            self.refresh_entries()
        
        self.dialog = MDDialog(
            title="Eintrag bearbeiten",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="LÖSCHEN", on_release=delete_entry),
                MDFlatButton(text="ABBRECHEN", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SPEICHERN", on_release=save_notes),
            ],
        )
        self.dialog.open()
    
    def export_pdf(self, auto_share=False, target_dir=None):
        """Export to PDF with automatic open and share"""
        customer = self.selected_customer
        if customer == '—':
            self.show_snackbar("Bitte Kunde auswählen")
            return
        
        rows = db.get_entries(self.get_db_path(), customer)
        if not rows:
            self.show_snackbar("Keine Einträge vorhanden")
            return
        
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from collections import defaultdict
            
            # Zielordner: vom Nutzer gewählt > übergeben > Standard
            out_dir = (self.export_dir if hasattr(self, 'export_dir') and self.export_dir else None)
            if target_dir:
                out_dir = target_dir
            if not out_dir:
                out_dir = self.get_documents_dir()
            base_name = f"report_{customer.replace(' ', '_')}.pdf"
            file_path = os.path.join(out_dir, base_name)
            
            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1976D2'),
                spaceAfter=30,
            )
            elements.append(Paragraph(f"Zeiterfassung - {customer}", title_style))
            elements.append(Spacer(1, 0.5*cm))
            
            # Customer info
            cust = db.get_customer(self.get_db_path(), customer)
            info_data = []
            info_data.append([Paragraph('<b>Kunde:</b>', styles['Normal']), customer])
            info_data.append([Paragraph('<b>Datum:</b>', styles['Normal']), 
                            datetime.datetime.now().strftime('%d.%m.%Y')])
            
            if cust:
                if cust[2]:  # address
                    info_data.append([Paragraph('<b>Adresse:</b>', styles['Normal']), cust[2]])
                if cust[3]:  # email
                    info_data.append([Paragraph('<b>Email:</b>', styles['Normal']), cust[3]])
                if cust[4]:  # phone
                    info_data.append([Paragraph('<b>Telefon:</b>', styles['Normal']), cust[4]])
            
            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 1*cm))
            
            # Group by month
            months_data = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]
                month_key = date_str[:7] if date_str else "Undatiert"
                months_data[month_key].append(r)
            
            sorted_months = sorted(months_data.keys(), reverse=True)
            grand_total = 0.0
            
            # Create table for each month
            for month_key in sorted_months:
                # Month header
                month_style = ParagraphStyle(
                    'MonthHeader',
                    parent=styles['Heading2'],
                    fontSize=16,
                    textColor=colors.HexColor('#1976D2'),
                    spaceAfter=10,
                )
                elements.append(Paragraph(f"Monat: {month_key}", month_style))
                
                # Table data
                data = [['Datum', 'Tätigkeit', 'Stunden']]
                rows_in_month = months_data[month_key]
                month_total = 0.0
                
                for r in rows_in_month:
                    date = (r[3] or '')[:10]
                    act = r[2] or ''
                    hrs = float(r[5] or 0)
                    data.append([date, act, f"{hrs:.2f}"])
                    month_total += hrs
                
                # Month total
                data.append(['', Paragraph('<b>Monatssumme</b>', styles['Normal']), 
                           Paragraph(f'<b>{month_total:.2f}</b>', styles['Normal'])])
                
                # Create table
                t = Table(data, colWidths=[3*cm, 10*cm, 3*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ]))
                
                elements.append(t)
                elements.append(Spacer(1, 0.5*cm))
                grand_total += month_total
            
            # Grand total
            total_data = [[
                Paragraph('<b>Gesamtstunden:</b>', styles['Heading3']),
                Paragraph(f'<b>{grand_total:.2f} Std</b>', styles['Heading3'])
            ]]
            total_table = Table(total_data, colWidths=[10*cm, 6*cm])
            total_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(Spacer(1, 1*cm))
            elements.append(total_table)
            
            # Build PDF
            doc.build(elements)
            
            self.show_snackbar(f"PDF erstellt: {base_name}")
            
            # Open PDF automatically
            self.open_file(file_path, mime_type='application/pdf')
            
            # Share if requested
            if auto_share:
                Clock.schedule_once(lambda dt: self.share_file(file_path, 'application/pdf'), 0.5)
        
        except Exception as e:
            import traceback
            error_msg = f"PDF Export Fehler: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.show_snackbar(f"PDF Fehler: {str(e)}")

    def export_pdf_choose_location(self, auto_share=False):
        """Android: System-Dialog zum Speichern verwenden (SAF). Desktop: Standardpfad.
        Workaround für freie Ordnerwahl auf dem Handy.
        """
        customer = self.selected_customer
        if customer == '—':
            self.show_snackbar("Bitte Kunde auswählen")
            return

        # Generiere PDF zunächst temporär im App-Verzeichnis
        suggested_name = f"report_{customer.replace(' ', '_')}.pdf"
        tmp_dir = self.get_documents_dir()
        tmp_path = os.path.join(tmp_dir, suggested_name)

        # Erzeuge PDF über bestehende Routine (ohne Öffnen/Teilen)
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from collections import defaultdict

            rows = db.get_entries(self.get_db_path(), customer)
            if not rows:
                self.show_snackbar("Keine Einträge vorhanden")
                return

            doc = SimpleDocTemplate(tmp_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1976D2'), spaceAfter=30)
            elements.append(Paragraph(f"Zeiterfassung - {customer}", title_style))
            elements.append(Spacer(1, 0.5*cm))

            cust = db.get_customer(self.get_db_path(), customer)
            info_data = [[Paragraph('<b>Kunde:</b>', styles['Normal']), customer],
                         [Paragraph('<b>Datum:</b>', styles['Normal']), datetime.datetime.now().strftime('%d.%m.%Y')]]
            if cust:
                if cust[2]: info_data.append([Paragraph('<b>Adresse:</b>', styles['Normal']), cust[2]])
                if cust[3]: info_data.append([Paragraph('<b>Email:</b>', styles['Normal']), cust[3]])
                if cust[4]: info_data.append([Paragraph('<b>Telefon:</b>', styles['Normal']), cust[4]])
            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
            elements.append(info_table)
            elements.append(Spacer(1, 1*cm))

            months = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]
                key = date_str[:7] if date_str else 'Undatiert'
                months[key].append(r)
            grand_total = 0.0
            for key in sorted(months.keys(), reverse=True):
                month_style = ParagraphStyle('MonthHeader', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#1976D2'), spaceAfter=10)
                elements.append(Paragraph(f"Monat: {key}", month_style))
                data = [['Datum', 'Tätigkeit', 'Stunden']]
                total = 0.0
                for r in months[key]:
                    date = (r[3] or '')[:10]
                    act = r[2] or ''
                    hrs = float(r[5] or 0)
                    data.append([date, act, f"{hrs:.2f}"])
                    total += hrs
                data.append(['', Paragraph('<b>Monatssumme</b>', styles['Normal']), Paragraph(f'<b>{total:.2f}</b>', styles['Normal'])])
                t = Table(data, colWidths=[3*cm, 10*cm, 3*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1976D2')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (2,0), (2,-1), 'RIGHT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 12),
                    ('BACKGROUND', (0,1), (-1,-2), colors.beige),
                    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E3F2FD')),
                    ('GRID', (0,0), (-1,-1), 1, colors.grey)
                ]))
                elements.append(t)
                elements.append(Spacer(1, 0.5*cm))
                grand_total += total

            total_data = [[Paragraph('<b>Gesamtstunden:</b>', styles['Heading3']), Paragraph(f'<b>{grand_total:.2f} Std</b>', styles['Heading3'])]]
            total_table = Table(total_data, colWidths=[10*cm, 6*cm])
            total_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0,0), (-1,-1), colors.whitesmoke),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ]))
            elements.append(Spacer(1, 1*cm))
            elements.append(total_table)

            doc.build(elements)

            # Android: Speichern via SAF (System-Dialog)
            if IS_ANDROID:
                try:
                    from androidstorage4kivy import SharedStorage
                    ss = SharedStorage()
                    ok = ss.save_file(tmp_path, suggested_name, 'application/pdf')
                    if ok:
                        self.show_snackbar("PDF gespeichert (Benutzerordner)")
                        if auto_share:
                            self.share_file(tmp_path, 'application/pdf')
                        return
                    else:
                        self.show_snackbar("Speichern abgebrochen")
                        return
                except Exception as e:
                    print(f"SAF save error: {e}")
                    # Fallback: belasse Datei im tmp_path
                    self.show_snackbar(f"Gespeichert in: {tmp_path}")

            # Desktop/iOS: Standard öffnen
            self.open_file(tmp_path, mime_type='application/pdf')
            if auto_share:
                Clock.schedule_once(lambda dt: self.share_file(tmp_path, 'application/pdf'), 0.5)

        except Exception as e:
            import traceback
            print(f"PDF Choose Location Fehler: {e}\n{traceback.format_exc()}")
            self.show_snackbar(f"PDF Fehler: {str(e)}")
    
    def export_csv(self, auto_share=False):
        """Export to CSV"""
        customer = self.selected_customer
        if customer == '—':
            self.show_snackbar("Bitte Kunde auswählen")
            return
        
        rows = db.get_entries(self.get_db_path(), customer)
        if not rows:
            self.show_snackbar("Keine Einträge vorhanden")
            return
        
        try:
            import csv
            from collections import defaultdict
            
            out_dir = self.get_documents_dir()
            base_name = f"report_{customer.replace(' ', '_')}.csv"
            file_path = os.path.join(out_dir, base_name)
            
            months_data = defaultdict(list)
            for r in rows:
                date_str = (r[3] or '')[:10]
                month_key = date_str[:7] if date_str else "Undatiert"
                months_data[month_key].append(r)
            
            sorted_months = sorted(months_data.keys(), reverse=True)
            grand_total = 0.0
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Kunde', customer])
                writer.writerow(['Erstellt am', datetime.datetime.now().isoformat(timespec='seconds')])
                
                cust = db.get_customer(self.get_db_path(), customer)
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
            
            if auto_share:
                self.share_file(file_path, 'text/csv')
            else:
                self.show_snackbar(f"CSV exportiert: {base_name}")
        
        except Exception as e:
            self.show_snackbar(f"Export Fehler: {str(e)}")
    
    def open_file(self, filepath, mime_type='application/pdf'):
        """Open file with default viewer"""
        try:
            if IS_ANDROID:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                context = PythonActivity.mActivity
                java_file = File(filepath)
                
                try:
                    FileProvider = autoclass('androidx.core.content.FileProvider')
                    # Authority muss mit package.domain + package.name übereinstimmen
                    authority = "org.tkideneb2.zeiterfassung.fileprovider"
                    uri = FileProvider.getUriForFile(context, authority, java_file)
                except:
                    uri = Uri.fromFile(java_file)
                
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, mime_type)
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                context.startActivity(intent)
                
            elif IS_IOS:
                # iOS file opening
                import webbrowser
                webbrowser.open(filepath)
            else:
                # Desktop - open with default application
                import subprocess
                if sys.platform == 'win32':
                    os.startfile(filepath)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.call(['open', filepath])
                else:  # linux
                    subprocess.call(['xdg-open', filepath])
                    
        except Exception as e:
            print(f"Open file error: {e}")
            self.show_snackbar(f"Öffnen fehlgeschlagen: {str(e)}")
    
    def share_file(self, filepath, mime_type='application/pdf'):
        """Share file using plyer (cross-platform)"""
        try:
            if IS_ANDROID or IS_IOS:
                # Use native share on mobile
                if IS_ANDROID:
                    from jnius import autoclass, cast
                    Intent = autoclass('android.content.Intent')
                    Uri = autoclass('android.net.Uri')
                    File = autoclass('java.io.File')
                    String = autoclass('java.lang.String')
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    
                    context = PythonActivity.mActivity
                    java_file = File(filepath)
                    
                    try:
                        FileProvider = autoclass('androidx.core.content.FileProvider')
                        authority = "org.tkideneb2.zeiterfassung.fileprovider"
                        uri = FileProvider.getUriForFile(context, authority, java_file)
                    except:
                        uri = Uri.fromFile(java_file)
                    
                    intent = Intent(Intent.ACTION_SEND)
                    # Setze korrekten MIME Type (z.B. application/pdf)
                    intent.setType(mime_type or 'application/octet-stream')
                    intent.putExtra(Intent.EXTRA_STREAM, uri)
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    
                    title = cast('java.lang.CharSequence', String('Report teilen via'))
                    chooser = Intent.createChooser(intent, title)
                    context.startActivity(chooser)
                    self.show_snackbar("Datei wird geteilt...")
                    
                elif IS_IOS:
                    # iOS sharing
                    from pyobjus import autoclass
                    UIActivityViewController = autoclass('UIActivityViewController')
                    NSURL = autoclass('NSURL')
                    
                    url = NSURL.fileURLWithPath_(filepath)
                    controller = UIActivityViewController.alloc().initWithActivityItems_applicationActivities_([url], None)
                    # Present controller (requires more iOS setup)
                    self.show_snackbar("iOS Sharing wird vorbereitet...")
            else:
                self.show_snackbar(f"Datei gespeichert: {filepath}")
        
        except Exception as e:
            self.show_snackbar(f"Share Fehler: {str(e)}")


class ZeiterfassungApp(MDApp):
    """Main application class"""
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        
        # Load KV file
        from kivy.lang import Builder
        Builder.load_file('zeiterfassung.kv')
        
        return MainScreen()
    
    def on_start(self):
        """Initialize app on start"""
        db_path = os.path.join(self.user_data_dir, 'stundenerfassung.db')
        db.init_db(db_path)
        print(f"DB path: {db_path}")
        print(f"Platform: {'Android' if IS_ANDROID else 'iOS' if IS_IOS else 'Desktop'}")


if __name__ == '__main__':
    ZeiterfassungApp().run()
