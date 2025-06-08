"""QA Collector for interactive Claude questioning."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import signal
import sys

from ..utils.retro_ui import RetroUI, RetroTheme
from ..claude.claude_processor import ClaudeProcessor
from ..utils.logger import get_logger

logger = get_logger(__name__)


class QuestionCategory(Enum):
    """Categories of questions for project understanding."""
    TECHNICAL = "technical"
    FEATURES = "features"
    ARCHITECTURE = "architecture"
    DEPLOYMENT = "deployment"
    USERS = "users"
    CONSTRAINTS = "constraints"
    INTEGRATIONS = "integrations"


@dataclass
class Question:
    """Represents a single question to ask the user."""
    text: str
    category: QuestionCategory
    context: Optional[str] = None
    follow_up_on: Optional[str] = None
    importance: str = "medium"  # low, medium, high


@dataclass
class Answer:
    """Represents a user's answer to a question."""
    question: Question
    response: str
    timestamp: float


class QACollector:
    """Collects detailed information about the project through Q&A."""
    
    MIN_QUESTIONS = 20
    MAX_QUESTIONS = 100
    
    def __init__(self, ui: RetroUI, claude_processor: Optional[ClaudeProcessor] = None):
        self.ui = ui
        self.claude_processor = claude_processor
        self.questions_asked: List[Question] = []
        self.answers: List[Answer] = []
        self.enough_signal_received = False
        
        # Register Ctrl+E handler
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for Ctrl+E."""
        def handle_ctrl_e(signum, frame):
            self.enough_signal_received = True
            logger.info("User signaled 'enough' with Ctrl+E")
        
        # Note: In real implementation, we'd need to handle this differently
        # as Ctrl+E isn't a standard signal. This is a placeholder.
    
    def collect_project_details(self, project_description: str) -> Dict[str, Any]:
        """Collect detailed project information through Q&A."""
        # Store project description for use in follow-up questions
        self.project_description = project_description
        
        self.ui.show_progress(
            "Starting Q&A Session",
            f"I'll ask you detailed questions about your project: {project_description}\n"
            "Press Ctrl+E at any time when you feel we have enough information."
        )
        
        # Generate initial questions based on project description
        initial_questions = self._generate_initial_questions(project_description)
        
        question_count = 0
        
        # Keep asking questions until we have enough or reach the limit
        while question_count < self.MAX_QUESTIONS and not self.enough_signal_received:
            # Get next question
            if question_count < len(initial_questions):
                question = initial_questions[question_count]
            else:
                # Generate follow-up questions based on previous answers
                question = self._generate_next_question()
                if not question:
                    break
            
            # Ask the question
            answer = self._ask_question(question, question_count + 1)
            if answer:
                self.questions_asked.append(question)
                self.answers.append(answer)
                question_count += 1
            
            # Check if we have minimum questions
            if question_count >= self.MIN_QUESTIONS and self.enough_signal_received:
                break
        
        # Compile the Q&A into a comprehensive project specification
        return self._compile_project_spec()
    
    def _generate_initial_questions(self, project_description: str) -> List[Question]:
        """Generate initial questions based on project description."""
        if self.claude_processor:
            try:
                # Use Claude's dedicated question generation method
                claude_questions = self.claude_processor.generate_project_questions(
                    project_description,
                    existing_qa=None  # No existing Q&A for initial questions
                )
                
                # Convert to Question objects
                questions = []
                for q in claude_questions:
                    category_map = {
                        'TECHNICAL': QuestionCategory.TECHNICAL,
                        'FEATURES': QuestionCategory.FEATURES,
                        'ARCHITECTURE': QuestionCategory.ARCHITECTURE,
                        'DEPLOYMENT': QuestionCategory.DEPLOYMENT,
                        'USERS': QuestionCategory.USERS,
                        'CONSTRAINTS': QuestionCategory.CONSTRAINTS,
                        'INTEGRATIONS': QuestionCategory.INTEGRATIONS,
                    }
                    
                    questions.append(Question(
                        text=q['question'],
                        category=category_map.get(q['category'], QuestionCategory.FEATURES),
                        importance="high" if len(questions) < 10 else "medium"
                    ))
                
                return questions
            except Exception as e:
                logger.warning(f"Failed to generate questions with Claude: {e}")
        
        # Fallback to predefined questions
        return self._get_default_questions(project_description)
    
    def _parse_claude_questions(self, claude_response: str) -> List[Question]:
        """Parse questions from Claude's response."""
        questions = []
        
        for line in claude_response.strip().split('\n'):
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    category_str = parts[0].strip().upper()
                    question_text = parts[1].strip()
                    
                    # Map to QuestionCategory
                    category_map = {
                        'TECHNICAL': QuestionCategory.TECHNICAL,
                        'FEATURES': QuestionCategory.FEATURES,
                        'ARCHITECTURE': QuestionCategory.ARCHITECTURE,
                        'DEPLOYMENT': QuestionCategory.DEPLOYMENT,
                        'USERS': QuestionCategory.USERS,
                        'CONSTRAINTS': QuestionCategory.CONSTRAINTS,
                        'INTEGRATIONS': QuestionCategory.INTEGRATIONS,
                    }
                    
                    category = category_map.get(category_str, QuestionCategory.FEATURES)
                    questions.append(Question(
                        text=question_text,
                        category=category
                    ))
        
        return questions
    
    def _get_default_questions(self, project_description: str) -> List[Question]:
        """Get default questions for any project."""
        is_web = 'web' in project_description.lower()
        is_cli = 'cli' in project_description.lower() or 'command' in project_description.lower()
        is_api = 'api' in project_description.lower()
        
        questions = [
            # Technical questions
            Question("What programming language would you prefer for this project?", QuestionCategory.TECHNICAL, importance="high"),
            Question("Do you have any specific framework preferences?", QuestionCategory.TECHNICAL),
            Question("What type of database would you like to use (if any)?", QuestionCategory.TECHNICAL),
            Question("Do you need real-time features (websockets, live updates)?", QuestionCategory.TECHNICAL),
            
            # Features questions
            Question("What are the core features this project must have?", QuestionCategory.FEATURES, importance="high"),
            Question("Are there any nice-to-have features you'd like to include?", QuestionCategory.FEATURES),
            Question("Do you need user authentication and authorization?", QuestionCategory.FEATURES),
            Question("Will this project handle file uploads or media?", QuestionCategory.FEATURES),
            
            # Architecture questions
            Question("Do you prefer a monolithic or microservices architecture?", QuestionCategory.ARCHITECTURE),
            Question("Should this be a single-page application or traditional multi-page?", QuestionCategory.ARCHITECTURE),
            Question("Do you need API versioning support?", QuestionCategory.ARCHITECTURE),
            
            # Deployment questions
            Question("Where do you plan to deploy this project?", QuestionCategory.DEPLOYMENT, importance="high"),
            Question("Do you need CI/CD pipeline setup?", QuestionCategory.DEPLOYMENT),
            Question("Should this be containerized with Docker?", QuestionCategory.DEPLOYMENT),
            
            # Users questions
            Question("Who are the primary users of this system?", QuestionCategory.USERS, importance="high"),
            Question("How many concurrent users do you expect?", QuestionCategory.USERS),
            Question("Will this be used internally or by external customers?", QuestionCategory.USERS),
            
            # Constraints questions
            Question("What's your timeline for this project?", QuestionCategory.CONSTRAINTS),
            Question("Are there any budget constraints to consider?", QuestionCategory.CONSTRAINTS),
            Question("Do you have any specific compliance requirements (GDPR, HIPAA, etc)?", QuestionCategory.CONSTRAINTS),
            
            # Integration questions
            Question("Will this need to integrate with any existing systems?", QuestionCategory.INTEGRATIONS),
            Question("Do you need third-party service integrations (payment, email, etc)?", QuestionCategory.INTEGRATIONS),
            Question("Should this expose a public API?", QuestionCategory.INTEGRATIONS),
        ]
        
        # Add context-specific questions
        if is_web:
            questions.extend([
                Question("Do you need SEO optimization?", QuestionCategory.FEATURES),
                Question("Should this be mobile-responsive?", QuestionCategory.FEATURES),
                Question("Do you need progressive web app (PWA) features?", QuestionCategory.TECHNICAL),
            ])
        
        if is_cli:
            questions.extend([
                Question("Should this tool have interactive prompts or just command flags?", QuestionCategory.FEATURES),
                Question("Do you need cross-platform support (Windows, Mac, Linux)?", QuestionCategory.TECHNICAL),
                Question("Should this integrate with shell completion?", QuestionCategory.FEATURES),
            ])
        
        if is_api:
            questions.extend([
                Question("What API style do you prefer (REST, GraphQL, gRPC)?", QuestionCategory.TECHNICAL),
                Question("Do you need API documentation (OpenAPI/Swagger)?", QuestionCategory.FEATURES),
                Question("Should this support rate limiting?", QuestionCategory.FEATURES),
            ])
        
        return questions
    
    def _generate_next_question(self) -> Optional[Question]:
        """Generate the next question based on previous answers."""
        if not self.claude_processor or len(self.answers) < 3:
            return None
        
        # Convert answers to the format expected by Claude processor
        existing_qa = []
        for answer in self.answers:
            existing_qa.append({
                'question': answer.question.text,
                'answer': answer.response,
                'category': answer.question.category.value.upper()
            })
        
        try:
            # Use Claude's method that considers conversation history
            follow_up_questions = self.claude_processor.generate_project_questions(
                self.project_description,  # We'll need to store this
                existing_qa=existing_qa
            )
            
            if follow_up_questions:
                # Take the first question from the generated list
                q = follow_up_questions[0]
                
                category_map = {
                    'TECHNICAL': QuestionCategory.TECHNICAL,
                    'FEATURES': QuestionCategory.FEATURES,
                    'ARCHITECTURE': QuestionCategory.ARCHITECTURE,
                    'DEPLOYMENT': QuestionCategory.DEPLOYMENT,
                    'USERS': QuestionCategory.USERS,
                    'CONSTRAINTS': QuestionCategory.CONSTRAINTS,
                    'INTEGRATIONS': QuestionCategory.INTEGRATIONS,
                }
                
                return Question(
                    text=q['question'],
                    category=category_map.get(q['category'], QuestionCategory.FEATURES),
                    importance="medium",
                    context="Based on your previous answers"
                )
            
            return None
        except Exception as e:
            logger.warning(f"Failed to generate follow-up question: {e}")
            return None
    
    def _ask_question(self, question: Question, question_number: int) -> Optional[Answer]:
        """Ask a single question and get the answer."""
        import time
        
        # Format the question with context
        question_text = question.text
        if question.context:
            question_text = f"{question.context}\n\n{question.text}"
        
        # Show question count and category
        title = f"Question {question_number} ({question.category.value})"
        if question.importance == "high":
            title += " [Important]"
        
        # Add hint about Ctrl+E
        hint = ""
        if question_number >= self.MIN_QUESTIONS:
            hint = "\n\n[Press Ctrl+E if you feel we have enough information]"
        
        response = self.ui.ask_text(
            title,
            question_text + hint,
            allow_empty=True
        )
        
        if response:
            return Answer(
                question=question,
                response=response,
                timestamp=time.time()
            )
        
        return None
    
    def _compile_project_spec(self) -> Dict[str, Any]:
        """Compile all Q&A into a comprehensive project specification."""
        spec = {
            "qa_summary": {
                "total_questions": len(self.answers),
                "categories": {}
            },
            "detailed_responses": {},
            "compiled_requirements": {}
        }
        
        # Group answers by category
        for answer in self.answers:
            category = answer.question.category.value
            if category not in spec["qa_summary"]["categories"]:
                spec["qa_summary"]["categories"][category] = 0
                spec["detailed_responses"][category] = []
            
            spec["qa_summary"]["categories"][category] += 1
            spec["detailed_responses"][category].append({
                "question": answer.question.text,
                "answer": answer.response,
                "importance": answer.question.importance
            })
        
        # Use Claude to compile requirements if available
        if self.claude_processor:
            # Convert answers to the format expected by compile method
            qa_session = []
            for answer in self.answers:
                qa_session.append({
                    'question': answer.question.text,
                    'answer': answer.response,
                    'category': answer.question.category.value.upper()
                })
            
            try:
                # Use Claude's dedicated compilation method
                compiled_spec = self.claude_processor.compile_qa_into_spec(
                    self.project_description,
                    qa_session
                )
                spec["compiled_requirements"]["claude_spec"] = compiled_spec
                
                # Also create a structured version for easier access
                spec["compiled_requirements"]["structured"] = {
                    "full_specification": compiled_spec,
                    "generated_from_qa": True,
                    "total_questions_answered": len(self.answers)
                }
            except Exception as e:
                logger.warning(f"Failed to compile spec with Claude: {e}")
        
        # Add raw Q&A for reference
        spec["raw_qa"] = [
            {
                "question": a.question.text,
                "answer": a.response,
                "category": a.question.category.value,
                "timestamp": a.timestamp
            }
            for a in self.answers
        ]
        
        return spec