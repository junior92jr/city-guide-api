from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, RecommendationViewSet

app_name = "places"

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="categories")
router.register("", RecommendationViewSet, basename="places")

urlpatterns = router.urls
