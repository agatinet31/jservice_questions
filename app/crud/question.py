from app.crud.base import CRUDBase
from app.models import Question
from app.schemas import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    """CRUD класс для вопросов."""
    pass


question_crud = CRUDQuestion(Question)
