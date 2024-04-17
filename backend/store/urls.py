from django.urls import path
from .views import product_view, category_thing, RegisterUser, VerifyOtp,single_product, UserLogin, set_review, cart,DeleteCategory,EditCategory,DeleteProduct,EditProduct, Category_wise,DeleteReview

urlpatterns = [
     path('product/', product_view.as_view(), name = "product" ),
     path('category/', category_thing.as_view(), name = "category" ),
     path('register/', RegisterUser.as_view(), name = "register" ),
     path('verify/', VerifyOtp.as_view(), name = "verify" ),
     path('login/', UserLogin.as_view(), name = "login" ),
     path('review/', set_review.as_view(), name = "review" ),
     path('cart/', cart.as_view(), name = "cart" ),
     path('detail/<int:product_id>/', single_product.as_view(), name = "detail" ),
     path('deleteCategory/<int:category_id>/', DeleteCategory.as_view(), name = "deleteCategory" ),
     path('editCategory/<int:category_id>/', EditCategory.as_view(), name = "editCategory" ),
     path('deleteProduct/<int:product_id>/', DeleteProduct.as_view(), name = "deleteProduct" ),
      path('editpdt/<int:product_id>/', EditProduct.as_view(), name = "editpdt" ),
      path('listing/', Category_wise.as_view(), name = "listing" ),
      path('deletereview/<int:review_id>/', DeleteReview.as_view(), name = "deletereview" ),
]
