from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
import json

from app.services.file_processor import process_file
from app.database.database import SessionLocal
from app.database.models import File as FileModel, Feature

router = APIRouter()


@router.get("/test")
def test_api():
    return {
        "message": "API routes are working"
    }


@router.post("/files/")
async def upload_file(file: UploadFile = File(...)):

    # 1. Check file extension
    if not file.filename.lower().endswith((".kml", ".zip")):
        raise HTTPException(
            status_code=400,
            detail="Only .kml and .zip files are allowed"
        )

    # 2. Determine file type
    if file.filename.endswith(".kml"):
        file_type = "kml"
    else:
        file_type = "zip"

    # 3. Save uploaded file
    safe_filename = os.path.basename(file.filename)

    file_path = os.path.join(
        "storage",
        "uploads",
        safe_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 4. Process file
    try:
        result = process_file(
            file_path,
            file_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # 5. Open database
    db: Session = SessionLocal()

    try:

        # 6. Create file record
        db_file = FileModel(
            filename=safe_filename,
            file_type=file_type,
            feature_count=result["feature_count"],
            original_crs=result["original_crs"],
            measurement_crs=result["measurement_crs"],
            status="COMPLETED"
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        # 7. Save every feature
        for feature in result["features"]:

            db_feature = Feature(
                file_id=db_file.id,
                feature_index=feature["feature_index"],
                geometry_type=feature["geometry_type"],
                geometry=feature["geometry"],
                properties=json.dumps(feature["properties"]),
                area_sq_m=feature["area_sq_m"],
                length_m=feature["length_m"]
            )

            db.add(db_feature)

        db.commit()

        # 8. Return response
        return {
            "id": db_file.id,
            "filename": db_file.filename,
            "feature_count": db_file.feature_count,
            "original_crs": db_file.original_crs,
            "measurement_crs": db_file.measurement_crs,
            "status": db_file.status
        }

    finally:
        db.close()

@router.get("/files/{file_id}")
def get_file(file_id: int):

    db: Session = SessionLocal()

    try:
        db_file = db.query(FileModel).filter(
            FileModel.id == file_id
        ).first()

        if db_file is None:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        return {
            "id": db_file.id,
            "filename": db_file.filename,
            "file_type": db_file.file_type,
            "feature_count": db_file.feature_count,
            "original_crs": db_file.original_crs,
            "measurement_crs": db_file.measurement_crs,
            "status": db_file.status,
            "created_at": db_file.created_at
        }

    finally:
        db.close()

@router.get("/files/{file_id}/measurements/")
def get_measurements(file_id: int):

    db: Session = SessionLocal()

    try:
        # Check whether file exists
        db_file = db.query(FileModel).filter(
            FileModel.id == file_id
        ).first()

        if db_file is None:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        # Get all features belonging to this file
        features = db.query(Feature).filter(
            Feature.file_id == file_id
        ).all()

        measurements = []

        for feature in features:
            measurements.append({
                "feature_id": feature.feature_index,
                "geometry_type": feature.geometry_type,
                "area_sq_m": feature.area_sq_m,
                "length_m": feature.length_m
            })

        return {
            "file_id": file_id,
            "measurements": measurements
        }

    finally:
        db.close()