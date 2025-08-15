import tracemalloc
from dotenv import load_dotenv

from openai import AsyncOpenAI
from api.core_and_router import Router
from api.accounting import Accounting
from api.ask import Ask
from api.analyze import Analyze
from api.joke import Joke
tracemalloc.start()


# создаем класс ChoaAI
class ChoaAI():

    load_dotenv()

    def __init__(self):
        self.client = AsyncOpenAI()
        self.total_summary = ''

    # метод вызова нейро-финансиста
    async def neuro_finansist(self, note: str):

        router = Router(note, self.total_summary, self.client)
        output = await router.activate()
        self.total_summary += note

        if 'accounting' in output:
            accounting = Accounting(note, self.total_summary, self.client)
            out_answer, was_written = await accounting.activate()

            if was_written == True:
                self.total_summary = ''
                return 'Спасибо, внесла операцию в журнал'
            else:
                ask = Ask(out_answer, self.client)
                questions = await ask.activate()
                self.total_summary += questions
                return questions
            
        elif 'analyze' in output:
            analyze = Analyze(self.client)
            out_answer = await analyze.activate()
            return out_answer
        
        elif 'error' in output:
            out_answer = await Joke.activate(note, self.client)
            return out_answer
        else:
            return 'Error router'