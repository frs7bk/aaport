#!/usr/bin/env python3
"""
اختبار الاتصال بقاعدة البيانات
استخدم هذا السكربت للتحقق من إمكانية الاتصال بقاعدة البيانات
"""
import os
import sys
import logging
from sqlalchemy import create_engine, text
import time

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection(max_retries=5, retry_delay=5):
    """
    اختبار الاتصال بقاعدة البيانات مع إعادة المحاولة
    
    Args:
        max_retries (int): عدد محاولات إعادة الاتصال
        retry_delay (int): الفاصل الزمني بين المحاولات بالثواني
        
    Returns:
        bool: True إذا كان الاتصال ناجحًا، False في حالة الفشل
    """
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        logger.error("متغير DATABASE_URL غير محدد في البيئة")
        return False
    
    # تحويل postgres:// إلى postgresql:// إذا لزم الأمر
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        logger.info("تم تعديل رابط قاعدة البيانات لاستخدام postgresql://")
    
    # محاولة الاتصال بقاعدة البيانات مع إعادة المحاولة
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"محاولة الاتصال بقاعدة البيانات ({attempt}/{max_retries})...")
            
            # إنشاء محرك قاعدة البيانات مع إعدادات مناسبة
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={"connect_timeout": 10}
            )
            
            # اختبار الاتصال باستخدام استعلام بسيط
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(f"تم الاتصال بنجاح! نتيجة الاستعلام: {result.fetchone()}")
            
            # إذا وصلنا إلى هنا، فإن الاتصال ناجح
            return True
            
        except Exception as e:
            logger.error(f"فشل الاتصال بقاعدة البيانات: {str(e)}")
            
            if attempt < max_retries:
                logger.info(f"إعادة المحاولة بعد {retry_delay} ثوانٍ...")
                time.sleep(retry_delay)
            else:
                logger.error("استنفدت جميع محاولات الاتصال. تعذر الوصول إلى قاعدة البيانات.")
                return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        logger.info("✅ تم الاتصال بقاعدة البيانات بنجاح!")
        sys.exit(0)
    else:
        logger.error("❌ فشل الاتصال بقاعدة البيانات!")
        sys.exit(1)