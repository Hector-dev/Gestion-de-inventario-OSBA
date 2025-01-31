from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Product, Sale, SaleItem
from datetime import datetime
from db.models import Base
from sqlalchemy import func

class InventoryController:
    def __init__(self, db_path='sqlite:///bodega.db'):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)  # Asegúrate de que las tablas existan
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all_products(self):
        """Obtiene todos los productos de la base de datos."""
        return self.session.query(Product).all()

    def get_product(self, product_id):
        """Obtiene un producto específico por ID."""
        return self.session.query(Product).get(product_id)

    def add_product(self, name, category, price, stock):
        """Añade un nuevo producto a la base de datos."""
        try:
            product = Product(name=name, category=category, price=price, stock=stock)
            self.session.add(product)
            self.session.commit()
            return "Producto añadido exitosamente"
        except Exception as e:
            self.session.rollback()
            return f"Error al añadir producto: {str(e)}"

    def edit_product(self, product_id, name, category, price, stock):
        """Edita un producto existente en la base de datos."""
        try:
            product = self.get_product(product_id)
            if product:
                product.name = name
                product.category = category
                product.price = price
                product.stock = stock
                self.session.commit()
                return "Producto actualizado exitosamente"
            return "Producto no encontrado"
        except Exception as e:
            self.session.rollback()
            return f"Error al actualizar producto: {str(e)}"

    def delete_product(self, product_id):
        """Elimina un producto de la base de datos."""
        try:
            product = self.get_product(product_id)
            if product:
                self.session.delete(product)
                self.session.commit()
                return "Producto eliminado exitosamente"
            return "Producto no encontrado"
        except Exception as e:
            self.session.rollback()
            return f"Error al eliminar producto: {str(e)}"

    def process_sale(self, sale_items):
        """Procesa una venta y actualiza el stock de los productos."""
        try:
            sale = Sale(date=datetime.now())
            self.session.add(sale)

            for item in sale_items:
                product = self.get_product(item['id'])
                if not product or product.stock < item['quantity']:
                    raise Exception(f"Stock insuficiente para {product.name}")

                # Reducir el stock del producto
                product.stock -= item['quantity']

                # Crear un ítem de venta
                sale_item = SaleItem(
                    sale=sale,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )
                self.session.add(sale_item)

            self.session.commit()
            return "Venta confirmada exitosamente"
        except Exception as e:
            self.session.rollback()
            return f"Error al procesar la venta: {str(e)}"

    def search_products(self, search_text):
        """Busca productos por nombre o categoría."""
        try:
            return self.session.query(Product).filter(
                (Product.name.ilike(f"%{search_text}%")) |
                (Product.category.ilike(f"%{search_text}%"))
            ).all()
        except Exception as e:
            return []

    def get_top_selling_products(self, limit=5):
        """Obtiene los productos más vendidos."""
        try:
            result = self.session.query(
                Product.name,
                func.sum(SaleItem.quantity).label('total_sales')
            ).join(SaleItem).group_by(Product.id).order_by(func.sum(SaleItem.quantity).desc()).limit(limit).all()

            return [{'name': row[0], 'total_sales': row[1]} for row in result]
        except Exception as e:
            return []

    def get_category_distribution(self):
        """Obtiene la distribución de productos por categoría."""
        try:
            result = self.session.query(
                Product.category,
                func.count(Product.id).label('count')
            ).group_by(Product.category).all()

            return {row[0]: row[1] for row in result}
        except Exception as e:
            return {}

    def get_monthly_sales(self):
        """Obtiene las ventas totales agrupadas por mes."""
        try:
            result = self.session.query(
                func.strftime('%Y-%m', Sale.date).label('month'),
                func.sum(SaleItem.quantity * SaleItem.price).label('total_sales')
            ).join(SaleItem).group_by('month').order_by('month').all()

            return {row.month: row.total_sales for row in result}
        except Exception as e:
            return {}
        
    def __del__(self):
        """Cierra la sesión y el motor al eliminar la instancia."""
        self.session.close()

    def get_daily_sales(self):
        """Obtiene las ventas agrupadas por día."""
        result = self.session.query(
            func.date(Sale.date).label('day'),
            func.sum(SaleItem.quantity * SaleItem.price).label('total_sales')
        ).join(SaleItem).group_by('day').order_by('day').all()
        return {row.day: row.total_sales for row in result}

    def get_weekly_sales(self):
        """Obtiene las ventas agrupadas por semana."""
        result = self.session.query(
            func.strftime('%Y-%W', Sale.date).label('week'),
            func.sum(SaleItem.quantity * SaleItem.price).label('total_sales')
        ).join(SaleItem).group_by('week').order_by('week').all()
        return {row.week: row.total_sales for row in result}

    def get_monthly_sales(self):
        """Obtiene las ventas agrupadas por mes."""
        result = self.session.query(
            func.strftime('%Y-%m', Sale.date).label('month'),
            func.sum(SaleItem.quantity * SaleItem.price).label('total_sales')
        ).join(SaleItem).group_by('month').order_by('month').all()
        return {row.month: row.total_sales for row in result}

    def get_yearly_sales(self):
        """Obtiene las ventas agrupadas por año."""
        result = self.session.query(
            func.strftime('%Y', Sale.date).label('year'),
            func.sum(SaleItem.quantity * SaleItem.price).label('total_sales')
        ).join(SaleItem).group_by('year').order_by('year').all()
        return {row.year: row.total_sales for row in result}

    def get_total_products(self):
        """Cuenta el número total de productos en la base de datos."""
        return self.session.query(Product).count()

    def get_total_sales(self):
        """Obtiene el total de ventas realizadas."""
        total_sales = self.session.query(Sale).count()
        return total_sales

    def get_total_profit(self):
        """Calcula el total de ganancias basado en ventas registradas."""
        total_profit = self.session.query(
            func.sum(SaleItem.quantity * SaleItem.price)
        ).scalar()

        return total_profit if total_profit else 0.0

    def close_session(self):
        """Cierra la sesión con la base de datos."""
        self.session.close()
