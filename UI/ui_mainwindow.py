# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warehouse-ui-qt-styled.txt'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet(
            """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #ddd;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2563eb;
                color: white;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
            }
            QPushButton#btnNuevoProducto {
                background-color: #2563eb;
                color: white;
            }
            QPushButton#btnEditar, QPushButton#btnEliminar {
                background-color: white;
                border: 1px solid #ddd;
                color: #666;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                gridline-color: #eee;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #ddd;
                color: #374151;
                font-weight: bold;
            }
            QGroupBox {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 1em;
                padding-top: 1em;
            }
            QGroupBox::title {
                color: #374151;
                font-weight: bold;
            }
            """
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Inicio Tab
        self.tabInicio = QtWidgets.QWidget()
        self.tabInicio.setObjectName("tabInicio")
        self.verticalLayoutInicio = QtWidgets.QVBoxLayout(self.tabInicio)
        self.verticalLayoutInicio.setObjectName("verticalLayoutInicio")

        # Welcome Label
        self.labelBienvenida = QtWidgets.QLabel(self.tabInicio)
        self.labelBienvenida.setObjectName("labelBienvenida")
        self.labelBienvenida.setStyleSheet("font-size: 18px; font-weight: bold; color: #374151;")
        self.labelBienvenida.setText("Bienvenido al Sistema de Gestión de Bodega OSBA")
        self.verticalLayoutInicio.addWidget(self.labelBienvenida)

        # Summary Section
        self.groupResumenInicio = QtWidgets.QGroupBox(self.tabInicio)
        self.groupResumenInicio.setObjectName("groupResumenInicio")
        self.groupResumenInicio.setTitle("Resumen de Datos")
        self.groupResumenInicio.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151;")

        self.gridLayoutResumenInicio = QtWidgets.QGridLayout(self.groupResumenInicio)
        self.gridLayoutResumenInicio.setObjectName("gridLayoutResumenInicio")

        # Productos
        self.labelTotalProductos = QtWidgets.QLabel(self.groupResumenInicio)
        self.labelTotalProductos.setObjectName("labelTotalProductos")
        self.labelTotalProductos.setText("Total de productos:")
        self.gridLayoutResumenInicio.addWidget(self.labelTotalProductos, 0, 0)
        self.valueTotalProductos = QtWidgets.QLabel(self.groupResumenInicio)
        self.valueTotalProductos.setObjectName("valueTotalProductos")
        self.valueTotalProductos.setText("0")
        self.gridLayoutResumenInicio.addWidget(self.valueTotalProductos, 0, 1)

        # Ventas Totales
        self.labelVentasTotales = QtWidgets.QLabel(self.groupResumenInicio)
        self.labelVentasTotales.setObjectName("labelVentasTotales")
        self.labelVentasTotales.setText("Ventas totales:")
        self.gridLayoutResumenInicio.addWidget(self.labelVentasTotales, 1, 0)
        self.valueVentasTotales = QtWidgets.QLabel(self.groupResumenInicio)
        self.valueVentasTotales.setObjectName("valueVentasTotales")
        self.valueVentasTotales.setText("0")
        self.gridLayoutResumenInicio.addWidget(self.valueVentasTotales, 1, 1)

        # Ganancias Totales
        self.labelGananciasTotales = QtWidgets.QLabel(self.groupResumenInicio)
        self.labelGananciasTotales.setObjectName("labelGananciasTotales")
        self.labelGananciasTotales.setText("Ganancias totales:")
        self.gridLayoutResumenInicio.addWidget(self.labelGananciasTotales, 2, 0)
        self.valueGananciasTotales = QtWidgets.QLabel(self.groupResumenInicio)
        self.valueGananciasTotales.setObjectName("valueGananciasTotales")
        self.valueGananciasTotales.setText("$0.00")
        self.gridLayoutResumenInicio.addWidget(self.valueGananciasTotales, 2, 1)


        self.verticalLayoutInicio.addWidget(self.groupResumenInicio)
        self.tabWidget.addTab(self.tabInicio, "Inicio")

        # Productos Tab
        self.tabProductos = QtWidgets.QWidget()
        self.tabProductos.setObjectName("tabProductos")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabProductos)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNuevoProducto = QtWidgets.QPushButton(self.tabProductos)
        self.btnNuevoProducto.setObjectName("btnNuevoProducto")
        self.btnNuevoProducto.setText("Nuevo Producto")
        self.horizontalLayout.addWidget(self.btnNuevoProducto)
        self.btnEditar = QtWidgets.QPushButton(self.tabProductos)
        self.btnEditar.setObjectName("btnEditar")
        self.btnEditar.setText("Editar")
        self.horizontalLayout.addWidget(self.btnEditar)
        self.btnEliminar = QtWidgets.QPushButton(self.tabProductos)
        self.btnEliminar.setObjectName("btnEliminar")
        self.btnEliminar.setText("Eliminar")
        self.btnEliminar.setStyleSheet("background-color: #f44336; color: white;")
        self.horizontalLayout.addWidget(self.btnEliminar)
        spacerItem = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.searchBox = QtWidgets.QLineEdit(self.tabProductos)
        self.searchBox.setMinimumWidth(250)
        self.searchBox.setObjectName("searchBox")
        self.searchBox.setPlaceholderText("Buscar producto...")
        self.horizontalLayout.addWidget(self.searchBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableProducts = QtWidgets.QTableWidget(self.tabProductos)
        self.tableProducts.setAlternatingRowColors(True)
        self.tableProducts.setObjectName("tableProducts")
        self.tableProducts.setColumnCount(5)
        self.tableProducts.setHorizontalHeaderLabels(["Código", "Nombre", "Stock", "Precio", "Categoría"])
        self.verticalLayout_2.addWidget(self.tableProducts)
        self.tabWidget.addTab(self.tabProductos, "Productos")

        # Despacho Tab
        self.tabDespacho = QtWidgets.QWidget()
        self.tabDespacho.setObjectName("tabDespacho")
        self.verticalLayoutDespacho = QtWidgets.QVBoxLayout(self.tabDespacho)
        self.verticalLayoutDespacho.setObjectName("verticalLayoutDespacho")


        # Barra de búsqueda
        self.horizontalLayoutDespacho = QtWidgets.QHBoxLayout()
        self.horizontalLayoutDespacho.setObjectName("horizontalLayoutDespacho")
        self.searchBoxDespacho = QtWidgets.QLineEdit(self.tabDespacho)
        self.searchBoxDespacho.setMinimumWidth(250)
        self.searchBoxDespacho.setPlaceholderText("Buscar producto para agregar...")
        self.searchBoxDespacho.setObjectName("searchBoxDespacho")
        self.horizontalLayoutDespacho.addWidget(self.searchBoxDespacho)
        self.verticalLayoutDespacho.addLayout(self.horizontalLayoutDespacho)

        # Tabla de productos disponibles
        self.tableProductsDespacho = QtWidgets.QTableWidget(self.tabDespacho)
        self.tableProductsDespacho.setObjectName("tableProductsDespacho")
        self.tableProductsDespacho.setColumnCount(4)
        self.tableProductsDespacho.setHorizontalHeaderLabels(["Código", "Nombre", "Precio", "Stock"])
        self.tableProductsDespacho.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        self.verticalLayoutDespacho.addWidget(self.tableProductsDespacho)

        # Tabla de productos añadidos
        self.labelAddedProducts = QtWidgets.QLabel(self.tabDespacho)
        self.labelAddedProducts.setObjectName("labelAddedProducts")
        self.labelAddedProducts.setText("Productos añadidos:")
        self.labelAddedProducts.setStyleSheet("font-size: 14px; font-weight: bold; color: #374151;")
        self.verticalLayoutDespacho.addWidget(self.labelAddedProducts)

        self.tableAddedProducts = QtWidgets.QTableWidget(self.tabDespacho)
        self.tableAddedProducts.setObjectName("tableAddedProducts")
        self.tableAddedProducts.setColumnCount(4)
        self.tableAddedProducts.setHorizontalHeaderLabels(["Código", "Nombre", "Cantidad", "Subtotal"])
        self.tableAddedProducts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        self.verticalLayoutDespacho.addWidget(self.tableAddedProducts)

                # Configuración del menú contextual
        self.tableAddedProducts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableAddedProducts.customContextMenuRequested.connect(MainWindow.open_context_menu)


        # Resumen y botones de confirmación
        self.horizontalLayoutSummary = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSummary.setObjectName("horizontalLayoutSummary")

        # Etiqueta para el total
        self.labelTotal = QtWidgets.QLabel(self.tabDespacho)
        self.labelTotal.setObjectName("labelTotal")
        self.labelTotal.setText("Total: $0.00")
        self.labelTotal.setStyleSheet("font-size: 16px; font-weight: bold; color: #111;")
        self.horizontalLayoutSummary.addWidget(self.labelTotal)

        # Espaciador
        spacerSummary = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutSummary.addItem(spacerSummary)

        # Botón Cancelar Venta
        self.btnCancelarVenta = QtWidgets.QPushButton(self.tabDespacho)
        self.btnCancelarVenta.setObjectName("btnCancelarVenta")
        self.btnCancelarVenta.setText("Cancelar Venta")
        self.btnCancelarVenta.setStyleSheet("background-color: #f44336; color: white;")
        self.horizontalLayoutSummary.addWidget(self.btnCancelarVenta)  # Añadido al diseño horizontal

        # Botón Confirmar Venta
        self.btnConfirmarVenta = QtWidgets.QPushButton(self.tabDespacho)
        self.btnConfirmarVenta.setObjectName("btnConfirmarVenta")
        self.btnConfirmarVenta.setText("Confirmar Venta")
        self.btnConfirmarVenta.setStyleSheet("background-color: #2563eb; color: white;")
        self.horizontalLayoutSummary.addWidget(self.btnConfirmarVenta)  # Añadido al diseño horizontal

        # Añadir el diseño horizontal al diseño vertical principal
        self.verticalLayoutDespacho.addLayout(self.horizontalLayoutSummary)

        # Añadir la pestaña de despacho
        self.tabWidget.addTab(self.tabDespacho, "Despacho")

        # Conectar la barra de búsqueda
        self.searchBoxDespacho.textChanged.connect(self.filtrarProductos)

        # Pestañas de estadísticas y reportes
        self.tabEstadisticas = QtWidgets.QWidget()
        self.tabEstadisticas.setObjectName("tabEstadisticas")

        # Configuración inicial para futuras gráficas
        self.verticalLayoutEstadisticas = QtWidgets.QVBoxLayout(self.tabEstadisticas)
        self.verticalLayoutEstadisticas.setObjectName("verticalLayoutEstadisticas")

        self.labelEstadisticas = QtWidgets.QLabel(self.tabEstadisticas)
        self.verticalLayoutEstadisticas.addWidget(self.labelEstadisticas)

        self.tabWidget.addTab(self.tabEstadisticas, "Estadísticas")

        self.tabReportes = QtWidgets.QWidget()
        self.tabReportes.setObjectName("tabReportes")

        # Configuración inicial para generación de reportes
        self.verticalLayoutReportes = QtWidgets.QVBoxLayout(self.tabReportes)
        self.verticalLayoutReportes.setObjectName("verticalLayoutReportes")

        self.tabWidget.addTab(self.tabReportes, "Reportes")

        # Finalización del diseño
        def cargarDatosDespacho(self, productos):
            self.tableProductsDespacho.setRowCount(len(productos))
            for row, producto in enumerate(productos):
                for col, dato in enumerate(producto):
                    self.tableProductsDespacho.setItem(row, col, QtWidgets.QTableWidgetItem(str(dato)))

        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def filtrarProductos(self, texto):
        for i in range(self.tableProductsDespacho.rowCount()):
            match = False
            for j in range(self.tableProductsDespacho.columnCount()):
                item = self.tableProductsDespacho.item(i, j)
                if item and texto.lower() in item.text().lower():
                    match = True
                    break
            self.tableProductsDespacho.setRowHidden(i, not match)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sistema de Gestión de Bodega"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInicio), _translate("MainWindow", "Inicio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProductos), _translate("MainWindow", "Productos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDespacho), _translate("MainWindow", "Despacho"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEstadisticas), _translate("MainWindow", "Estadísticas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReportes), _translate("MainWindow", "Reportes"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
