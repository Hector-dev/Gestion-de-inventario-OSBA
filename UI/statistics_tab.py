import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QComboBox, QHBoxLayout, 
                           QSpinBox, QGridLayout, QScrollArea, QSpacerItem, 
                           QSizePolicy, QFrame, QLabel)
from PyQt5.QtCore import Qt

class StatisticsTab:
    def __init__(self, inventory_controller):
        self.inventory_controller = inventory_controller
        self.period_mapping = {
            "Día": "daily",
            "Semana": "weekly",
            "Mes": "monthly",
            "Año": "yearly"
        }

    def create_statistics_widget(self):
        # Crear QScrollArea principal
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget principal que contendrá todo
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Panel de filtros fijo en la parte superior
        filters_widget = QWidget()
        filters_layout = QHBoxLayout(filters_widget)
        filters_layout.setContentsMargins(0, 0, 0, 0)

        # Grupo de filtro de período
        period_group = QWidget()
        period_layout = QHBoxLayout(period_group)
        period_layout.setContentsMargins(0, 0, 0, 0)
        
        period_label = QLabel("Período de ventas:")
        self.period_filter = QComboBox()
        self.period_filter.addItems(self.period_mapping.keys())
        self.period_filter.setMinimumWidth(120)
        self.period_filter.currentIndexChanged.connect(self.update_statistics)
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_filter)
        period_layout.addStretch()

        # Grupo de filtro de productos top
        top_products_group = QWidget()
        top_products_layout = QHBoxLayout(top_products_group)
        top_products_layout.setContentsMargins(0, 0, 0, 0)
        
        products_label = QLabel("Top productos:")
        self.top_products_filter = QComboBox()
        self.top_products_filter.addItems(["5", "10", "15", "20"])
        self.top_products_filter.setMinimumWidth(120)
        self.top_products_filter.currentIndexChanged.connect(self.update_statistics)
        
        top_products_layout.addWidget(products_label)
        top_products_layout.addWidget(self.top_products_filter)
        top_products_layout.addStretch()

        # Añadir grupos de filtros al layout de filtros
        filters_layout.addWidget(period_group)
        filters_layout.addWidget(top_products_group)
        filters_layout.addStretch()

        # Crear área scrollable para las gráficas
        charts_scroll = QScrollArea()
        charts_scroll.setWidgetResizable(True)
        charts_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        charts_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget contenedor para las gráficas
        charts_widget = QWidget()
        charts_layout = QVBoxLayout(charts_widget)
        charts_layout.setSpacing(30)
        charts_layout.setContentsMargins(0, 0, 0, 0)

        # Crear contenedores para cada gráfica
        self.sales_widget = QWidget()
        self.sales_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sales_graph_layout = QVBoxLayout(self.sales_widget)
        
        self.products_widget = QWidget()
        self.products_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.top_products_graph_layout = QVBoxLayout(self.products_widget)
        
        self.category_widget = QWidget()
        self.category_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.category_distribution_layout = QVBoxLayout(self.category_widget)

        # Añadir widgets de gráficas al layout
        charts_layout.addWidget(self.sales_widget)
        charts_layout.addWidget(self.products_widget)
        charts_layout.addWidget(self.category_widget)
        charts_layout.addStretch()

        # Configurar el área scrollable de gráficas
        charts_scroll.setWidget(charts_widget)

        # Añadir todo al layout principal
        main_layout.addWidget(filters_widget)
        main_layout.addWidget(charts_scroll, 1)  # El 1 da prioridad de expansión

        # Configurar el scroll principal
        main_scroll.setWidget(main_widget)

        # Generar estadísticas iniciales
        self.update_statistics()

        return main_scroll

    def update_statistics(self):
        """Actualiza los gráficos al cambiar los filtros."""
        # Limpiar gráficos existentes
        for layout in [self.sales_graph_layout, self.top_products_graph_layout, 
                      self.category_distribution_layout]:
            for i in reversed(range(layout.count())):
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)

        # Actualizar gráficos con el nuevo tamaño
        sales_chart = self._create_sales_chart()
        sales_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sales_graph_layout.addWidget(sales_chart)

        products_chart = self._create_top_products_chart()
        products_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.top_products_graph_layout.addWidget(products_chart)

        category_chart = self._create_category_distribution_chart()
        category_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.category_distribution_layout.addWidget(category_chart)

    def _create_sales_chart(self):
        period = self.period_filter.currentText()
        mapped_period = self.period_mapping.get(period, "daily")
        sales_data = getattr(self.inventory_controller, f"get_{mapped_period}_sales")()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('none')  # Fondo transparente
        
        ax.bar(sales_data.keys(), sales_data.values(), color='#2563eb')
        ax.set_title(f'Ventas Totales por {period}', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel(period, fontsize=14, labelpad=10)
        ax.set_ylabel('Ventas ($)', fontsize=14, labelpad=10)
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        return canvas

    def _create_top_products_chart(self):
        top_count = int(self.top_products_filter.currentText())
        top_productos = self.inventory_controller.get_top_selling_products(top_count)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('none')  # Fondo transparente
        
        nombres = [p['name'] for p in top_productos]
        ventas = [p['total_sales'] for p in top_productos]
        
        ax.bar(nombres, ventas, color='#16a34a')
        ax.set_title(f'Top {top_count} Productos Más Vendidos', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Producto', fontsize=14, labelpad=10)
        ax.set_ylabel('Cantidad Vendida', fontsize=14, labelpad=10)
        ax.tick_params(axis='x', rotation=30, labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        return canvas

    def _create_category_distribution_chart(self):
        distribucion_categorias = self.inventory_controller.get_category_distribution()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('none')  # Fondo transparente
        
        wedges, texts, autotexts = ax.pie(
            distribucion_categorias.values(),
            labels=distribucion_categorias.keys(),
            autopct='%1.1f%%',
            colors=plt.cm.Paired.colors,
            textprops={'fontsize': 12}
        )
        
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12)
        
        ax.set_title('Distribución de Productos por Categoría', 
                    fontsize=16, weight='bold', pad=20)
        
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        return canvas