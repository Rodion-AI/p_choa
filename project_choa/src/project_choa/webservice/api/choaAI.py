import tracemalloc
from dotenv import load_dotenv

from openai import AsyncOpenAI
from .core_and_router import Router
from .accounting import Accounting
from .ask import Ask
from .analyze import Analyze
from .joke import Joke
tracemalloc.start()


# создаем класс ChoaAI
class ChoaAI():

    load_dotenv()

    def __init__(self):
        self.client = AsyncOpenAI()
        self.total_summary = ''
    
    # метод вызова нейро-финансиста
    async def neuro_finansist(self, note: str):

        output = await Router.activate(note, self.total_summary, self.client)
        self.total_summary += note

        if 'accounting' in output:
            out_answer, was_written = await Accounting.activate(note, self.total_summary, self.client)

            if was_written == True:
                self.total_summary = ''
                return 'Спасибо, внесла операцию в журнал'
            else:
                questions = await Ask.activate(out_answer, self.client)
                self.total_summary += questions
                return questions
            
        elif 'analyze' in output:
            out_answer = await Analyze.activate(self.client)
            return out_answer
        
        elif 'error' in output:
            out_answer = await Joke.activate(note, self.client)
            return out_answer
        else:
            return 'Error router'