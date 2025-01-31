# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QMenu, QInputDialog, QVBoxLayout
from PyQt5 import QtWidgets
from ui.ui_mainwindow import Ui_MainWindow
from controllers.inventory import *
from dialogs.product_dialog import ProductDialog
from controllers.statistics_tab import StatisticsTab
from sqlalchemy import create_engine
from db.models import Base
from controllers.reports_tab import ReportsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.inventory_controller = InventoryController()

        self.setup_ui_table()
        self.dispatch_items = []
        self.setup_ui_table()
        self.setup_connections()
        self.load_products_to_dispatch()
        self.load_products()
        self.update_summary()
        
        self.reports_tab = ReportsTab(self.inventory_controller)
        self.ui.tabReportes.layout().addWidget(self.reports_tab)
        self.statistics_tab = StatisticsTab(self.inventory_controller)
        statistics_widget = self.statistics_tab.create_statistics_widget()
        self.ui.tabEstadisticas.setLayout(QVBoxLayout())
        self.ui.tabEstadisticas.layout().addWidget(statistics_widget)

    def setup_ui_table(self):
        """Configura las propiedades iniciales de la tabla de productos"""
        # Deshabilitar edición directa
        self.ui.tableProducts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Habilitar selección por filas completas
        self.ui.tableProducts.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # Selección múltiple
        self.ui.tableProducts.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        
        # Ajustar el ancho de las columnas
        self.ui.tableProducts.setColumnWidth(0, 100)  # Código
        self.ui.tableProducts.setColumnWidth(1, 250)  # Nombre
        self.ui.tableProducts.setColumnWidth(2, 100)  # Stock
        self.ui.tableProducts.setColumnWidth(3, 100)  # Precio
        self.ui.tableProducts.setColumnWidth(4, 150)  # Categoría

    def setup_connections(self):
        """Conecta las señales de los botones con sus respectivas funciones"""
        self.ui.btnNuevoProducto.clicked.connect(self.add_product)
        self.ui.btnEditar.clicked.connect(self.edit_product)
        self.ui.btnEliminar.clicked.connect(self.delete_products)
        self.ui.searchBox.textChanged.connect(self.filter_products)
        """Conecta las señales de los botones con sus respectivas funciones."""
        self.ui.searchBoxDespacho.textChanged.connect(self.filter_products_to_dispatch)
        self.ui.tableProductsDespacho.cellDoubleClicked.connect(self.add_product_to_dispatch)
        self.ui.btnConfirmarVenta.clicked.connect(self.confirm_dispatch)
        # coneccion botón "Cancelar Venta"
        self.ui.btnCancelarVenta.clicked.connect(self.cancel_dispatch)
        self.generateReportButton = QtWidgets.QPushButton(self)




    def load_products(self):
        """Carga los productos en la tabla"""
        products = self.inventory_controller.get_all_products()
        self.ui.tableProducts.setRowCount(len(products))
        for row, product in enumerate(products):
            self.ui.tableProducts.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.ui.tableProducts.setItem(row, 1, QTableWidgetItem(product.name))
            self.ui.tableProducts.setItem(row, 2, QTableWidgetItem(str(product.stock)))
            self.ui.tableProducts.setItem(row, 3, QTableWidgetItem(f"${product.price:.2f}"))
            self.ui.tableProducts.setItem(row, 4, QTableWidgetItem(product.category))

    def filter_products(self, text):
        """Filtra los productos en la tabla según el texto de búsqueda"""
        for row in range(self.ui.tableProducts.rowCount()):
            show = False
            for col in range(self.ui.tableProducts.columnCount()):
                item = self.ui.tableProducts.item(row, col)
                if item and text.lower() in item.text().lower():
                    show = True
                    break
            self.ui.tableProducts.setRowHidden(row, not show)

    def add_product(self):
        """Añade un nuevo producto"""
        dialog = ProductDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            message = self.inventory_controller.add_product(
                data["name"], 
                data["category"], 
                data["price"], 
                data["stock"]
            )
            QMessageBox.information(self, "Nuevo Producto", message)
            self.load_products()

    def edit_product(self):
        """Edita el producto seleccionado"""
        selected_row = self.ui.tableProducts.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producto para editar.")
            return

        product_id = int(self.ui.tableProducts.item(selected_row, 0).text())
        current_product = {
            "name": self.ui.tableProducts.item(selected_row, 1).text(),
            "category": self.ui.tableProducts.item(selected_row, 4).text(),
            "price": float(self.ui.tableProducts.item(selected_row, 3).text().replace("$", "")),
            "stock": int(self.ui.tableProducts.item(selected_row, 2).text())
        }

        dialog = ProductDialog(self, product=current_product)
        if dialog.exec_():
            data = dialog.get_data()
            message = self.inventory_controller.edit_product(
                product_id,
                data["name"],
                data["category"],
                data["price"],
                data["stock"]
            )
            QMessageBox.information(self, "Editar Producto", message)
            self.load_products()

    def open_context_menu(self, position):
        """Muestra un menú contextual en la tabla de productos añadidos."""
        menu = QMenu(self)
        quitar_action = menu.addAction("Quitar Producto Añadido")
        modificar_action = menu.addAction("Modificar Cantidad de Producto")

        # Conectar las acciones
        quitar_action.triggered.connect(self.quitar_producto)
        modificar_action.triggered.connect(self.modificar_cantidad_producto)

        menu.exec_(self.ui.tableAddedProducts.viewport().mapToGlobal(position))

    def quitar_producto(self):
        """Elimina el producto seleccionado de la tabla de despacho."""
        selected_row = self.ui.tableAddedProducts.currentRow()
        if selected_row >= 0:
            del self.dispatch_items[selected_row]
            self.update_dispatch_table()
            self.update_dispatch_total()
        else:
            QMessageBox.warning(self, "Error", "Selecciona un producto para quitar.")

    def modificar_cantidad_producto(self):
        """Modifica la cantidad de un producto en el despacho."""
        selected_row = self.ui.tableAddedProducts.currentRow()
        if selected_row >= 0:
            item = self.dispatch_items[selected_row]
            nueva_cantidad, ok = QInputDialog.getInt(
                self, "Modificar Cantidad", f"Nueva cantidad para {item['name']}:",
                value=item['quantity'], min=1
            )
            if ok:
                item['quantity'] = nueva_cantidad
                item['subtotal'] = nueva_cantidad * item['price']
                self.update_dispatch_table()
                self.update_dispatch_total()
        else:
            QMessageBox.warning(self, "Error", "Selecciona un producto para modificar.")


    def delete_products(self):
        """Elimina los productos seleccionados"""
        selected_rows = self.ui.tableProducts.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Selecciona uno o más productos para eliminar.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar los productos seleccionados?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            for index in sorted(selected_rows, reverse=True):
                product_id = int(self.ui.tableProducts.item(index.row(), 0).text())
                self.inventory_controller.delete_product(product_id)
            
            QMessageBox.information(self, "Eliminar Productos", "Los productos seleccionados han sido eliminados.")
            self.load_products()

    def cancel_dispatch(self):
        """Cancela la venta actual y limpia los datos de despacho."""
        confirm = QMessageBox.question(
            self, "Cancelar Venta", "¿Estás seguro de que deseas cancelar esta venta?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            # Limpiar los productos añadidos al despacho
            self.dispatch_items.clear()
            self.update_dispatch_table()
            self.update_dispatch_total()
            QMessageBox.information(self, "Venta Cancelada", "Se ha cancelado la venta actual.")

    """funciones de despacho"""
    def load_products_to_dispatch(self):
        """Carga los productos disponibles en la tabla de despacho."""
        products = self.inventory_controller.get_all_products()
        self.ui.tableProductsDespacho.setRowCount(len(products))
        for row, product in enumerate(products):
            self.ui.tableProductsDespacho.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.ui.tableProductsDespacho.setItem(row, 1, QTableWidgetItem(product.name))
            self.ui.tableProductsDespacho.setItem(row, 2, QTableWidgetItem(f"${product.price:.2f}"))
            self.ui.tableProductsDespacho.setItem(row, 3, QTableWidgetItem(str(product.stock)))

    def filter_products_to_dispatch(self, text):
        """Filtra los productos disponibles según el texto ingresado."""
        for row in range(self.ui.tableProductsDespacho.rowCount()):
            show = False
            for col in range(self.ui.tableProductsDespacho.columnCount()):
                item = self.ui.tableProductsDespacho.item(row, col)
                if item and text.lower() in item.text().lower():
                    show = True
                    break
            self.ui.tableProductsDespacho.setRowHidden(row, not show)

    def add_product_to_dispatch(self, row, column):
        """Añade un producto al despacho con selección de cantidad."""
        product_id = int(self.ui.tableProductsDespacho.item(row, 0).text())
        product_name = self.ui.tableProductsDespacho.item(row, 1).text()
        product_price = float(self.ui.tableProductsDespacho.item(row, 2).text().replace("$", ""))
        available_stock = int(self.ui.tableProductsDespacho.item(row, 3).text())

        # Abrir diálogo para seleccionar cantidad
        quantity, ok = QInputDialog.getInt(
            self, 
            "Seleccionar Cantidad", 
            f"Seleccione la cantidad de {product_name} a agregar:", 
            min=1, 
            max=available_stock, 
            value=1
        )

        if ok and quantity > 0:
            # Verificar si el producto ya está en el despacho
            for item in self.dispatch_items:
                if item['id'] == product_id:
                    item['quantity'] += quantity
                    item['subtotal'] = item['quantity'] * item['price']
                    break
            else:
                # Añadir nuevo producto al despacho
                self.dispatch_items.append({
                    'id': product_id,
                    'name': product_name,
                    'price': product_price,
                    'quantity': quantity,
                    'subtotal': product_price * quantity
                })

            self.update_dispatch_table()
            self.update_dispatch_total()

    def update_dispatch_table(self):
        """Actualiza la tabla de productos añadidos al despacho."""
        self.ui.tableAddedProducts.setRowCount(len(self.dispatch_items))
        for row, item in enumerate(self.dispatch_items):
            self.ui.tableAddedProducts.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.ui.tableAddedProducts.setItem(row, 1, QTableWidgetItem(item['name']))
            self.ui.tableAddedProducts.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.ui.tableAddedProducts.setItem(row, 3, QTableWidgetItem(f"${item['subtotal']:.2f}"))

    def update_dispatch_total(self):
        """Actualiza el total del despacho."""
        total = sum(item['subtotal'] for item in self.dispatch_items)
        self.ui.labelTotal.setText(f"Total: ${total:.2f}")

    def confirm_dispatch(self):
        """Confirma la venta y actualiza la base de datos."""
        if not self.dispatch_items:
            QMessageBox.warning(self, "Error", "No hay productos en el despacho.")
            return

        result = self.inventory_controller.process_sale(self.dispatch_items)
        if "Error" in result:
            QMessageBox.critical(self, "Error", result)
        else:
            QMessageBox.information(self, "Venta confirmada", result)
            self.dispatch_items.clear()
            self.update_dispatch_table()
            self.update_dispatch_total()
            self.load_products_to_dispatch()

    def generate_report(self):
        """Genera un reporte basado en la selección del usuario."""
        report_type = self.ui.reportTypeComboBox.currentText()  # Obtén el tipo de reporte
        self.ui.reportStatusLabel.setText(f"Generando el {report_type.lower()}...")  # Actualiza el estado
        
        # Aquí puedes implementar la lógica real de generación de reportes
        # Por ejemplo, generar un archivo o mostrar un resumen:
        try:
            # Simulación de generación de reporte
            if report_type == "Reporte Diario":
                self.generate_daily_report()
            elif report_type == "Reporte Semanal":
                self.generate_weekly_report()
            elif report_type == "Reporte Mensual":
                self.generate_monthly_report()

            self.ui.reportStatusLabel.setText(f"{report_type} generado exitosamente.")
        except Exception as e:
            self.ui.reportStatusLabel.setText(f"Error al generar el {report_type.lower()}: {str(e)}")

    def generate_daily_report(self):
        """Genera un reporte diario en formato CSV."""
        from datetime import datetime
        import csv

        today = datetime.now().strftime("%Y-%m-%d")  # Fecha actual
        file_name = f"reporte_diario_{today}.csv"  # Nombre del archivo

        try:
            # Obtener datos de ventas del día
            daily_sales = self.inventory_controller.get_daily_sales_data(today)

            # Crear archivo CSV
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Producto", "Cantidad Vendida", "Precio Total"])
                for sale in daily_sales:
                    writer.writerow([sale["product"], sale["quantity"], sale["total_price"]])

            # Mensaje de éxito
            self.ui.reportStatusLabel.setText(f"Reporte diario guardado como {file_name}.")
            print(f"Reporte diario generado: {file_name}")

        except Exception as e:
            self.ui.reportStatusLabel.setText(f"Error al generar el reporte diario: {str(e)}")
            print(f"Error: {e}")

    def generate_weekly_report(self):
        """Genera un reporte semanal en formato CSV."""
        from datetime import datetime, timedelta
        import csv

        today = datetime.now()
        start_of_week = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")  # Lunes de la semana actual
        end_of_week = (today + timedelta(days=6 - today.weekday())).strftime("%Y-%m-%d")  # Domingo de la semana actual
        file_name = f"reporte_semanal_{start_of_week}_a_{end_of_week}.csv"

        try:
            # Obtener datos de ventas de la semana
            weekly_sales = self.inventory_controller.get_weekly_sales_data(start_of_week, end_of_week)

            # Crear archivo CSV
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Producto", "Cantidad Vendida", "Precio Total"])
                for sale in weekly_sales:
                    writer.writerow([sale["product"], sale["quantity"], sale["total_price"]])

            # Mensaje de éxito
            self.ui.reportStatusLabel.setText(f"Reporte semanal guardado como {file_name}.")
            print(f"Reporte semanal generado: {file_name}")

        except Exception as e:
            self.ui.reportStatusLabel.setText(f"Error al generar el reporte semanal: {str(e)}")
            print(f"Error: {e}")

    def generate_weekly_report(self):
        """Genera un reporte semanal en formato CSV."""
        from datetime import datetime, timedelta
        import csv

        today = datetime.now()
        start_of_week = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")  # Lunes de la semana actual
        end_of_week = (today + timedelta(days=6 - today.weekday())).strftime("%Y-%m-%d")  # Domingo de la semana actual
        file_name = f"reporte_semanal_{start_of_week}_a_{end_of_week}.csv"

        try:
            # Obtener datos de ventas de la semana
            weekly_sales = self.inventory_controller.get_weekly_sales_data(start_of_week, end_of_week)

            # Crear archivo CSV
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Producto", "Cantidad Vendida", "Precio Total"])
                for sale in weekly_sales:
                    writer.writerow([sale["product"], sale["quantity"], sale["total_price"]])

            # Mensaje de éxito
            self.ui.reportStatusLabel.setText(f"Reporte semanal guardado como {file_name}.")
            print(f"Reporte semanal generado: {file_name}")

        except Exception as e:
            self.ui.reportStatusLabel.setText(f"Error al generar el reporte semanal: {str(e)}")
            print(f"Error: {e}")

    def update_summary(self):
        """Actualiza la sección de resumen de datos en la pestaña Inicio."""
        total_products = self.inventory_controller.get_total_products()
        total_sales = self.inventory_controller.get_total_sales()
        total_profit = self.inventory_controller.get_total_profit()

        self.ui.valueTotalProductos.setText(str(total_products))
        self.ui.valueVentasTotales.setText(f"{total_sales}")
        self.ui.valueGananciasTotales.setText(f"${total_profit:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())