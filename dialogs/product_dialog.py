# ui/dialogs/product_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt

class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setup_ui()
        if product:
            self.set_product_data(product)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.price_input = QLineEdit()
        self.stock_input = QLineEdit()
        
        form.addRow("Nombre:", self.name_input)
        form.addRow("Categoría:", self.category_input)
        form.addRow("Precio:", self.price_input)
        form.addRow("Stock:", self.stock_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "price": float(self.price_input.text() or 0),
            "stock": int(self.stock_input.text() or 0)
        }

    def set_product_data(self, product):
        self.name_input.setText(product["name"])
        self.category_input.setText(product["category"])
        self.price_input.setText(str(product["price"]))
        self.stock_input.setText(str(product["stock"]))
