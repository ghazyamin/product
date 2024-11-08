from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

class product(BaseModel):
  id: int
  name: str
  number: int

def setup_database():
  try:
    conn = sqlite3.connect('products.db') # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor() # إنشاء مؤشر
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number INTEGER
        )
    ''')
    conn.commit() # حفظ التغييرات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch products"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات

setup_database()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/products/")
async def read_products():
  try:
    conn = sqlite3.connect('products.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر (cursor) للتفاعل مع قاعدة البيانات
    cursor.execute("SELECT * FROM products")  # تنفيذ استعلام SQL لجلب جميع الصفوف من جدول products
    rows = cursor.fetchall()  # جلب جميع النتائج من قاعدة البيانات
    conn.close()  # إغلاق الاتصال بقاعدة البيانات
    return rows  # إرجاع البيانات التي تم جلبها من قاعدة البيانات
  except sqlite3.Error as e:  # التعامل مع الأخطاء المحتملة
    print(e)  # طباعة الخطأ
    return {"error": "Failed to fetch products"}  # إرجاع رسالة خطأ في حالة فشل جلب البيانات
 
class productCreate(BaseModel):
    name: str
    number: int
    
@app.post("/products/")
async def create_product(product: productCreate):
  try:
      conn = sqlite3.connect('products.db')
      cursor = conn.cursor()
      cursor.execute("INSERT INTO products (name, number) VALUES (?, ?)", (product.name, product.number))
      conn.commit()
      conn.close()
      return {"message": "product added successfully"}
  except sqlite3.Error as e:
      print(e)
      return {"error": "Failed to create product"}


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: product):
  try:
    conn = sqlite3.connect('products.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("UPDATE products SET name = ?, number = ? WHERE id = ?",
                  (product.name, product.number, product_id))  #SQL لتحديث بيانات طالب
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"id": product_id, **product.dict()}  # إرجاع بيانات الطالب المحدثة
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to update product"}  # إرجاع رسالة خطأ

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
  try:
    conn = sqlite3.connect('products.db')  # إنشاء اتصال بقاعدة البيانات
    cursor = conn.cursor()  # إنشاء مؤشر
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))  # تنفيذ استعلام SQL لحذف طالب
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    conn.close()  # إغلاق الاتصال
    return {"message": "product deleted"}  # إرجاع رسالة تأكيد الحذف
  except sqlite3.Error as e:  # في حالة حدوث خطأ
    print(e)  # طباعة الخطأ
    return {"error": "Failed to delete product"}  # إرجاع رسالة خطأ
