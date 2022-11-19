from django.db import connection
from .models import Basket


def set_filter(request, model, name):
    fltrs = request.GET.getlist(name)
    if not fltrs:
        return model.objects.all()
    return model.objects.filter(name__in=fltrs).all()

def get_basket_total(user_id):
    return sum([item.ingredient.price for item in Basket.objects.filter(user_id=user_id)])

def calculate_basket(user_id):
    query = """
        SELECT
            i.name ingredient,
            COUNT(i.id) cnt,
            SUM(i.price) price
        FROM main_basket b
        INNER JOIN main_ingredient i
        ON b.ingredient_id = i.id
        WHERE b.user_id = %s
        GROUP BY i.name
        """
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        rows = cursor.fetchall()
        basket = {
            row[0]: {
                'quantity': row[1],
                'price': row[2]
            }
            for row in rows
        }
    
    basket['total'] = get_basket_total(user_id)

    return basket
