# reports_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                           QLabel, QPushButton, QComboBox, QCalendarWidget,
                           QCheckBox, QFileDialog, QProgressBar, QTableWidget,
                           QTableWidgetItem, QTabWidget, QScrollArea)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
import pandas as pd
from datetime import datetime, timedelta
import os

class ReportsTab(QWidget):
    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configura la interfaz de usuario para la pestaña de reportes"""
        # Contenedor principal con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget contenedor para el scroll
        scroll_content = QWidget()
        main_layout = QVBoxLayout(scroll_content)
        
        # Panel de configuración
        config_group = QGroupBox("Configuración del Reporte")
        config_layout = QVBoxLayout()
        
        # Tipo de reporte
        report_type_layout = QHBoxLayout()
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Reporte Diario", "Reporte Semanal", "Reporte Mensual", 
            "Reporte Personalizado"
        ])
        report_type_layout.addWidget(QLabel("Tipo de Reporte:"))
        report_type_layout.addWidget(self.report_type_combo)
        config_layout.addLayout(report_type_layout)
        
        # Selector de fechas
        dates_group = QGroupBox("Rango de Fechas")
        dates_layout = QHBoxLayout()
        
        # Fecha inicial
        start_date_layout = QVBoxLayout()
        self.start_calendar = QCalendarWidget()
        start_date_layout.addWidget(QLabel("Fecha Inicial:"))
        start_date_layout.addWidget(self.start_calendar)
        dates_layout.addLayout(start_date_layout)
        
        # Fecha final
        end_date_layout = QVBoxLayout()
        self.end_calendar = QCalendarWidget()
        end_date_layout.addWidget(QLabel("Fecha Final:"))
        end_date_layout.addWidget(self.end_calendar)
        dates_layout.addLayout(end_date_layout)
        
        dates_group.setLayout(dates_layout)
        config_layout.addWidget(dates_group)
        
        # Opciones de contenido
        content_group = QGroupBox("Contenido del Reporte")
        content_layout = QVBoxLayout()
        
        self.include_products = QCheckBox("Incluir detalle de productos")
        self.include_categories = QCheckBox("Agrupar por categorías")
        self.include_charts = QCheckBox("Incluir gráficos")
        self.include_summary = QCheckBox("Incluir resumen")
        
        content_layout.addWidget(self.include_products)
        content_layout.addWidget(self.include_categories)
        content_layout.addWidget(self.include_charts)
        content_layout.addWidget(self.include_summary)
        
        content_group.setLayout(content_layout)
        config_layout.addWidget(content_group)
        
        # Formato de salida
        format_layout = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel", "PDF"])
        format_layout.addWidget(QLabel("Formato de salida:"))
        format_layout.addWidget(self.format_combo)
        config_layout.addLayout(format_layout)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Previsualización
        preview_group = QGroupBox("Previsualización")
        preview_layout = QVBoxLayout()
        
        # Tabs para diferentes vistas previas
        self.preview_tabs = QTabWidget()
        
        # Tab de datos
        self.preview_table = QTableWidget()
        self.preview_tabs.addTab(self.preview_table, "Datos")
        
        # Tab de gráficos
        self.chart_view = QChartView()
        self.preview_tabs.addTab(self.chart_view, "Gráficos")
        
        preview_layout.addWidget(self.preview_tabs)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        self.preview_button = QPushButton("Previsualizar")
        self.save_config_button = QPushButton("Guardar Configuración")
        
        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addWidget(self.save_config_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Botón generar reporte al final
        self.generate_button = QPushButton("Generar Reporte")
        main_layout.addWidget(self.generate_button)
        
        # Configurar el scroll
        scroll.setWidget(scroll_content)
        
        # Layout final
        final_layout = QVBoxLayout(self)
        final_layout.addWidget(scroll)
        self.setLayout(final_layout)
        
    def setup_connections(self):
        """Configura las conexiones de señales y slots"""
        self.report_type_combo.currentTextChanged.connect(self.on_report_type_changed)
        self.preview_button.clicked.connect(self.preview_report)
        self.generate_button.clicked.connect(self.generate_report)
        self.save_config_button.clicked.connect(self.save_report_config)

    # El resto de los métodos permanecen igual...
    def on_report_type_changed(self, report_type):
        """Maneja el cambio de tipo de reporte"""
        is_custom = report_type == "Reporte Personalizado"
        self.start_calendar.setEnabled(is_custom)
        self.end_calendar.setEnabled(is_custom)
        
        # Establecer fechas predeterminadas según el tipo
        today = QDate.currentDate()
        if report_type == "Reporte Diario":
            self.start_calendar.setSelectedDate(today)
            self.end_calendar.setSelectedDate(today)
        elif report_type == "Reporte Semanal":
            self.start_calendar.setSelectedDate(today.addDays(-today.dayOfWeek() + 1))
            self.end_calendar.setSelectedDate(today)
        elif report_type == "Reporte Mensual":
            self.start_calendar.setSelectedDate(QDate(today.year(), today.month(), 1))
            self.end_calendar.setSelectedDate(today)
            
    def preview_report(self):
        """Genera una vista previa del reporte"""
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Obtener datos según configuración
            start_date = self.start_calendar.selectedDate().toPyDate()
            end_date = self.end_calendar.selectedDate().toPyDate()
            
            # Obtener datos de ventas
            data = self.inventory_controller.get_sales_data(start_date, end_date)
            
            # Actualizar tabla de previsualización
            self.update_preview_table(data)
            
            # Actualizar gráficos si están habilitados
            if self.include_charts.isChecked():
                self.update_preview_charts(data)
                
            self.progress_bar.setValue(100)
            
        except Exception as e:
            self.show_error_message(f"Error al generar vista previa: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
            
    def generate_report(self):
        """Genera y guarda el reporte final"""
        try:
            file_format = self.format_combo.currentText().lower()
            default_name = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Obtener ubicación de guardado
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Guardar Reporte",
                f"{default_name}.{file_format}",
                f"Archivos {file_format.upper()} (*.{file_format})"
            )
            
            if filename:
                # Obtener datos
                start_date = self.start_calendar.selectedDate().toPyDate()
                end_date = self.end_calendar.selectedDate().toPyDate()
                data = self.inventory_controller.get_sales_data(start_date, end_date)
                
                # Generar reporte según formato
                if file_format == 'csv':
                    self.export_to_csv(data, filename)
                elif file_format == 'excel':
                    self.export_to_excel(data, filename)
                elif file_format == 'pdf':
                    self.export_to_pdf(data, filename)
                    
        except Exception as e:
            self.show_error_message(f"Error al generar reporte: {str(e)}")
            
    def save_report_config(self):
        """Guarda la configuración actual del reporte"""
        config = {
            'report_type': self.report_type_combo.currentText(),
            'include_products': self.include_products.isChecked(),
            'include_categories': self.include_categories.isChecked(),
            'include_charts': self.include_charts.isChecked(),
            'include_summary': self.include_summary.isChecked(),
            'format': self.format_combo.currentText()
        }
        
        # Guardar configuración en archivo JSON
        try:
            with open('report_config.json', 'w') as f:
                json.dump(config, f)
        except Exception as e:
            self.show_error_message(f"Error al guardar configuración: {str(e)}")