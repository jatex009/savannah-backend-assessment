from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def average_price_by_category(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(id=category_id)
            # Get all descendants of the category
            categories = category.get_descendants(include_self=True)
            avg_price = Product.objects.filter(
                category__in=categories,
                is_active=True
            ).aggregate(avg_price=Avg('price'))
            
            return Response({
                'category': category.name,
                'average_price': round(float(avg_price['avg_price'] or 0), 2)
            })
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
