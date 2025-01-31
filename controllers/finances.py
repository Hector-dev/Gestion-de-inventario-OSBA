# controllers/finances.py
class FinancesController:
    def __init__(self):
        self.db = Database()

    def get_total_sales(self):
        """Obtiene el total de ventas"""
        return self.db.session.query(func.sum(Sale.total)).scalar() or 0.0

    def get_total_profits(self):
        """Calcula las ganancias totales"""
        return self.db.session.query(
            func.sum(SaleItem.price * SaleItem.quantity)
        ).scalar() or 0.0

    def get_sales_statistics(self):
        """Obtiene estadísticas de ventas para gráficos"""
        sales = self.db.session.query(
            Sale.date,
            func.sum(SaleItem.price * SaleItem.quantity).label('amount')
        ).join(SaleItem).group_by(Sale.date).all()
        
        return [{'date': sale.date, 'amount': sale.amount} for sale in sales]