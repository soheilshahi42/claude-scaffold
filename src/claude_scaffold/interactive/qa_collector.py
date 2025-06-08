"""QA Collector for interactive Claude questioning."""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import signal
import sys
import os
from contextlib import contextmanager

from ..utils.retro_ui import RetroUI, RetroTheme
from ..claude.claude_processor import ClaudeProcessor
from ..utils.logger import get_logger

logger = get_logger(__name__)


@contextmanager
def suppress_output():
    """Temporarily suppress stdout/stderr to prevent logs from showing."""
    # Save the original stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Redirect to devnull
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            # Restore original stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr


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
        
        question_count = 0
        
        # Keep asking questions until we have enough or reach the limit
        while question_count < self.MAX_QUESTIONS and not self.enough_signal_received:
            
            # Show progress while generating the next question
            if question_count == 0:
                self.ui.show_qa_progress(
                    "Starting Q&A session... Analyzing your project description..."
                )
            else:
                self.ui.show_qa_progress(
                    f"Generating question {question_count + 1} based on your previous answers..."
                )
            
            # Generate the next question based on all previous Q&A
            question = self._generate_contextual_question(question_count)
            if not question:
                # If we can't generate more questions, we're done
                break
            
            # Ask the question
            answer = self._ask_question(question, question_count + 1)
            if answer:
                self.questions_asked.append(question)
                self.answers.append(answer)
                question_count += 1
            else:
                # Empty answer means user wants to skip
                continue
            
            # Check if we have minimum questions
            if question_count >= self.MIN_QUESTIONS and self.enough_signal_received:
                break
        
        # Show progress while compiling the specification
        if self.answers:
            self.ui.show_qa_progress(
                f"Compiling {len(self.answers)} Q&A responses into comprehensive specification..."
            )
        
        # Compile the Q&A into a comprehensive project specification
        return self._compile_project_spec()
    
    def _generate_contextual_question(self, question_number: int) -> Optional[Question]:
        """Generate a single contextual question based on all previous Q&A."""
        if not self.claude_processor:
            logger.error("Claude processor not available for Q&A generation")
            return None
        
        # Build the context from all previous Q&A
        qa_context = ""
        if self.answers:
            qa_context = "\n\nPrevious Q&A:\n"
            for i, answer in enumerate(self.answers, 1):
                qa_context += f"\nQ{i}: {answer.question.text}\n"
                qa_context += f"A{i}: {answer.response}\n"
        
        # Create a comprehensive prompt for question generation
        prompt = f"""You are conducting a detailed discovery session for a software project. Your goal is to understand ALL aspects needed to develop this project successfully.

Project Description: "{self.project_description}"
{qa_context}

Based on the project description and any previous Q&A above, generate the NEXT SINGLE most important question to ask.

Consider these aspects that need to be covered throughout the session:
- Technical stack (languages, frameworks, databases, tools)
- Architecture and system design
- Core features and functionality
- User interface and user experience
- Authentication and authorization
- Data models and relationships
- API design and endpoints
- Third-party integrations
- Performance and scalability requirements
- Security considerations
- Deployment and hosting
- Development timeline and constraints
- Testing strategy
- Error handling and logging
- Documentation needs
- Future extensibility

Questions asked so far: {question_number}

Generate exactly ONE question that:
1. Builds on previous answers (if any)
2. Explores an aspect not yet covered
3. Is specific and actionable
4. Helps clarify technical decisions

Format: CATEGORY: question text

Categories: TECHNICAL, FEATURES, ARCHITECTURE, DEPLOYMENT, USERS, CONSTRAINTS, INTEGRATIONS"""
        
        try:
            # Suppress output during Claude call to prevent logs from showing
            with suppress_output():
                response = self.claude_processor._call_claude(prompt, expect_json=False)
            
            # Parse the single question from response
            for line in response.strip().split('\n'):
                if ':' in line and any(cat in line.upper() for cat in ['TECHNICAL', 'FEATURES', 'ARCHITECTURE', 'DEPLOYMENT', 'USERS', 'CONSTRAINTS', 'INTEGRATIONS']):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        category = parts[0].strip().upper()
                        question_text = parts[1].strip()
                        
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
                            text=question_text,
                            category=category_map.get(category, QuestionCategory.FEATURES),
                            importance="high" if question_number < 10 else "medium",
                            context=f"Question {question_number + 1}"
                        )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to generate contextual question: {e}")
            # No fallback - all questions must be dynamic
            return None
    
    
    def _ask_question(self, question: Question, question_number: int) -> Optional[Answer]:
        """Ask a single question and get the answer."""
        import time
        
        # Format the question with context
        question_text = question.text
        if question.context:
            question_text = f"{question.context}\n\n{question.text}"
        
        # Show question count and category
        title = f"Q&A SESSION - QUESTION {question_number}"
        if question.importance == "high":
            title += " [IMPORTANT]"
        
        # Use the new ask_qa_input method for better UI and Ctrl+E support
        response, enough_signal = self.ui.ask_qa_input(
            title,
            question_text,
            question_number,
            question.category.value,
            allow_skip_after=self.MIN_QUESTIONS,
            subtitle=f"Deep Dive Mode - {self.MIN_QUESTIONS}-{self.MAX_QUESTIONS} Questions"
        )
        
        # If user signaled they have enough info, set the flag
        if enough_signal:
            self.enough_signal_received = True
            logger.info(f"User signaled 'enough' at question {question_number}")
        
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
                with suppress_output():
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