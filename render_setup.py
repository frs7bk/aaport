#!/usr/bin/env python3
"""
سكربت إعداد بدء التشغيل على Render.com
يقوم بإنشاء المجلدات اللازمة والتحقق من الإعدادات
"""
import os
import logging
import sys

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_render_environment():
    """تهيئة البيئة اللازمة للتشغيل على Render"""
    logger.info("بدء إعداد بيئة Render...")
    
    # التحقق من المتغيرات البيئية الأساسية
    required_env_vars = [
        "DATABASE_URL",
        "FLASK_SECRET_KEY",
        "SESSION_SECRET"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"المتغيرات البيئية التالية مفقودة: {', '.join(missing_vars)}")
    else:
        logger.info("تم التحقق من جميع المتغيرات البيئية المطلوبة")
    
    # تحويل عنوان قاعدة البيانات إذا لزم الأمر
    database_url = os.environ.get("DATABASE_URL", "")
    if database_url.startswith("postgres://"):
        new_db_url = database_url.replace("postgres://", "postgresql://", 1)
        os.environ["DATABASE_URL"] = new_db_url
        logger.info("تم تصحيح DATABASE_URL لاستخدام postgresql://")
    
    # إنشاء مجلدات التحميل
    upload_folders = [
        "static/uploads",
        "static/uploads/profile",
        "static/uploads/portfolio",
        "static/uploads/carousel",
        "static/uploads/services",
        "static/uploads/projects",
        "instance"
    ]
    
    for folder in upload_folders:
        os.makedirs(folder, exist_ok=True)
        logger.info(f"تم إنشاء المجلد: {folder}")
    
    # Render يوفر متغير PORT البيئي
    port = os.environ.get("PORT", 5000)
    logger.info(f"سيتم استخدام المنفذ: {port}")
    
    logger.info("اكتمل إعداد بيئة Render بنجاح!")
    return True

if __name__ == "__main__":
    try:
        setup_render_environment()
    except Exception as e:
        logger.error(f"حدث خطأ أثناء الإعداد: {str(e)}")
        sys.exit(1)