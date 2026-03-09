from fastapi import APIRouter
from routes.api.students import router as students_router
from routes.api.companies import router as companies_router
from routes.api.placements import router as placements_router
from routes.api.charts import router as charts_router
from routes.api.export import router as export_router
from routes.api.ai import router as ai_router
from routes.api.predictions import router as predictions_router

router = APIRouter(prefix="/api")

router.include_router(students_router)
router.include_router(companies_router)
router.include_router(placements_router)
router.include_router(charts_router)
router.include_router(export_router)
router.include_router(ai_router)
router.include_router(predictions_router)
