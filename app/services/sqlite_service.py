import os
import sqlite3
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

class SQLiteService:
    """
    บริการสำหรับจัดการฐานข้อมูล SQLite และเก็บข้อมูล embeddings
    """
    
    def __init__(self, db_path: str = None):
        """
        สร้าง SQLiteService
        
        Args:
            db_path: พาธไปยังไฟล์ฐานข้อมูล SQLite ถ้าไม่ระบุจะใช้ค่าเริ่มต้น
        """
        if db_path is None:
            # สร้างโฟลเดอร์ data ถ้ายังไม่มี
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "embeddings.db"
            
        self.db_path = str(db_path)
        self._create_tables()
    
    def _create_tables(self) -> None:
        """
        สร้างตารางในฐานข้อมูลถ้ายังไม่มี
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # สร้างตาราง documents สำหรับเก็บข้อมูลเอกสาร
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # สร้างตาราง embeddings สำหรับเก็บ embeddings
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                model TEXT NOT NULL,
                embedding TEXT NOT NULL,
                dimensions INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
            )
            ''')
            
            conn.commit()
    
    def add_document(self, content: str, embedding: List[float], model: str, metadata: Dict[str, Any] = None) -> int:
        """
        เพิ่มเอกสารและ embedding ลงในฐานข้อมูล
        
        Args:
            content: เนื้อหาของเอกสาร
            embedding: embedding vector
            model: ชื่อโมเดลที่ใช้สร้าง embedding
            metadata: ข้อมูลเพิ่มเติมของเอกสาร
            
        Returns:
            int: ID ของเอกสารที่เพิ่ม
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # เพิ่มเอกสาร
            cursor.execute(
                "INSERT INTO documents (content, metadata) VALUES (?, ?)",
                (content, json.dumps(metadata) if metadata else None)
            )
            document_id = cursor.lastrowid
            
            # เพิ่ม embedding
            cursor.execute(
                "INSERT INTO embeddings (document_id, model, embedding, dimensions) VALUES (?, ?, ?, ?)",
                (document_id, model, json.dumps(embedding), len(embedding))
            )
            
            conn.commit()
            return document_id
    
    def search_similar(self, query_embedding: List[float], model: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        ค้นหาเอกสารที่มี embedding ใกล้เคียงกับ query_embedding
        
        Args:
            query_embedding: embedding vector ของคำค้นหา
            model: ชื่อโมเดลที่ใช้สร้าง embedding
            top_k: จำนวนผลลัพธ์ที่ต้องการ
            
        Returns:
            List[Dict[str, Any]]: รายการเอกสารที่มี embedding ใกล้เคียงที่สุด
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # ดึงข้อมูล embeddings ทั้งหมดสำหรับโมเดลที่ระบุ
            cursor.execute(
                """
                SELECT e.document_id, e.embedding, d.content, d.metadata
                FROM embeddings e
                JOIN documents d ON e.document_id = d.id
                WHERE e.model = ?
                """,
                (model,)
            )
            
            results = []
            query_embedding_np = np.array(query_embedding)
            
            for row in cursor.fetchall():
                document_id, embedding_json, content, metadata_json = row
                embedding = np.array(json.loads(embedding_json))
                
                # คำนวณ cosine similarity
                similarity = self._cosine_similarity(query_embedding_np, embedding)
                
                results.append({
                    "document_id": document_id,
                    "content": content,
                    "metadata": json.loads(metadata_json) if metadata_json else None,
                    "similarity": float(similarity)
                })
            
            # เรียงลำดับตามความคล้ายคลึงจากมากไปน้อย
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            return results[:top_k]
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        คำนวณ cosine similarity ระหว่างสองเวกเตอร์
        
        Args:
            a: เวกเตอร์แรก
            b: เวกเตอร์ที่สอง
            
        Returns:
            float: ค่า cosine similarity
        """
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def get_document(self, document_id: int) -> Optional[Dict[str, Any]]:
        """
        ดึงข้อมูลเอกสารตาม ID
        
        Args:
            document_id: ID ของเอกสาร
            
        Returns:
            Optional[Dict[str, Any]]: ข้อมูลเอกสาร หรือ None ถ้าไม่พบ
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT d.id, d.content, d.metadata, e.model, e.embedding
                FROM documents d
                LEFT JOIN embeddings e ON d.id = e.document_id
                WHERE d.id = ?
                """,
                (document_id,)
            )
            
            row = cursor.fetchone()
            if not row:
                return None
            
            document_id, content, metadata_json, model, embedding_json = row
            
            return {
                "document_id": document_id,
                "content": content,
                "metadata": json.loads(metadata_json) if metadata_json else None,
                "model": model,
                "embedding": json.loads(embedding_json) if embedding_json else None
            }
    
    def delete_document(self, document_id: int) -> bool:
        """
        ลบเอกสารตาม ID
        
        Args:
            document_id: ID ของเอกสาร
            
        Returns:
            bool: True ถ้าลบสำเร็จ, False ถ้าไม่พบเอกสาร
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            
            return cursor.rowcount > 0
