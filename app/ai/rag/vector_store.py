from qdrant_client import QdrantClient
from app.core.settings import settings


from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

class QdrantVectorStore:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

        self.collection_name = settings.QDRANT_COLLECTION


    def create_collection(
        self,
        vector_size: int
    ):

        collections = self.client.get_collections()

        exists = any(
            c.name == self.collection_name
            for c in collections.collections
        )

        if not exists:

            self.client.create_collection(
                collection_name=self.collection_name,

                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )


    def add_chunks(
        self,
        chunks,
        vectors
    ):

        points = []

        for index, (chunk, vector) in enumerate(
            zip(chunks, vectors)
        ):

            points.append(
                PointStruct(
                    id=index,
                    vector=vector,
                    payload={
                        "content": chunk.content,
                        "title": chunk.title,
                        "section": chunk.section,
                        "category": chunk.category,
                        "source": str(chunk.source)
                    }
                )
            )


        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def reset_collection(
        self,
        vector_size
    ):

        collections = self.client.get_collections()

        exists = any(
            c.name == self.collection_name
            for c in collections.collections
        )

        if exists:
            self.client.delete_collection(
                self.collection_name
            )

        self.create_collection(vector_size)
    
    def search(
        self,
        vector,
        limit=5,
        category=None
    ):

        query_filter = None

        if category:

            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(
                            value=category
                        )
                    )
                ]
            )

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit
        )

        if hasattr(response, "points"):
            return response.points

        if isinstance(response, tuple):
            return response[1]

        return response